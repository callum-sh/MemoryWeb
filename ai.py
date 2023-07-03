import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image

# return what objects are in the image


def get_objects(image_path):
    # get the model
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
        pretrained=True)
    model.eval()

    # get the labels
    labels = ['__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
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
              'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    # Open the image
    image = Image.open(image_path)

    # transform the image
    transform = transforms.Compose([
        transforms.ToTensor()
    ])

    # get the predictions
    with torch.no_grad():
        pred = model([transform(image).to('cpu')])[0]

    # get the bounding boxes
    boxes = pred['boxes'].tolist()
    scores = pred['scores'].tolist()
    pred_labels = [labels[i] for i in pred['labels'].tolist()]

    # return the results
    return boxes, scores, pred_labels


if __name__ == "__main__":
    boxes, scores, labels = get_objects('test.jpeg')
    print(boxes)
    print(scores)
    print(labels)
