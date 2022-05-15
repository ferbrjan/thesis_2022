# thesis_2022

This repository contains multiple scripts that were used for Bachelor thesis of Ferbr Jan in 2022.

align_holo2colmap.m script works, but needs to be edited if it is desired to be used on your data. Firstly the path to COLMAP reconstruction needs to be set (line 4) and the path to hololens2 poses needs to be set as well (line 8). Lastly the correct mesh for aligning needs to be loaded (line 55).

align_scene_to_main_axis cript also needs some editing if required to use for your data. Firstly the data for the correct mesh need to be loaded (line 5). Secondly the correct vecot neeeds to be set upt according to previous axis orientation of the original mesh (line 9). Line 34 needs to adress the correct COLMAP database to be transformed into the new coordinate system.

compresser.py can be run on any dataset that is split into 4 directories: color,depth,pose,intrinsics. color contains rgb images, depth contains corresponding depth images, pose contains corresponding transformation matrixes for each rames and intrinsics contains rgb + depth camera intrinsics + extrinsics. The --input_path and --output_path arguments are required! (input_path specifying directory with 4 subdirectories mentioned above, output_path specifiyng the output destination)

generate_dataset.py is a script that needs to be inputed into a already existing project. Please first install https://gitlab.com/ssteidl/habitat-ros according to instruction, and the paste this script into habitat-ros/spring_simulation folder. Please be sure that you already used obj2glb.py and point to correct data path on line 156. Also it is adviced to create your own scene as in lines 30-42 and 108-131. In configs/tasks/pointnav.yaml change the parameters for each sensor as required.

ob2glb.py needs to be edited on line 6 to point to the correct path with .json and .obj files. The folder that line 6 reffers to need to be structured as: folder -> categories_subfolders {chair, table, ...} -> nameofcategory_obj, {corresponding .object_config.json files for each object in _obj folder} -> .obj files for each object. Image can be found below:

<img width="333" alt="Snímek obrazovky 2022-05-15 v 16 32 05" src="https://user-images.githubusercontent.com/74875970/168478195-973ab842-d08a-4f2c-836a-f9930b43a387.png">

To use remove_blurry.py and rotate_every_xth.py please use -h / --help to read about all the required arguments and their meaning. If needed the blur threshold can be changed on line 5 in remove_blurry.py

subsample_dataset.py requires changing multiple lines in order to be used. Firstly, the files identifier on line 5, needs to point to directory structured the same as for compresser.py. In this directory a subsampled subdirectory needs to be created, and there the subsampled data will be transfered. Only specify the paths on lines 10,11,17,18,23 and 24. Moreover please copy the intrinsics folder from the original dataset into the subsampled datset to ensure completeness of the data.



