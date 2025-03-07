from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
from typing import List
import pandas as pd
from ads_analytics_bridge.complements import Data_base, Errors
from decouple import config

class Google_analytics(Errors):

    def __init__(self, service_account_file, empresa):
        super().__init__()
        self.empresa = empresa
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        self.__client = BetaAnalyticsDataClient(credentials=credentials)
        self.__DB_table_canal = config('DB_table_canal')
        self.__DB_table_device = config('DB_table_device')
        self.__DB_table_summary = config('DB_table_summary')
        self.__properties = None
        self.__date_range = None
        self.__dimensions = None
        self.__metrics = None
        self.__request = None
        self.__rename = {
            'date':'fecha',
            'deviceCategory':'category',
            'sessionDefaultChannelGroup':'channel',
            'sessions': 'sessions',
            'screenPageViewsPerUser':'views',
            'transactions':'transactions',
            'totalUsers':'users',
            'averageSessionDuration':'avg_time_sessions',
        }
    
    def set_properties(self, properties: str):
        self.__properties = f'properties/{properties}'
        self.__id_source =properties
    
    def set_date_ranges(self, start_date, end_date):
        self.__start_date = start_date
        self.__end_date = end_date
        self.__date_range = [{'start_date': start_date, 'end_date': end_date}]
    
    def set_dimensions(self, dimensions: List[str]):
        self.__dimensions = [{'name': dimension} for dimension in dimensions]
    
    def set_metrics(self, metrics: List[str]):
        self.__metrics = [{'name': metric} for metric in metrics]
        self.__metrics_names = metrics
    
    def set_all(self, properties, start_date, end_date, metrics, dimensions=None):
        self.set_properties(properties)
        self.set_date_ranges(start_date, end_date)
        self.set_metrics(metrics)
        if dimensions is not None:
            self.set_dimensions(dimensions)
    
    def pre_validate(func):
        def wrapper(self, *args, **kwargs):
            one = self.__date_range == '' or self.__date_range is None
            two = self.__properties == '' or self.__properties is None
            three = self.__metrics == '' or self.__metrics is None
            if one or two or three:
                raise ValueError(f"No se puede ejecutar {func.__name__} Es necesario setear minimo las fechas, la propiedad y las metricas")
            else:
                return func(self, *args, **kwargs)
        return wrapper
    
    @pre_validate
    def create_request(self):
        self.__request = {
            'property': self.__properties,
            'date_ranges': self.__date_range,
            'metrics': self.__metrics,
            'metric_aggregations': ['TOTAL']
        }
        if self.__dimensions is not None and self.__dimensions != '':
            self.__request['dimensions'] = self.__dimensions
    
    def execute(self):
        if self.__request == None:
            raise('No se establecio la request por favor usar el metodo .create_request')
        response = self.__client.run_report(self.__request)
        self.__data = []
        titles = []
        for i, name in enumerate(response.dimension_headers):
            titles.append(name.name)
        for i, name in enumerate(response.metric_headers):
            titles.append(name.name)
        for i, row in enumerate(response.rows):
            values = []
            for j, value in enumerate(row.dimension_values):
                values.append(value.value)
            for j, value in enumerate(row.metric_values):
                values.append(value.value)
            temporal = {titles[x]:values[x] for x in range(len(values))}
            self.__data.append(temporal)
    
    def get_data(self):
        return self.__data
    
    @Errors.manage_errors('Ejecución rapida')
    def easy_execute(self, properties, start_date, end_date, metrics, dimensions=None):
        self.set_all(properties, start_date, end_date, metrics, dimensions)
        self.create_request()
        self.execute()
        data = self.get_data()
        self.__data = data
        return data
    
    @Errors.manage_errors('Generar dataframe')
    def generate_dataframe(self):
        df = pd.DataFrame(self.__data)
        df.rename(columns=self.__rename, inplace=True)
        df = df.where(pd.notnull(df), 'None')
        df = df.replace('None', None)
        df['empresa'] = self.empresa
        df['id_source'] = self.__id_source
        for colum in df.columns:
            if 'fecha' == colum:
                df['fecha'] = pd.to_datetime(df['fecha'], format='%Y%m%d')
                df['fecha'] = df['fecha'].dt.tz_localize('UTC')
                df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
            elif 'views' == colum:
                df[colum] = df[colum].astype(float).round(2)
            elif colum in ['sessions', 'transactions']:
                df[colum] = df[colum].astype(float).astype(int)
        df = df.where(pd.notnull(df), 'None')
        df = df.replace('None', None)
        self.__df = df
        return self.__df
    
    @Errors.manage_errors('guardar datos canal')
    def save_data_canal(self):
        self.__db = Data_base()
        data, column_names = self.__db.get_data_canal(self.__start_date, self.__end_date, self.empresa)
        df = pd.DataFrame(data, columns=column_names)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
        merged_df = self.__df.merge(df, on=['fecha', 'empresa', 'id_source'], how='left', indicator=True)
        new = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
        old = merged_df[merged_df['_merge'] == 'both'].drop(columns=['_merge'])
        new.columns = [column.replace('_x','') for column in new.columns]
        self.__db.save_canal(new)
    
    @Errors.manage_errors('guardar datos device')
    def save_data_device(self):
        self.__db = Data_base()
        data, column_names = self.__db.get_data_device(self.__start_date, self.__end_date, self.empresa)
        df = pd.DataFrame(data, columns=column_names)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
        merged_df = self.__df.merge(df, on=['fecha', 'empresa', 'id_source'], how='left', indicator=True)
        new = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
        old = merged_df[merged_df['_merge'] == 'both'].drop(columns=['_merge'])
        new.columns = [column.replace('_x','') for column in new.columns]
        self.__db.save_device(new)
    
    @Errors.manage_errors('guardar datos summary')
    def save_data_summary(self):
        self.__db = Data_base()
        data, column_names = self.__db.get_data_summary(self.__start_date, self.__end_date, self.empresa)
        df = pd.DataFrame(data, columns=column_names)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
        merged_df = self.__df.merge(df, on=['fecha', 'empresa', 'id_source'], how='left', indicator=True)
        new = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
        old = merged_df[merged_df['_merge'] == 'both'].drop(columns=['_merge'])
        new.columns = [column.replace('_x','') for column in new.columns]
        self.__db.save_summary(new)
    
    @Errors.manage_errors('Actualizar Actividad')
    def update_activity_canal(self):
        error = self.return_error()
        estado = 'incorrecto' if len(error) > 0 else 'correcto'
        mensaje = ''
        if len(error) > 0:
            for i in range(len(error)):
                mensaje = mensaje + " " + error[i]['modulo']
        fecha_max = self.__df['fecha'].max()[:10]
        fecha_min = self.__df['fecha'].min()[:10]
        self.__db.update_activity(self.__DB_table_canal, self.empresa, estado, mensaje, fecha_max, fecha_min)
    
    @Errors.manage_errors('Actualizar Actividad')
    def update_activity_device(self):
        error = self.return_error()
        estado = 'incorrecto' if len(error) > 0 else 'correcto'
        mensaje = ''
        if len(error) > 0:
            for i in range(len(error)):
                mensaje = mensaje + " " + error[i]['modulo']
        fecha_max = self.__df['fecha'].max()[:10]
        fecha_min = self.__df['fecha'].min()[:10]
        self.__db.update_activity(self.__DB_table_device, self.empresa, estado, mensaje, fecha_max, fecha_min)
    
    @Errors.manage_errors('Actualizar Actividad')
    def update_activity_summary(self):
        error = self.return_error()
        estado = 'incorrecto' if len(error) > 0 else 'correcto'
        mensaje = ''
        if len(error) > 0:
            for i in range(len(error)):
                mensaje = mensaje + " " + error[i]['modulo']
        fecha_max = self.__df['fecha'].max()[:10]
        fecha_min = self.__df['fecha'].min()[:10]
        self.__db.update_activity(self.__DB_table_summary, self.empresa, estado, mensaje, fecha_max, fecha_min)

