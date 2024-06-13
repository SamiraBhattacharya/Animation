import bpy

def delete_keyframes_outside_range(obj, start_time, end_time):
    # Select the armature object
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='POSE')

    # Iterate over all bones
    for bone in obj.pose.bones:
        # Select all keyframes for the current bone
        bpy.ops.pose.select_all(action='SELECT')
        
        # Filter keyframes outside the specified range
        for fc in bone.animation_data.action.fcurves:
            for keyframe in fc.keyframe_points:
                if keyframe.co[0] < start_time or keyframe.co[0] > end_time:
                    keyframe.select_control_point = True
                else:
                    keyframe.select_control_point = False
        
        # Delete selected keyframes
        bpy.ops.pose.delete(type='KEYFRAME')

    # Switch back to Object mode
    bpy.ops.object.mode_set(mode='OBJECT')

def align_keyframes_to_start(obj):
    # Select the armature object
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='POSE')

    # Deselect all keyframes
    bpy.ops.pose.select_all(action='DESELECT')

    # Select all keyframes
    bpy.ops.pose.select_all(action='SELECT')

    # Set the start time (0th second)
    bpy.ops.pose.transforms_clear()

    # Switch back to Object mode
    bpy.ops.object.mode_set(mode='OBJECT')

def main():
    # Check if the armature named "BAZeel" is present
    armature_name = "BAZeel"
    obj = bpy.data.objects.get(armature_name)
    if not obj:
        print(f"Armature '{armature_name}' not found in the scene.")
        return
    
    # Get start and end time from user input
    start_time = float(input("Enter start time (seconds): "))
    end_time = float(input("Enter end time (seconds): "))

    # Delete keyframes outside the specified range
    delete_keyframes_outside_range(obj, start_time, end_time)

    # Align remaining keyframes to the start (0th second) of the timeline
    align_keyframes_to_start(obj)

    # Execute functions from the add-on
    bpy.ops.azee_animator.create_posture_button()
    bpy.ops.azee_animator.config_popup()
    bpy.ops.azee_animator.save_to_npy()

if __name__ == "__main__":
    main()

