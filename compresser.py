import argparse
import os, sys
import struct
import numpy as np
import cv2
import zlib
import png

# params
parser = argparse.ArgumentParser()
# data paths
parser.add_argument('--input_path', required=True, help='path to directory to read containing 4 subdirectories: color,depth,pose,intrinsics. color contains rgb images, depth contains corresponding depth images, pose contains corresponding transformation matrixes for each rames and intrinsics contains rgb + depth camera intrinsics + extrinsics')
parser.add_argument('--output_path', required=True, help='path to output sens file')

opt = parser.parse_args()
print(opt)



def read_intrinsic(path): #Path to main_directory
    file = open(path,"r")
    intrinsic = file.read().split()
    return(intrinsic)

def get_num_of_files(path): #Path to directory with frames
    list = os.listdir(path)
    num_of_files =  len(list)
    return num_of_files

def send_RGBD_frame(rgb_path,depth_path,pose_path,sens_file): #Path to main_directory
    print(pose_path)
    pose = np.array(read_intrinsic(pose_path))

    #poses matrix
    for i in range(16):
        sens_file.write(struct.pack("f",float(pose[i])))

    sens_file.write(struct.pack("Q", 0))  # timestamp
    sens_file.write(struct.pack("Q", 0))  # timestamp

    #RGB + DEPTH read as bytes
    with open(rgb_path, "rb") as image:
        f = image.read()
        b = bytearray(f)
    reader = png.Reader(depth_path)
    depth = reader.read_flat()
    depth_bytes=bytearray(depth[2])
    g_com = zlib.compress(depth_bytes)

    sens_file.write(struct.pack("Q", os.path.getsize(rgb_path)))  # size of color
    sens_file.write(struct.pack("Q", sys.getsizeof(g_com))) # size of depth
    sens_file.write(struct.pack(f"!{os.path.getsize(rgb_path)}s", b)) #color data
    sens_file.write(struct.pack(f"!{sys.getsizeof(g_com)}s", g_com)) #depth data






def main():
    sens_file = open(opt.output_path,"wb")

    #Version number/scanner name
    version_number=4
    sens_file.write(struct.pack("I",version_number))
    sens_file.write(struct.pack("Q",7))
    sens_file.write(struct.pack("!7s", b"testing"))

    # Intrinsics
    path_to_intrinsic_color = os.path.join(opt.input_path,"intrinsic/intrinsic_color.txt")
    intrinsic_color = np.array(read_intrinsic(path_to_intrinsic_color))
    for i in range(16):
        sens_file.write(struct.pack("f",float(intrinsic_color[i])))
    path_to_extrinsic_color = os.path.join(opt.input_path, "intrinsic/extrinsic_color.txt")
    extrinsic_color = read_intrinsic(path_to_extrinsic_color)
    for i in range(16):
        sens_file.write(struct.pack("f", float(extrinsic_color[i])))
    path_to_intrinsic_depth = os.path.join(opt.input_path, "intrinsic/intrinsic_depth.txt")
    intrinsic_depth = read_intrinsic(path_to_intrinsic_depth)
    for i in range(16):
        sens_file.write(struct.pack("f", float(intrinsic_depth[i])))
    path_to_extrinsic_depth = os.path.join(opt.input_path, "intrinsic/extrinsic_depth.txt")
    extrinsic_depth = read_intrinsic(path_to_extrinsic_depth)
    for i in range(16):
        sens_file.write(struct.pack("f", float(extrinsic_depth[i])))

    #Compression type
    sens_file.write(struct.pack("i", 2)) #change this accordingly to your format!!! {-1: 'unknown', 0: 'raw', 1: 'png', 2: 'jpeg'}
    sens_file.write(struct.pack("i", 1)) #change this accordingly to your format!!! {-1: 'unknown', 0: 'raw_ushort', 1: 'zlib_ushort', 2: 'occi_ushort'}

    #Image dimensions
    path_to_color = os.path.join(opt.input_path,"color")
    path_to_depth = os.path.join(opt.input_path,"depth")
    path_to_pose = os.path.join(opt.input_path,"pose")
    image_color_rndm = cv2.imread(os.path.join(path_to_color,os.listdir(path_to_color)[0]))
    image_depth_rndm = cv2.imread(os.path.join(path_to_depth, os.listdir(path_to_depth)[0]))
    print(os.path.join(path_to_depth, os.listdir(path_to_color)[0]))
    print("SHAPE IS",image_depth_rndm.shape)
    sens_file.write(struct.pack("I", image_color_rndm.shape[1]))
    sens_file.write(struct.pack("I", image_color_rndm.shape[0]))
    sens_file.write(struct.pack("I", image_depth_rndm.shape[1]))
    sens_file.write(struct.pack("I", image_depth_rndm.shape[0]))
    print(os.path.join(path_to_color, os.listdir(path_to_color)[0]))
    sens_file.write(struct.pack("f", 1000.0))

    #Number of images
    if get_num_of_files(path_to_color) != get_num_of_files(path_to_depth):
        print("Number of depth files does not match the number of color files! ending")
        raise
    count = get_num_of_files(path_to_color)
    sens_file.write(struct.pack("Q", count))

    #RGBD data
    color_frames = os.listdir(path_to_color)
    for i in range(count):
        color_frame = os.path.join(path_to_color,color_frames[i])
        depth_frame =  os.path.join(path_to_depth,color_frames[i])
        depth_frame = depth_frame.strip(".jpg") + ".png"
        pose = os.path.join(path_to_pose,color_frames[i])
        pose = pose.strip(".jpg") + ".txt"
        print(color_frame)
        print(depth_frame)
        print(pose)
        print("Frame number:",i+1)
        send_RGBD_frame(color_frame,depth_frame,pose,sens_file)



if __name__ == '__main__':
    main()
