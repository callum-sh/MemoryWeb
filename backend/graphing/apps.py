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

    def ready(self):
        # Run your code here
        creds = self.service_account_login()
        settings.CREDS = creds

    def service_account_login(self):
        for port in range(8080, 8090):
            try:
                credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=port)
                return creds
            except OSError as e:
                if e.errno == 98:
                    continue
                else:
                    raise
        raise Exception("Unable to find an available port.")
