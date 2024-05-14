
#  Data extraction from .fbx to .npy 
import bpy
import os
import time
import sys
import json
from mathutils import Vector
import numpy as np 



BASE_JOINT_NAMES = ['Spine1.001, Spine2.001, Neck.001, Head.001, LeftShoulder.001, LeftArm.001, LeftForeArm.001, LeftHand.001, LeftHandThumb1.001, LeftHandThumb2.001, LeftHandThumb3.001, LeftHandIndex1.001, LeftHandIndex2.001, LeftHandIndex3.001, LeftHandMiddle1.001, LeftHandMiddle2.001, LeftHandMiddle3.001, LeftHandRing1.001, LeftHandRing2.001, LeftHandRing3.001, LeftHandPinky1.001, LeftHandPinky2.001, LeftHandPinky3.001, RightShoulder.001, RightArm.001, RightForeArm.001, RightHand.001, RightHandThumb1.001, RightHandThumb2.001, RightHandThumb3.001, RightHandIndex1.001, RightHandIndex2.001, RightHandIndex3.001, RightHandMiddle1.001, RightHandMiddle2.001, RightHandMiddle3.001'
                    ] # names of all fk_controller
#Source directory where .fbx exist
#storing of all the files
SRC_DATA_DIR = '/people/bhattacharya/CNRS/Progress' #where the .fbx file is already stored 
OUT_DATA_DIR = '/people/bhattacharya/CNRS/Progress/fbx2json' #where we will store the json file
FINAL_DIR_PATH = '/people/bhattacharya/CNRS/Progress/json2npy' #where we will store the numpy array

# This function converts blend file to JSON


def blend2json():

    # Iterating over .blend files in the directory
    for filename in os.listdir(SRC_DATA_DIR):
        if filename.endswith('.blend') or filename.endswish('.fbx'):
            blend_file_path = os.path.join(SRC_DATA_DIR, filename)
            save_dir = os.path.join(OUT_DATA_DIR, os.path.splitext(filename)[0])
            
            
            # Loading the .blend file
            bpy.ops.wm.open_mainfile(filepath=blend_file_path)
            
            # Getting the start and end frames of the animation
            start_frame = bpy.context.scene.frame_start
            end_frame = bpy.context.scene.frame_end
            
            # Iterate over frames
            for i in range(start_frame, end_frame + 1):
                bpy.context.scene.frame_set(i)
                bone_struct = bpy.data.objects['Armature'].pose.bones #accesss data ``
                armature = bpy.data.objects['Armature']
                out_dict = {'pose_keypoints_3d': []}
                
                # Iterate over bones
                for name in BASE_JOINT_NAMES:
                    global_location = armature.matrix_world @ bone_struct[name].matrix @ Vector((0, 0, 0))
                    l = [global_location[0], global_location[1], global_location[2]]
                    out_dict['pose_keypoints_3d'].extend(l)
                
                # JSON dictionary to file
                save_path = os.path.join(save_dir, f'{i:04d}_keypoints.json')
                with open(save_path, 'w') as f:
                    json.dump(out_dict, f)


blend2json()

# This converts JSON to NPY 
def jointDict2npy():
    json_dir = OUT_DATA_DIR
    npy_dir = FINAL_DIR_PATH
    
    if not os.path.exists(npy_dir):
        os.makedirs(npy_dir)
    
    for anim_name in os.listdir(json_dir):
        files_path = os.path.join(json_dir, anim_name, 'JointDict')
        frame_files = [f for f in os.listdir(files_path) if f.endswith('.json')]
        motion = []
        
        for frame_file in frame_files:
            file_path = os.path.join(files_path, frame_file)
            
            with open(file_path) as f:
                info = json.load(f)
                joint = np.array(info['pose_keypoints_3d']).reshape((-1, 3))
                motion.append(joint[:, :])  
        
        motion = np.stack(motion, axis=2)
        save_path = os.path.join(npy_dir, anim_name)
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        np.save(save_path + '.npy', motion)

jointDict2npy()

