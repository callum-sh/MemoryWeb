from google_auth_oauthlib.flow import InstalledAppFlow
import requests
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import torch
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from PIL import Image
import os

import networkx as nx
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import urllib.request
import tempfile
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# COCO dataset classes for indexing made predictions
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]


def load_image(image_path):
    """
    Load given image path into PIL image for processing.

    """
    img = Image.open(image_path).convert("RGB")
    img = F.to_tensor(img)
    return img


def analyze_photo(image_path):
    image_path = './test/1.jpeg'
    image = load_image(image_path)

# load model
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    model = model.eval()

# make prediction
    with torch.no_grad():
        prediction = model([image])

# filter predictions by score threshold
    threshold = 0.5
    filtered_prediction = []

    for i in range(len(prediction[0]['labels'])):
        if prediction[0]['scores'][i] > threshold:
            filtered_prediction.append({
                'bbox': prediction[0]['boxes'][i].tolist(),
                'label': prediction[0]['labels'][i].item(),
                'score': prediction[0]['scores'][i].item()
            })

    print(filtered_prediction)

# draw bounding boxes
    fig, ax = plt.subplots(1)
    ax.imshow(image.permute(1, 2, 0))

    for pred in filtered_prediction:
        xmin, ymin, xmax, ymax = pred['bbox']
        rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax -
                                 ymin, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    # Adding the label and score
        label = COCO_INSTANCE_CATEGORY_NAMES[pred['label']]
        score = pred['score']
        ax.text(xmin, ymin, "{} {:.0f}%".format(label, score*100), color='white',
                bbox=dict(facecolor='r', edgecolor='r', pad=0.5, alpha=0.5))

    plt.savefig('./test/out.jpeg')


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

    img = mpimg.imread(photos[0]["baseUrl"],
                       format=photos[0]["mimeType"].split("/")[1])
    G.add_node(0, image=img)
    G.add_node(1, image=img)
    G.add_edge(0, 1)

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


# Google Photos API information
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def service_account_login():
    for port in range(8080, 8090):
        try:
            credentials_path = os.path.join(
                os.path.dirname(__file__), 'credentials.json')
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
