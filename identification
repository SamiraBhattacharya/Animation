
def analyze_animation():
    armature = bpy.data.objects.get('BAZeel') 
    if not armature:
        print("Armature not found")
        return

    for joint_name in BASE_JOINT_NAMES:
        bone = armature.pose.bones.get(joint_name)
        if bone:
            # Check rotation mode (FK)
            if bone.rotation_mode == 'QUATERNION':
                print(f"{joint_name} uses FK")
            # Check location (IK)
            elif any(loc != 0.0 for loc in bone.location):
                print(f"{joint_name} uses IK")

# Example usage:
analyze_animation()
