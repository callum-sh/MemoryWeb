from django.apps import AppConfig
from django.apps import AppConfig
import os
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


class GraphingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graphing'

    def ready(self):
        # Run your code here
        creds = self.service_account_login()
        # os.environ['CREDS'] = creds

    def service_account_login(self):
        for port in range(8080, 8090):
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/home/joshpuglielli/Desktop/memory-web/MemoryWeb/backend/graphing/credentials.json', SCOPES)
                creds = flow.run_local_server(port=port)
                return creds
            except OSError as e:
                if e.errno == 98:
                    continue
                else:
                    raise
        raise Exception("Unable to find an available port.")
