from google.ads.googleads.client import GoogleAdsClient
import os
import yaml
import pandas as pd
from ads_analytics_bridge.complements import Data_base, Errors
from decouple import config as cf
from datetime import datetime, timedelta

class Google_ads(Errors):

    def __init__(self, start_date, end_date, campaign_data:list, segments:list, metrics:list, id_customer, empresa):
        super().__init__()
        self.__start_date = start_date
        self.__end_date = end_date
        self.__campaign_data = campaign_data
        self.__segments = segments
        self.__metrics = metrics
        self.__id_customer = id_customer
        self.empresa = empresa
        self.__DB_table_pauta = cf('DB_table_pauta')
        self.__rename = {
            'id':'id_campana',
            'date':'fecha',
            'name':'campana',
            'cost_micros':'total_cost',
            'clicks':'link_clicks',
            'conversions':'website_conversion',
            'engagements':'engagement',
        }
        self.init()
    
  
    @Errors.manage_errors('Conexion Google Ads')
    def init(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_ads.json'
        with open('google-ads.yaml', 'r') as file:
            config = yaml.safe_load(file)
        credentials = {
            "developer_token": config['developer_token'],
            "refresh_token": config['refresh_token'],
            "client_id": config['client_id'],
            "client_secret": config['client_secret'],
            "use_proto_plus": True,
        }
        client = GoogleAdsClient.load_from_dict(credentials)
        self.ga_service = client.get_service('GoogleAdsService')
    
    @Errors.manage_errors('Creacion Query')
    def create_query(self):    
        fecha = datetime.strptime(self.__end_date, '%Y-%m-%d')
        hoy = datetime.today()
        if fecha.date() == hoy.date():
            fecha -= timedelta(days=1)
            self.__end_date = fecha.strftime('%Y-%m-%d')
        self.__columns = {}
        self.__columns_list = []
        select = 'SELECT'
        for i in self.__campaign_data:
            select += f'\n campaign.{i}' if select == 'SELECT' else f', \n campaign.{i}'
            self.__columns[i] = f'row.campaign.{i}'
            self.__columns_list.append(i)
        for i in self.__segments:
            select += f'\n segments.{i}' if select == 'SELECT' else f', \n segments.{i}'
            self.__columns[i] = f'row.segments.{i}'
            self.__columns_list.append(i)
        for i in self.__metrics:
            select += f'\n metrics.{i}' if select == 'SELECT' else f', \n metrics.{i}'
            self.__columns[i] = f'row.metrics.{i}'
            self.__columns_list.append(i)
        where = f'''
            FROM campaign
            WHERE segments.date BETWEEN '{self.__start_date}' AND '{self.__end_date}'
        '''
        self.__query = select + where
    
    @Errors.manage_errors('Conseguir Datos')
    def get_data(self):
        results = []
        response = self.ga_service.search(customer_id=self.__id_customer, query=self.__query)
        for row in response:
            result = {}
            for field in self.__columns_list:
                result[field] = eval(self.__columns[field])
            results.append(result)
        df = pd.DataFrame(results)
        df['empresa'] = self.empresa
        df['publisher_platform'] = 'google'
        df['Area'] = self.empresa
        df['objetive'] = ''
        df['post_shares'] = None
        df['leads'] = None
        df['reach'] = None
        df['reach_add'] = None
        df.rename(columns=self.__rename, inplace=True)
        df['total_cost'] = df['total_cost'] * 10**-6
        self.__data_df = df
        return df
    
    @Errors.manage_errors('Guardar Datos')
    def save_data(self):
        self.__db = Data_base()
        data, column_names = self.__db.get_pauta(self.__start_date, self.__end_date, self.empresa)
        df = pd.DataFrame(data, columns=column_names)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
        merged_df = self.__data_df.merge(df, on=['fecha', 'id_campana'], how='left', indicator=True)
        new = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
        old = merged_df[merged_df['_merge'] == 'both'].drop(columns=['_merge'])
        new.columns = [column.replace('_x','') for column in new.columns]
        self.__db.save_pauta(new)
    
    @Errors.manage_errors('Actualizar Actividad')
    def update_activity(self):
        error = self.return_error()
        estado = 'incorrecto' if len(error) > 0 else 'correcto'
        fecha_max = self.__data_df['fecha'].max()
        fecha_min = self.__data_df['fecha'].min()
        self.__db.update_activity(self.__DB_table_pauta, self.empresa, estado, '', fecha_max, fecha_min)