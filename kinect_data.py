# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("starting")
    cnt = 1
    for i in range (416, 528601, 200):
        command = f"E:/ferbrjan\Azure-Kinect-Sensor-SDK-develop\Azure-Kinect-Sensor-SDK-develop\examples\save_depth_as_color\Debug/transformation_example.exe playback E:/ferbrjan\B_635-Kinect/recording03\output.mkv {i} E:/ferbrjan\B_635-Kinect/recording03\depth_to_color\{cnt}.png"
        print(command)
        os.system(command)
        cnt += 1


