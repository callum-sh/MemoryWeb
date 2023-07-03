import datetime
import networkx as nx
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
import matplotlib.pyplot as plt

# Google Photos API information
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def service_account_login():
    for port in range(8000, 8090):
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=port)
            return creds
        except OSError as e:
            if e.errno == 98:
                continue
            else:
                raise
    raise Exception("Unable to find an available port.")


def get_all_photos(creds):
    headers = {
        'Authorization': 'Bearer {}'.format(creds.token)
    }

    photos = []

    page_token = None
    while True:
        params = {'pageSize': 100}
        if page_token:
            params['pageToken'] = page_token

        response = requests.get(
            'https://photoslibrary.googleapis.com/v1/mediaItems', headers=headers, params=params)
        items = response.json().get('mediaItems', [])
        photos.extend(items)

        page_token = response.json().get('nextPageToken')
        if not page_token or len(photos) >= 100:
            break

    return photos[:100]
