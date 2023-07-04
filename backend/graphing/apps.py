from django.apps import AppConfig
from django.apps import AppConfig
import os
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import requests
from django.conf import settings


SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


class GraphingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graphing'

    # def ready(self):
    #     # Run your code here
    #     creds = self.service_account_login()
    #     # photos = self.get_all_photos(creds)
    #     # settings.PHOTOS = photos
    #     settings.CREDS = creds

    # def service_account_login(self):
    #     for port in range(8080, 8090):
    #         try:
    #             credentials_path = os.path.join(
    #                 os.path.dirname(__file__), 'credentials.json')
    #             flow = InstalledAppFlow.from_client_secrets_file(
    #                 credentials_path, SCOPES)
    #             creds = flow.run_local_server(port=port)
    #             return creds
    #         except OSError as e:
    #             if e.errno == 98:
    #                 continue
    #             else:
    #                 raise
    #     raise Exception("Unable to find an available port.")

    # def get_all_photos(self, creds):
    #     headers = {
    #         'Authorization': 'Bearer {}'.format(creds.token)
    #     }

    #     photos = []

    #     page_token = None
    #     while True:
    #         params = {'pageSize': 100}
    #         if page_token:
    #             params['pageToken'] = page_token

    #         response = requests.get(
    #             'https://photoslibrary.googleapis.com/v1/mediaItems', headers=headers, params=params)
    #         items = response.json().get('mediaItems', [])
    #         photos.extend(items)

    #         page_token = response.json().get('nextPageToken')
    #         if not page_token or len(photos) >= 100:
    #             break

    #     return photos[:100]
