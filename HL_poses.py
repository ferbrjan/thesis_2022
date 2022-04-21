import os
import argparse
import open3d as o3d
import numpy as np

# params
parser = argparse.ArgumentParser()
# data paths
parser.add_argument('--input_path', required=True, help='path to directory to read')

opt = parser.parse_args()
print(opt)

def main():
    inv_trajectory = o3d.io.read_pinhole_camera_trajectory(str(opt.input_path + "/odometry.log"))
    rgb_file_list = str(opt.input_path + "/rgb.txt")

    with open(str(rgb_file_list)) as rf:
        i = 0
        while True:
            rgb_line = rf.readline()
            if not rgb_line:
                break
            pose = inv_trajectory.parameters[i].extrinsic
            rgb_name = rgb_line.split()[1]
            rgb_name = rgb_name[4:].strip(".png")
            pose_path = opt.input_path + "/pose/" + rgb_name + ".txt"
            print(pose)
            print(rgb_name)
            pose_file = open(pose_path, "w")
            pose_file.write(str(pose).replace(' [', '').replace('[', '').replace(']', ''))
            i += 1
    """
    with open(str(rgb_file_list)) as rf:
        rgb_line = rf.readline()
    rgb_path = str(opt.input_path + "/" + rgb_line.split()[1])
    color = o3d.io.read_image(rgb_path)
    rgb_np = np.asarray(color)
    intrinsic_path = str(opt.input_path + "/calibration.txt")
    intrinsic_np = np.loadtxt(str(intrinsic_path))
    print(rgb_np.shape[1], rgb_np.shape[0])
    intrinsic = o3d.camera.PinholeCameraIntrinsic(
        rgb_np.shape[1], rgb_np.shape[0],
        intrinsic_np[0], intrinsic_np[1],
        intrinsic_np[2], intrinsic_np[3])
    print(intrinsic.intrinsic_matrix)
    intrinsics = intrinsic.intrinsic_matrix
    intrinsics = np.concatenate((intrinsics, [[0, 0, 0]]),axis=0)
    print(intrinsics)
    intrinsics = np.concatenate((intrinsics, np.transpose([[0, 0, 0 ,1]])), axis=1)
    print(intrinsics)
    intrinsic_color = open(str(opt.input_path + "/intrinsic_color.txt"),"w")
    intrinsic_depth = open(str(opt.input_path + "/intrinsic_depth.txt"),"w")
    extrinsic_depth = open(str(opt.input_path + "/extrinsis_depth.txt"),"w")
    extrinsic_color = open(str(opt.input_path + "/extrinsic_color.txt"),"w")
    intrinsic_color.write(str(intrinsics).replace(' [', '').replace('[', '').replace(']', ''))
    intrinsic_depth.write(str(intrinsics).replace(' [', '').replace('[', '').replace(']', ''))
    extrinsic_depth.write(str(np.eye(4)).replace(' [', '').replace('[', '').replace(']', ''))
    extrinsic_color.write(str(np.eye(4)).replace(' [', '').replace('[', '').replace(']', ''))
    """
if __name__ == '__main__':
    main()