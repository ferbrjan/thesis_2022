import os
import pymeshlab
#https://www.npmjs.com/package/obj2gltf

#Change here to Living_Lab if needed
orig_path = "data/objects_categorized/HL2COLMAPf"

orig_dirs = os.listdir(orig_path)
for file in orig_dirs:
    if not file.startswith('.'):
        path = orig_path + "/" + file
        print ("PATH IS",path)
        dirs = os.listdir(path)
        for item in dirs:
            print ("ITEM IS:",item)
            if item.endswith("_obj"):
                objects = os.listdir(os.path.join(path,item))
                print(objects)
                for object in objects:
                    if object.endswith(".obj"):
                        final_path = path + "/" + item + "/" + object
                        final_path_glb = path + "/" + object[:-4] + ".glb"
                        final_path_json = path + "/" + object[:-4] + ".object_config.json"
                        print(final_path)
                        print(final_path_glb)
                        print(final_path_json)

                        item_glb = object[:-4] + ".glb"

                        ms = pymeshlab.MeshSet()
                        ms.load_new_mesh(final_path)
                        ms.compute_matrix_from_rotation(rotaxis="X axis",rotcenter="origin",angle=-90)
                        ms.save_current_mesh(final_path)


                        command = "obj2gltf -i " + final_path + " -o " + final_path_glb
                        stream = os.popen('echo Returned output')
                        os.system(command)
                        output = stream.read()
                        output
    
                        f = open(final_path_json, "w")
                        f.write("{")
                        f.write("\n")
                        new_line = "    \"render_asset\": \"" + item_glb + "\""
                        f.write(new_line)
                        f.write("\n")
                        f.write("}")
                        f.close()
                        print("file complete")


