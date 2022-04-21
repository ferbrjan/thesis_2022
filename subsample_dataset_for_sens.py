import os
import shutil

def main():
    files = os.listdir("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/color")
    cnt = 0
    for file in files:
        cnt += 1
        if cnt % 4 == 0:
            file_path_src = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/color",file)
            file_path_dst = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/subsampled/color",file)
            print(file_path_dst)
            print(file_path_src)
            shutil.copyfile(file_path_src,file_path_dst)
            file_num = file.strip(".jpg")
            file_depth = file_num + ".png"
            file_path_src = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/depth", file_depth)
            file_path_dst = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/subsampled/depth", file_depth)
            print(file_path_dst)
            print(file_path_src)
            shutil.copyfile(file_path_src, file_path_dst)
            file_pose = file_num + ".txt"
            file_path_src = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/pose", file_pose)
            file_path_dst = os.path.join("/Users/ferbrjan/Documents/SPSG-dataset_hl/recording02/subsampled/pose", file_pose)
            print(file_path_dst)
            print(file_path_src)
            shutil.copyfile(file_path_src, file_path_dst)


    print("ready")

if __name__ == '__main__':
    main()