import networkx as nx
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
import tempfile
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def construct_graph(photos):
    # G = nx.Graph()

    # for photo in photos:
    #     G.add_node(photo['id'], date=photo['mediaMetadata']['creationTime'])

    # for photo1 in photos:
    #     for photo2 in photos:
    #         photo1_date = datetime.datetime.strptime(
    #             photo1['mediaMetadata']['creationTime'], "%Y-%m-%dT%H:%M:%S%z")
    #         photo2_date = datetime.datetime.strptime(
    #             photo2['mediaMetadata']['creationTime'], "%Y-%m-%dT%H:%M:%S%z")

    #         if abs((photo1_date - photo2_date).days) <= 14:
    #             G.add_edge(photo1['id'], photo2['id'])
    G = nx.Graph()

    fig, ax = plt.subplots()

    img=mpimg.imread(photos[0]["baseUrl"], format=photos[0]["mimeType"].split("/")[1])
    G.add_node(0,image= img)
    G.add_node(1,image= img)
    G.add_edge(0,1)

    pos = nx.spring_layout(G)

    # Draw the graph using the spring layout
    nx.draw(G, pos, with_labels=False)

    # draw images on the vertices
    for n in G.nodes:
        image = G.nodes[n]['image']
        
        # Offset the image so that it's centered
        offset_image = OffsetImage(image, zoom=0.1)
        image_marker = AnnotationBbox(offset_image, pos[n])
        ax.add_artist(image_marker)

    # Show the graph
    plt.show()

    
    # if len(photos) >= 2:
    #     photo1 = photos[0]
    #     photo2 = photos[1]

    #     G.add_node(photo1['id'], date=photo1['mediaMetadata']['creationTime'])
    #     G.add_node(photo2['id'], date=photo2['mediaMetadata']['creationTime'])
    #     G.add_edge(photo1['id'], photo2['id'])

    
    return G
