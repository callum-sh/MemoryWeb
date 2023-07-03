import datetime
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
import networkx as nx
import plotly.graph_objects as go
import random

import os
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the edges and vertices
edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
vertices = [1, 2, 3, 4]

# Create a graph
G = nx.Graph()
G.add_nodes_from(vertices)
G.add_edges_from(edges)

# Generate positions for the nodes
pos = nx.spring_layout(G)

edge_trace = go.Scatter(x=[], y=[], line=dict(
    width=0.5, color='#888'), hoverinfo='none', mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(x=[], y=[], mode='markers', hoverinfo='text', marker=dict(
    showscale=True, colorscale='YlGnBu', reversescale=True, color=[], size=10))

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

# Add node colors to the node trace
for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color'] += tuple([len(adjacencies[1])])

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(title='<br>Network graph',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False,
                           showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

fig.show()


def get_photos():
    scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']

    creds = None

    if os.path.exists('_secrets_/token.json'):
        creds = Credentials.from_authorized_user_file(
            '_secrets_/token.json', scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '_secrets_/client_secret.json', scopes)
            creds = flow.run_local_server()
        print(creds)
        # Save the credentials for the next run
        with open('_secrets_/token.json', 'w') as token:
            token.write(creds.to_json())


# Google Photos API information
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'


def service_account_login():
    creds = None

    # Load credentials from the 'credentials.json' file
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)

    try:
        # Build the service
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        return service
    except RefreshError:
        print("Failed to connect.")
        return None


def get_all_photos(service):
    results = service.mediaItems().list(pageSize=100).execute()
    items = results.get('mediaItems', [])

    while 'nextPageToken' in results:
        results = service.mediaItems().list(
            pageSize=100, pageToken=results['nextPageToken']).execute()
        items.extend(results.get('mediaItems', []))

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
    service = service_account_login()
    if service is None:
        print("Failed to log in to Google Photos.")
        return

    # Get all photos
    photos = get_all_photos(service)

    # Construct graph
    G = construct_graph(photos)


if __name__ == "__main__":
    main()
