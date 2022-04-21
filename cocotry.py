from coco_assistant import COCO_Assistant
import os

img_dir = os.path.join(os.getcwd(), 'data/datasets/coco/images')
ann_dir = os.path.join(os.getcwd(), 'data/datasets/coco/annotations')
cas = COCO_Assistant(img_dir, ann_dir)

cas.visualise()