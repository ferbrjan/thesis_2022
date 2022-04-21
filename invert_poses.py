import os
import numpy as np


def main():
    poses_inv = os.listdir("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording03/pose_inv")
    print(poses_inv)
    for file in poses_inv:
        print(file)
        path = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording03/pose_inv",file)
        pose_file = open(path,"r")
        T_inv=[[],[],[],[]]
        for i in range(0,4):
            T_inv[i] = pose_file.readline().split()
        T_inv_copy = np.eye(4)
        for i in range(len(T_inv)):
            for j in range(len(T_inv[i])):
                T_inv_copy[i][j]=float(T_inv[i][j])
        print(T_inv_copy)
        T_inv_copy = np.linalg.inv(T_inv_copy)
        path = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording03/pose", file)
        pose = open(path, "w")
        pose.write(str(T_inv_copy).replace(' [', '').replace('[', '').replace(']', ''))

if __name__ == '__main__':
    main()