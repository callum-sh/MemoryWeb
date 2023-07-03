import datetime
import networkx as nx
import requests
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Photos API information
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def service_account_login():
    for port in range(8080, 8090):
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


def construct_graph(photos):
    G = nx.Graph()

    for photo in photos:
        G.add_node(photo['id'], date=photo['mediaMetadata']['creationTime'])

    for photo1 in photos:
        for photo2 in photos:
            photo1_date = datetime.datetime.strptime(
                photo1['mediaMetadata']['creationTime'], "%Y-%m-%dT%H:%M:%S%z")
            photo2_date = datetime.datetime.strptime(
                photo2['mediaMetadata']['creationTime'], "%Y-%m-%dT%H:%M:%S%z")

            if abs((photo1_date - photo2_date).days) <= 14:
                G.add_edge(photo1['id'], photo2['id'])

    return G


def main():
    # Login to Google Photos
    creds = service_account_login()

    # Get all photos (limited to the first 100)
    photos = get_all_photos(creds)
    print(f'Found {len(photos)} photos')

    # Construct graph
    G = construct_graph(photos)
    print(f'Constructed graph with {len(G.nodes)} nodes and {len(G.edges)} edges')


if __name__ == "__main__":
    main()
