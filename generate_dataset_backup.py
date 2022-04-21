import _magnum
import habitat
import habitat_sim
from PIL import Image
from habitat.sims.habitat_simulator.actions import HabitatSimActions
import cv2
import envs.spring_env
import math
import warnings
import visitor_utils
import pyvista as pv
import os
import random
import numpy as np
from habitat_sim.utils.common import d3_40_colors_rgb
from cocostuffapi.PythonAPI.pycocotools.cocostuffhelper import segmentationToCocoMask
from pycocotools import mask
import json



FORWARD_KEY="w"
LEFT_KEY="a"
RIGHT_KEY="d"
FINISH="f"
LOOK_UP_KEY="u"
LOOK_DOWN_KEY="j"


HOSPITAL_1 = "hospital_1"
HOSPITAL_2 = "hospital_2"
LIVINGLAB_1 = "livinglab_1"
LIVINGLAB_2 = "livinglab_2"
B315 = "b315"
APARTMENT = "apartment"
B670 = "b670"
CORRIDOR = "corridor"
CASTLE = "castle"
SEMANTIC_H = "semantic_h" #IN progress hospital
SEMANTIC_L = "semantic_l" #IN progress living lab
HL2COLMAP = "hl2col"
SPSG = "spsg"

def _segmentationToPoly(mask, ):
    contours, _ = cv2.findContours((mask).astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    segmentationPoly = []

    for contour in contours:
        contour = contour.flatten().tolist()
        if len(contour) > 4:
            segmentationPoly.append(contour)
    return segmentationPoly


def normalize(v, tolerance=0.00001):
    mag2 = sum(n * n for n in v)
    if mag2 == 0:
        return v
    if abs(mag2 - 1.0) > tolerance:
        mag = math.sqrt(mag2)
        i = 0
        for n in v:
            v[i] = n / mag
            i += 1
    return v

def create_quat(angle,x,y,z):
    v=[0,0,0,0]
    v[0] = math.cos(math.radians(angle / 2))
    v[1] = math.sin(math.radians(angle / 2)) * math.cos(math.radians(x))
    v[2] = math.sin(math.radians(angle / 2)) * math.cos(math.radians(y))
    v[3] = math.sin(math.radians(angle / 2)) * math.cos(math.radians(z))
    return v

def transform_rgb_bgr(image):
    return image[:, :, [2, 1, 0]]


def searchfor(matrix, number):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == number:
                return i
    return 666

def bbox(segmentation):
    if (len(segmentation) == 0 or len(segmentation[0]) == 0 or len(segmentation[1]) == 0):
        return [0,0,0,0]
    else:
        miny=min(segmentation[0])
        maxy=max(segmentation[0])
        minx=min(segmentation[1])
        maxx=max(segmentation[1])
        return [float(minx),float(miny),float(maxx-minx),float(maxy-miny)]



def visit(location="not set"):

    config=habitat.get_config("configs/tasks/pointnav.yaml")

    objects = []
    env = envs.spring_env.SpringEnv(
        config=config,
        objects=objects,
    )

    if location == HOSPITAL_1:
        env.episodes[0].scene_id = ("data/scene_datasets/hospital_1.glb")
    elif location == HOSPITAL_2:
        env.episodes[0].scene_id = ("data/scene_datasets/hospital_2.glb")
    elif location == LIVINGLAB_1:
        env.episodes[0].scene_id = ("data/scene_datasets/livinglab_1.glb")
    elif location == LIVINGLAB_2:
        env.episodes[0].scene_id = ("data/scene_datasets/livinglab_2.glb")
    elif location == B315:
        env.episodes[0].scene_id = ("data/scene_datasets/B315.glb")
    elif location == B670:
        env.episodes[0].scene_id = ("data/scene_datasets/B670.glb")
    elif location == APARTMENT:
        env.episodes[0].scene_id = ("data/scene_datasets/apartment_1.glb")
    elif location == CORRIDOR:
        env.episodes[0].scene_id = ("data/scene_datasets/corridor.glb")
    elif location == CASTLE:
        env.episodes[0].scene_id = ("data/scene_datasets/skokloster-castle.glb")
    elif location == SEMANTIC_H:
        env.episodes[0].scene_id = ("data/scene_datasets/hospital_empty.glb") #hospital_empty.glb is missing roof
    elif location == SEMANTIC_L:
        env.episodes[0].scene_id = ("data/scene_datasets/living_lab_empty.glb")  #living_lab_empty.glb is missing roof
    elif location == HL2COLMAP:
        env.episodes[0].scene_id = ("data/scene_datasets/HL2COLMAP_noSPSG.glb")
    elif location == SPSG:
        print("SPSG LOCATION SELECTED")
        env.episodes[0].scene_id = ("data/scene_datasets/B-635_SPSG.glb")
    else:
        warnings.warn("Place not set or unrecognized, using HOSPITAL_1(default)")
        env.episodes[0].scene_id = ("data/scene_datasets/hospital_1.glb")

    print("JSON initiated")
    dictionary = {
        "categories" : [],
        "images" : [],
        "type" : "instances",
        "annotations" : []

    print("Environment creation successful")
    observations = env.reset()

    if location ==  SEMANTIC_H:
        orig_path = "data/objects_categorized/Hospital"
    if location == SEMANTIC_L:
        orig_path = "data/objects_categorized/Living_lab"
    if location == HL2COLMAP:
        orig_path = "data/objects_categorized/HL2COLMAP"
    if location == SPSG:
        orig_path = "data/objects_categorized/SPSG"
    orig_dirs = os.listdir(orig_path)
    i = 0
    category_names = []
    category_ids = []
    for file in orig_dirs:
        if not file.startswith('.'):
            category_names.append(str(file))
            path = orig_path + "/" + file
            dirs = os.listdir(path)
            insert = []
            for item in dirs:
                if item.endswith(".glb"):
                    i += 1
                    insert.append(i)
                    final_path = path + "/" + item[:-4]
                    name_obj = path + "/" + file + "_obj/" + item[:-4] + ".obj"
                    print(name_obj)
                    obj_file=pv.read(name_obj)
                    obj_file.rotate_x(-90) #IDK IF THIS WILL BE NECESARRY BUT WE WILL SEE WHAT HABITAT DOES WITH NEW SCENES
                    coords=obj_file.center
                    env.add_object(final_path[4:], coords, i)  # Weird scaling + translation
            category_ids.append(insert)

    #JSON for categories (open file write into it)
    for i in range(len(category_ids)):
        category = {
            "id" : i+1,
            "name" : category_names[i]
        }
        dictionary["categories"].append(category)

    cnt = 0 #5229
    #Sample dataset INSERT DESIRED NUMBER OF IMAGES

    print("SIMULATION STARTING")
    for i in range (50): #Image id is i+1

        #Find random point in map
        new_point = env.sim.sample_navigable_point()

        #Add random angles + heights
        height_off=random.uniform(-1.3,1.1)
        x_axis_off=random.uniform(-5,5)
        z_axis_off=random.uniform(0,360)

        #Apply randomness
        while new_point[1]>3:
            new_point = env.sim.sample_navigable_point()
        height_check = new_point[1] + height_off
        if (height_check > 0.7):
            y_axis_off = random.uniform(-25, 0)
        else:
            y_axis_off = random.uniform(0, 25)
        rotation=create_quat(180,0+x_axis_off,90+y_axis_off ,0+z_axis_off)

        observations = env.sim.get_observations_at(new_point,normalize(rotation)) #get observations at random point
        rgb = transform_rgb_bgr(observations["rgb"]) #create RGB scan

        #Visualize for detecting object and categorize what is seen
        semantic_img =Image.new("P", (observations['semantic'].shape[1], observations['semantic'].shape[0]))
        semantic_img.putpalette(d3_40_colors_rgb.flatten())
        semantic_img.putdata((observations['semantic'].flatten()).astype(np.uint8))
        semantic_img = np.array(semantic_img)

        obj_ids = [x for x in np.unique(semantic_img)]

        print("i is",i)
        image = {
            "id" : i+1,
            "file_name" : str(i+1) + ".jpg",
            "height" : 756,
            "width" : 1344
        }
        dictionary["images"].append(image)

        #JSON
        for j in range(1,len(obj_ids)):
            cnt += 1
            obj_id=obj_ids[j]
            result=np.where(semantic_img==obj_id)
            iscrowd = 0
            image_id=i+1    #ID of image
            category_id=searchfor(category_ids,obj_id) #Name of category
            b_box = bbox(result) #B_box in format [x,y,width,height]
            seg = segmentationToCocoMask(semantic_img, obj_id) #Segmentaton from semantic img
            area = float(mask.area(seg))  #Area of segmentation
            seg['counts'] = str(seg['counts'], "utf-8")
            bitmap = mask.decode(seg)
            seg = _segmentationToPoly(bitmap)

            #Remove too small masks
            if b_box[2]>10 and b_box[3]>10:
                check=True
            else:
                check=False

            #Annotations JSON, napsat file a pak zkopírovat
            if (result != [] and result[0] != [] and result[1] != [] and seg != [] and check == True):
                print("JSON annotation added")
                annotation = {
                    "id": cnt,
                    "image_id": i + 1,
                    "category_id": category_id + 1,
                    "bbox": b_box,
                    "segmentation": seg,
                    "area": area,
                    "iscrowd": iscrowd
                }
                dictionary["annotations"].append(annotation)
            else:
                cnt -= 1

        #Visualization with colours

        semantic_img = Image.new("P", (observations['semantic'].shape[1], observations['semantic'].shape[0]))
        semantic_img.putpalette(d3_40_colors_rgb.flatten())
        semantic_img.putdata((observations['semantic'].flatten() % 40).astype(np.uint8))
        semantic_img = semantic_img.convert("RGB")
        semantic_img = np.array(semantic_img)

        #cv2.circle(semantic_img, (1, 1), 2, (255, 255, 255), -1)
        #cv2.imshow("RGB",rgb)
        #cv2.imshow("semantic", semantic_img)

        name=str(i+1)+".jpg"
        path_rgb = "data/datasets/coco/rgbs/" + name
        cv2.imwrite(path_rgb, rgb)
        #cv2.waitKey(0)

        print("\n\n\n NEW IMAGE no:" + str(i+1) + "\n\n\n")

    with open('json_data.json', 'w') as outfile:
        outfile.write(json.dumps(dictionary))


    print("Sampling completed!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', "--location",
                        action='store',
                        help='The location to visit. Known locations: hospital_1, hospital_2, livinglab_1, livinglab_2, default(hospital_1).',
                        dest="location")
    parser.set_defaults(location=HOSPITAL_1)
    args = parser.parse_args()
    visit(args.location)
