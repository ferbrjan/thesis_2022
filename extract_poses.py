import os.path

from scipy.spatial.transform import Rotation as R
import argparse
import numpy as np

def main():
    files = os.listdir("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/color")
    colmap_data = open("/Users/ferbrjan/Downloads/colmap_sparse_rotated/images.txt")
    cnt=-3
    poses=[] #only poses for kinect recording03
    for line in colmap_data:
        cnt += 1
        if cnt > 0 and cnt % 2 == 0:
            poses.append(line.split())
            if poses[len(poses)-1][9].startswith("kinect/recording02"):
                print(poses[len(poses)-1][9])
            else:
                poses.pop()
    print(len(poses))
    print(poses)

    for file in files:
        found=0
        if int(file.strip(".png"))<9:
            file_name = "000"+file
        elif int(file.strip(".png"))<99:
            file_name = "00"+file
        elif int(file.strip(".png"))<999:
            file_name = "0"+file
        else:
            file_name = file
        #print(file_name)
        for i in range (len(poses)):
            if poses[i][9].endswith(file_name):
                Qw, Qx, Qy, Qz = poses[i][1], poses[i][2], poses[i][3], poses[i][4]
                Tx, Ty, Tz = poses[i][5], poses[i][6], poses[i][7]
                #print(Qw, Qx, Qy, Qz)

                r = R.from_quat([float(Qx), float(Qy), float(Qz), float(Qw)])
                rot_mat = r.as_matrix()
                #print(file)
                #print(rot_mat)
                trans_mat = np.eye(4)
                for row in range(3):
                    for col in range(3):
                        trans_mat[row][col] = rot_mat[row][col]
                trans_mat[0][3] = Tx
                trans_mat[1][3] = Ty
                trans_mat[2][3] = Tz
                #print("found for file",file)
                #print(trans_mat)
                trans_mat=np.linalg.inv(trans_mat)
                #print(trans_mat)
                number = file[-8:]
                pure_number = number.strip(".png")
                pure_number = int(pure_number)
                pure_number = str(pure_number)
                #print(pure_number)
                path = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/pose",str(pure_number + ".txt"))
                pose = open(path, "w")
                pose.write(str(trans_mat).replace(' [', '').replace('[', '').replace(']', ''))
                found=1
            if found == 1:
                break
            if i==(len(poses)-1) and found==0:
                print(file)
        """
        file_number = file[-8:].strip(".png")
        file_number = int(file_number)
        file_number = str(file_number)
        file_new_name = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/color", str(file_number + ".png"))
        print(file_new_name)
        os.rename(str("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/color/" + file),file_new_name)
        """
if __name__ == '__main__':
    main()
