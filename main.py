import datetime
import networkx as nx
import requests
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Photos API information
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def service_account_login():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)

    return creds


def get_all_photos(creds):
    headers = {
        'Authorization': 'Bearer {}'.format(creds.token)
    }

    response = requests.get(
        'https://photoslibrary.googleapis.com/v1/mediaItems', headers=headers)
    items = response.json().get('mediaItems', [])

    nextPageToken = response.json().get('nextPageToken')

    while nextPageToken:
        response = requests.get(
            f'https://photoslibrary.googleapis.com/v1/mediaItems?pageToken={nextPageToken}', headers=headers)
        items.extend(response.json().get('mediaItems', []))
        nextPageToken = response.json().get('nextPageToken')

    return items


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

    # Get all photos
    photos = get_all_photos(creds)
    print(f'Found {len(photos)} photos')

    # Construct graph
    G = construct_graph(photos)
    print(f'Constructed graph with {len(G.nodes)} nodes and {len(G.edges)} edges')


if __name__ == "__main__":
    main()
