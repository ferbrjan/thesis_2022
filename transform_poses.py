import os.path

from scipy.spatial.transform import Rotation as R
import argparse
import numpy as np

# params
parser = argparse.ArgumentParser()
# data paths
parser.add_argument('--input_path', required=True, help='path to file to read')
parser.add_argument('--output_path', required=True, help='path to output directory')

opt = parser.parse_args()
print(opt)

def main():
    poses = open(opt.input_path,"r")
    lines = poses.readlines()
    for i in range (len(lines)):
        line=lines[i].split()
        print(line)
        Qw,Qx,Qy,Qz = line[1],line[2],line[3],line[4]
        Tx,Ty,Tz = line[5],line[6],line[7]

        r = R.from_quat([float(Qw),float(Qx),float(Qy),float(Qz)])
        rot_mat = r.as_matrix()
        trans_mat = np.eye(4)
        for row in range (3):
            for col in range (3):
                trans_mat[row][col]=rot_mat[row][col]
        trans_mat[0][3] = Tx
        trans_mat[1][3] = Ty
        trans_mat[2][3] = Tz
        name = line[9].strip("\\")
        number = name[-8:]
        pure_number = number.strip(".png")
        print(pure_number)
        path = os.path.join(opt.output_path,pure_number) + ".txt"
        print(path)
        pose = open(path,"w")
        pose.write(str(trans_mat).replace(' [', '').replace('[', '').replace(']', ''))



if __name__ == '__main__':
    main()