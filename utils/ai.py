import matplotlib.patches as patches
import matplotlib.pyplot as plt
import torch
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from PIL import Image

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

plt.show()
