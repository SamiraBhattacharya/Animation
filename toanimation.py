
# Steps involved in animatingwith 2 parameters: location & numpy value of the animation

#Step 1: Take the 2 parameters as inputs: numpy array and the location

import bpy
import os
import numpy as np
from mathutils import Quaternion
from mathutils import Vector

# Base joint names (names of all fk_controller)
BASE_JOINT_NAMES = [
    'Spine1.001', 'Spine2.001', 'Neck.001', 'Head.001',
    'LeftShoulder.001', 'LeftArm.001', 'LeftForeArm.001', 'LeftHand.001',
    'LeftHandThumb1.001', 'LeftHandThumb2.001', 'LeftHandThumb3.001',
    'LeftHandIndex1.001', 'LeftHandIndex2.001', 'LeftHandIndex3.001',
    'LeftHandMiddle1.001', 'LeftHandMiddle2.001', 'LeftHandMiddle3.001',
    'LeftHandRing1.001', 'LeftHandRing2.001', 'LeftHandRing3.001',
    'LeftHandPinky1.001', 'LeftHandPinky2.001', 'LeftHandPinky3.001',
    'RightShoulder.001', 'RightArm.001', 'RightForeArm.001', 'RightHand.001',
    'RightHandThumb1.001', 'RightHandThumb2.001', 'RightHandThumb3.001',
    'RightHandIndex1.001', 'RightHandIndex2.001', 'RightHandIndex3.001',
    'RightHandMiddle1.001', 'RightHandMiddle2.001', 'RightHandMiddle3.001'
]



SRC_DATA_DIR = '/CNRS/AZee-anim/json'  


def apply_fk():

    num_joints = len(BASE_JOINT_NAMES)
    num_frames = 250
    joint_rots = np.random.rand(num_frames, num_joints, 4)
    armature = bpy.data.objects.get('BAZeel')  

    if armature:
        # Iterate over frames 
        for frame in range(num_frames):
            bpy.context.scene.frame_set(frame)
        # Iterate over each bone 
            for joint_idx, joint_name in enumerate(BASE_JOINT_NAMES):
                bone = armature.pose.bones.get(joint_name)
                if bone:
                    # Assuming joint_rotations contains quaternions (w, x, y, z)
                    quaternion_rotation = joint_rotations[frame, joint_idx]
                    bone.rotation_quaternion = Quaternion(quaternion_rotation)
                
    else:
        print("Armature not found")

# Call the function to apply FK animations
apply_fk_animations()

#Step 2: Convert the FK to IK by applying the location parameter 

def apply_ik(location):
    armature = bpy.data.objects.get('BAZeel')  
    if not armature:
        print("Armature not found")
        return

    # Iterate over the base joint names
    for joint_name in BASE_JOINT_NAMES:
        bone = armature.pose.bones.get(joint_name)
        if bone:
            # Set the bone's location directly
            bone.location = Vector(location)  

    print("FK to IK conversion complete!")

    
#Step 3: Again convert IK to FK

apply_ik(l)
apply

