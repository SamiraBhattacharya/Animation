import bpy

def delete_keyframes_outside_range(obj, start_time, end_time):
    # Set the armature object as active and switch to Pose mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='POSE')

    # Select all bones in the armature
    bpy.ops.pose.select_all(action='SELECT')

    # Switch to Object mode to manipulate keyframes
    bpy.ops.object.mode_set(mode='OBJECT')

    # Iterate over all fcurves in the armature's action
    action = obj.animation_data.action
    for fc in action.fcurves:
        # Select keyframes outside the specified range
        for keyframe in fc.keyframe_points:
            if keyframe.co[0] < start_time or keyframe.co[0] > end_time:
                keyframe.select_control_point = True
            else:
                keyframe.select_control_point = False
        
        # Delete selected keyframes
        bpy.ops.anim.keyframe_delete(type='ALL', confirm=False)

def align_keyframes_to_start(obj):
    # Set the armature object as active and switch to Pose mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='POSE')

    # Select all bones in the armature
    bpy.ops.pose.select_all(action='SELECT')

    # Deselect all keyframes
    bpy.ops.pose.select_all(action='DESELECT')

    # Switch to Object mode to manipulate keyframes
    bpy.ops.object.mode_set(mode='OBJECT')

    # Deselect all keyframes
    bpy.ops.graph.select_all_toggle(action='DESELECT')

    # Select all keyframes
    bpy.ops.graph.select_all_toggle(action='SELECT')

    # Move all selected keyframes to the start (frame 0)
    bpy.ops.transform.transform(mode='TIME_TRANSLATE', value=(-bpy.context.scene.frame_current, 0, 0, 0))

    # Switch back to Pose mode
    bpy.ops.object.mode_set(mode='POSE')

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


