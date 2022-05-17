import pymeshlab
import os
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Program for merging all meshes in a directory')
    parser.add_argument("-i", "--input_directory", help="include path to directory to be processed")
    parser.add_argument("-o", "--output_directory", help="include path for the output directory where merged_mesh.ply will be saved \n\n -if empty, merged_mesh.ply will be saved in the same directory as merge_mesh.py")

    args = parser.parse_args()
    print(args.input_directory)
    print(args.output_directory)


    ms = pymeshlab.MeshSet()

    path = args.input_directory #"/Users/ferbrjan/Downloads/HoloLens2/2021-10-06-082512/Depth_Long_Throw"
    dir = os.listdir(path)
    i=0
    for file in dir:
        #print(file)
        if file.endswith(".ply"):
            i+=1
            file_path = path + "/" + file
            #print(file_path)
            ms.load_new_mesh(file_path)
            print(i)

    ms.flatten_visible_layers(mergevisible=False)
    output_path = args.output_directory + "/merged_mesh.ply"
    ms.save_current_mesh(output_path)

