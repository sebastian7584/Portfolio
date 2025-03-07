import webbrowser
import requests
from flask import request
from decouple import config
import json
import pandas as pd
from ads_analytics_bridge.complements import Data_base, Errors

class Meta_api(Errors):

    def __init__(self, start_date, end_date, id_customer, empresa):
        super().__init__()
        self.__token = config('token_meta')
        self.__start_date = start_date
        self.__end_date = end_date
        self.__id_customer = id_customer
        self.empresa = empresa
        self.__url_base_graph = 'https://graph.facebook.com/v14.0'
        self.__ad_accounts = None
        self.__pages = None
        self.__data_organic_insights_facebook = None
        self.__data_organic_insights_instagram = None
        self.__df_organic_instagram = self.__df_organic_facebook = pd.DataFrame()
        self.__DB_table_pauta = config('DB_table_pauta')
        self.__DB_table_organic = config('DB_table_organic')
        self.__rename = {
            'date_start':'fecha',
            'campaign_id':'id_campana',
            'campaign_name':'campana',
            'objective': 'objetive',
            'spend':'total_cost',
            'inline_link_clicks':'link_clicks',
            'post':'post_shares',
            'lead':'leads',
            'purchase':'website_conversion',
            'post_engagement':'engagement',
        }
        self.__rename_reach_add = {
            'date_stop':'fecha',
            'campaign_id':'id_campana',
            'campaign_name':'campana',
            'objective': 'objetive',
            'spend':'total_cost',
            'inline_link_clicks':'link_clicks',
            'post':'post_shares',
            'lead':'leads',
            'purchase':'website_conversion',
            'post_engagement':'engagement',
        }
        self.__rename_facebook = {
            'created_time':'fecha',
            'id':'id_post',
            'permalink_url':'url',
            'post_impressions': 'impressions',
            'post_impressions_unique':'reach',
            'like':'like_post',
        }
        self.__rename_instagram = {
            'timestamp':'fecha',
            'id':'id_post',
            'permalink':'url',
            'likes':'like_post',
            'comments':'comment',
            'shares':'share',
            'saved':'save',
            'video_views':'video_view',
        }

    @Errors.manage_errors('Listas ad accounts')
    def generate_ad_accounts(self):
        if self.__token is not None:
            url = f'{self.__url_base_graph}/me/adaccounts'
            params = {
                'access_token': self.__token,
                'fields': 'account_id,name,account_status,business_name,currency,spend_cap,amount_spent,timezone_name,created_time',
                'limit': 200,
            }
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                self.__ad_accounts = data.get('data', [])
            else:
                self.__ad_accounts = [{response.status_code}]
        else:
            raise('Metodo no ejecutable sin antes generar o establecer un token, utilice .generate_token para generar uno o .set_token para asignar uno valido')
    
    @Errors.manage_errors('Retornar ad accounts')
    def get_accounts(self):
        return self.__ad_accounts
    
    @Errors.manage_errors('Listar managed pages')
    def generate_managed_pages(self):
        if self.__token is not None:
            base_url = 'https://graph.facebook.com/v20.0'
            url = f'{base_url}/me/accounts'
            params = {
                'access_token': self.__token,
                'fields': 'id,name,access_token'
            }
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                self.__pages = data.get('data', [])
                while True:
                    if 'paging' in data:
                        paging = data['paging']
                        if 'next' in paging:
                            next_page = data['paging']['next']
                            response = requests.get(next_page)
                            data = response.json()
                            self.__pages.extend(data['data'])
                        else: break
                    else: break
                
            else:
                self.__pages = [{response.status_code}]
        else:
            raise('Metodo no ejecutable sin antes generar o establecer un token, utilice .generate_token para generar uno o .set_token para asignar uno valido')
    
    @Errors.manage_errors('Retornar managed pages')
    def get_pages(self):
        return self.__pages
    
    @Errors.manage_errors('Consultar datos')
    def get_ad_insights(self):
        url = f'https://graph.facebook.com/v20.0/act_{self.__id_customer}/insights'
        params = {
            'access_token': self.__token,
            'time_increment': 1,
            'fields': 'date_start, date_stop, campaign_id, campaign_name, ad_id, ad_name, created_time, objective, spend, impressions, inline_link_clicks, reach, actions',
            'time_range': json.dumps({'since': self.__start_date, 'until': self.__end_date}),
            'level': 'ad',
            'breakdowns':'publisher_platform',
            'limit': 200
        }
        response = requests.get(url, params=params)
        data = response.json()
        self.__data_ad_insights = data['data']
        while True:
            if 'paging' in data:
                paging = data['paging']
                if 'next' in paging:
                    next_page = data['paging']['next']
                    response = requests.get(next_page)
                    data = response.json()
                    self.__data_ad_insights.extend(data['data'])
                else: break
            else: break
        return self.__data_ad_insights
    
    @Errors.manage_errors('Consultar datos reach acumulado')
    def get_reach_add(self):
        data_reach_ad = []
        for end_date in self.__end_dates:
            df_filtrado = self.__new[self.__new['fecha'] == end_date]
            df_filtrado['created_time'] = pd.to_datetime(df_filtrado['created_time'])
            start_date = df_filtrado['created_time'].min().strftime('%Y-%m-%d')
            url = f'https://graph.facebook.com/v20.0/act_{self.__id_customer}/insights'
            params = {
                'access_token': self.__token,
                'fields': 'campaign_id, reach',
                'time_range': json.dumps({'since': start_date, 'until': end_date}),
                'level': 'campaign',
                'breakdowns':'publisher_platform',
                'limit': 200
            }
            response = requests.get(url, params=params)
            data = response.json()
            data_reach_ad.extend(data['data'])
            while True:
                if 'paging' in data:
                    paging = data['paging']
                    if 'next' in paging:
                        next_page = data['paging']['next']
                        response = requests.get(next_page)
                        data = response.json()
                        data_reach_ad.extend(data['data'])
                    else: break
                else: break
        self.__data_reach_ad = data_reach_ad
    
    @Errors.manage_errors('Obtener token pagina')
    def generate_pages_access_token(self):
        self.__page_access_token = ''
        for i in self.__pages:
            if i['id'] == self.__id_customer:
                self.__page_access_token = i['access_token']
                break


    @Errors.manage_errors('Listar post facebook')
    def get_post_organic_facebook(self):
        base_url = 'https://graph.facebook.com/v20.0'
        metrics_url = f'{base_url}/{self.__id_customer}/posts'
        params = {
            'access_token': self.__page_access_token,
            'fields': 'created_time, status_type, id,permalink_url, insights.metric(post_impressions, post_impressions_unique), likes.summary(true), comments.summary(true)',
            # 'fields': 'id, actions',
            'since': self.__start_date,
            'until': self.__end_date,
            'limit': 100,
        }
        response = requests.get(metrics_url, params=params)
        data = response.json()
        self.__data_organic_insights_facebook = data['data']
        while True:
            if 'paging' in data:
                paging = data['paging']
                if 'next' in paging:
                    next_page = data['paging']['next']
                    response = requests.get(next_page)
                    data = response.json()
                    self.__data_organic_insights_facebook.extend(data['data'])
                else: break
            else: break
        
    @Errors.manage_errors('Listar post Instagram')
    def get_post_organic_instagram(self):
        base_url = 'https://graph.facebook.com/v20.0'
        url_id_instagram = f'{base_url}/{self.__id_customer}'
        params = {
            'access_token': self.__page_access_token,
            'fields': 'instagram_business_account'
        }
        response = requests.get(url_id_instagram, params=params)
        ig_account_data = response.json()
        ig_user_id = None
        if 'instagram_business_account' in ig_account_data:
            if 'id' in ig_account_data['instagram_business_account']:
                ig_user_id = ig_account_data['instagram_business_account']['id']
        if ig_user_id is not None:
            url = f'{base_url}/{ig_user_id}/media'
            # url = f'{base_url}/17889627753078351'
            params = {
                'access_token': self.__page_access_token,
                'fields': 'timestamp, id, permalink, media_type, insights.metric(impressions, reach, likes, comments, shares, saved, video_views)',
                'since': self.__start_date,
                'until': self.__end_date,
                # 'since': '2024-08-14',
                # 'until': '2024-08-15',
                'limit': 100,
            }
            response = requests.get(url, params=params)
            data = response.json()
            self.__data_organic_insights_instagram = data['data']
            while True:
                if 'paging' in data:
                    paging = data['paging']
                    if 'next' in paging:
                        next_page = data['paging']['next']
                        response = requests.get(next_page)
                        data = response.json()
                        self.__data_organic_insights_instagram.extend(data['data'])
                    else: break
                else: break
    
    @Errors.manage_errors('organizar datos facebook')
    def organize_post_organic_facebook(self):
        base_url = 'https://graph.facebook.com/v17.0'
        for i in range(len(self.__data_organic_insights_facebook)):
            self.__data_organic_insights_facebook[i]['empresa'] = self.empresa
            self.__data_organic_insights_facebook[i]['publisher_platform'] = 'Facebook'
            self.__data_organic_insights_facebook[i]['media_type'] = 'video' if 'video' in self.__data_organic_insights_facebook[i]['permalink_url'] else 'post'
            if 'insights' in self.__data_organic_insights_facebook[i].keys():
                for insight in self.__data_organic_insights_facebook[i]['insights']['data']:
                    self.__data_organic_insights_facebook[i][insight['name']] = insight['values'][0]['value']
            self.__data_organic_insights_facebook[i]['like'] = self.__data_organic_insights_facebook[i]['likes']['summary']['total_count']
            self.__data_organic_insights_facebook[i]['comment'] = self.__data_organic_insights_facebook[i]['comments']['summary']['total_count']
            post_id = self.__data_organic_insights_facebook[i]['id']
            insights_url = f'{base_url}/{post_id}'
            insights_params = {
                'access_token': self.__page_access_token,
                'fields': 'shares',
            }
            insights_response = requests.get(insights_url, params=insights_params)
            insights_data = insights_response.json()
            if 'shares' in insights_data.keys():
                self.__data_organic_insights_facebook[i]['share'] = insights_data['shares']['count']
            else:
                self.__data_organic_insights_facebook[i]['share'] = None
            self.__data_organic_insights_facebook[i]['save'] = None
            self.__data_organic_insights_facebook[i]['video_view'] = None
        self.__df_organic_facebook = pd.DataFrame(self.__data_organic_insights_facebook)
        self.__df_organic_facebook.rename(columns=self.__rename_facebook, inplace=True)
            
    @Errors.manage_errors('organizar datos instagram')
    def organize_post_organic_instagram(self):  
        for i in range(len(self.__data_organic_insights_instagram)):
            self.__data_organic_insights_instagram[i]['empresa'] = self.empresa
            self.__data_organic_insights_instagram[i]['publisher_platform'] = 'Instagram'
            self.__data_organic_insights_instagram[i]['media_type'] = 'post' if self.__data_organic_insights_instagram[i]['media_type'] == 'IMAGE' else self.__data_organic_insights_instagram[i]['media_type'].lower()
            if 'insights' in self.__data_organic_insights_instagram[i].keys():
                for insight in self.__data_organic_insights_instagram[i]['insights']['data']:
                    self.__data_organic_insights_instagram[i][insight['name']] = insight['values'][0]['value']
            pass
        self.__df_organic_instagram = pd.DataFrame(self.__data_organic_insights_instagram)
        self.__df_organic_instagram.rename(columns=self.__rename_instagram, inplace=True)

    @Errors.manage_errors('concatenar dfs')
    def merge_organic_df(self):
        comuns_titles = self.__df_organic_facebook.columns.intersection(self.__df_organic_instagram.columns)
        df_organic = pd.concat([self.__df_organic_facebook[comuns_titles], self.__df_organic_instagram[comuns_titles]], ignore_index=True)
        df_organic = df_organic.where(pd.notnull(df_organic), 'None')
        df_organic = df_organic.replace('None', None)
        del df_organic['insights']
        self.__df_organic = df_organic

    @Errors.manage_errors('organizar los campos de action')
    def organize_actions(self):
        for i in range(len(self.__data_ad_insights)):
            row = self.__data_ad_insights[i]
            if 'actions' in row:
                for action in row['actions']:
                    self.__data_ad_insights[i][action['action_type']] = action['value']

    @Errors.manage_errors('generar el dataframe')
    def generate_dataframe(self):
        df = pd.DataFrame(self.__data_ad_insights)
        df['campaign_id'] = df['campaign_id'].astype(int)
        df['empresa'] = self.empresa
        if 'post_engagement' not in df.columns:
            df['engagement'] = None
        if 'purchase' not in df.columns:
            df['website_conversion'] = None
        if 'lead' not in df.columns:
            df['leads'] = None
        if 'post' not in df.columns:
            df['post'] = None
        df.rename(columns=self.__rename, inplace=True)
        df = df.where(pd.notnull(df), None)
        df['reach_add'] = 0
        self.__data_df = df
    
    @Errors.manage_errors('Merge con reach add')
    def merge_reach_add(self):
        self.__new = self.__new.drop('reach_add', axis=1)
        df_rech_add = pd.DataFrame(self.__data_reach_ad)
        if len(df_rech_add)>0:
            df_rech_add.rename(columns=self.__rename_reach_add, inplace=True)
            df_rech_add['id_campana'] = df_rech_add['id_campana'].astype(int)
            df_merged = pd.merge(self.__new, df_rech_add[['fecha', 'id_campana', 'publisher_platform', 'reach']], 
                        on=['fecha', 'id_campana', 'publisher_platform'], 
                        how='left', 
                        suffixes=('', '_add'))
            df_merged = df_merged.where(pd.notnull(df_merged), 'None')
            df_merged = df_merged.replace('None', None)
        else:
            df_merged = self.__new
        self.__merged = df_merged
    
    @Errors.manage_errors('Guardar Datos')
    def save_data_organic(self):
        self.__db = Data_base()
        data, column_names = self.__db.get_organic(self.__start_date, self.__end_date, self.empresa)
        df = pd.DataFrame(data, columns=column_names)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
        merged_df = self.__df_organic.merge(df, on=['id_post'], how='left', indicator=True)
        new = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
        old = merged_df[merged_df['_merge'] == 'both'].drop(columns=['_merge'])
        new.columns = [column.replace('_x','') for column in new.columns]
        old.columns = [column.replace('_x','') for column in old.columns]
        self.__db.save_organic(new, old)

    @Errors.manage_errors('Identificar nuevos')
    def identify_new(self):
        self.__db = Data_base()
        data, column_names = self.__db.get_pauta(self.__start_date, self.__end_date, self.empresa)
        df = pd.DataFrame(data, columns=column_names)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')
        merged_df = self.__data_df.merge(df, on=['fecha', 'id_campana', 'publisher_platform'], how='left', indicator=True)
        new = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])
        old = merged_df[merged_df['_merge'] == 'both'].drop(columns=['_merge'])
        new.columns = [column.replace('_x','') for column in new.columns]
        self.__end_dates = new['fecha'].drop_duplicates().tolist()
        self.__new = new

    @Errors.manage_errors('Guardar Datos')
    def save_data(self):
        self.__db.save_pauta(self.__merged)
    
    @Errors.manage_errors('Actualizar Actividad')
    def update_activity(self):
        error = self.return_error()
        estado = 'incorrecto' if len(error) > 0 else 'correcto'
        mensaje = ''
        if len(error) > 0:
            for i in range(len(error)):
                mensaje = mensaje + " " + error[i]['modulo']
        fecha_max = self.__data_df['fecha'].max()
        fecha_min = self.__data_df['fecha'].min()
        self.__db.update_activity(self.__DB_table_pauta, self.empresa, estado, mensaje, fecha_max, fecha_min)
    
    @Errors.manage_errors('Actualizar Actividad')
    def update_activity_organic(self):
        error = self.return_error()
        estado = 'incorrecto' if len(error) > 0 else 'correcto'
        mensaje = ''
        if len(error) > 0:
            for i in range(len(error)):
                mensaje = mensaje + " " + error[i]['modulo']
        fecha_max = self.__df_organic['fecha'].max()[:10]
        fecha_min = self.__df_organic['fecha'].min()[:10]
        self.__db.update_activity(self.__DB_table_organic, self.empresa, estado, '', fecha_max, fecha_min)
    
    @Errors.manage_errors('Exportar excel')
    def create_excel_ad_insights(self): 
        self.__data_df.to_excel('meta_pauta.xlsx')

    @Errors.manage_errors('Exportar excel organicos')
    def create_excel_organic(self): 
        self.__df_organic.to_excel('meta_organico.xlsx')