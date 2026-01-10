import bpy
import re

armature = bpy.context.active_object
previous_mode = armature.mode

# Check if current selected object is an armature
if not armature or armature.type != 'ARMATURE':
    raise TypeError("Active object is not an armature.")

# Switch to edit mode
bpy.ops.object.mode_set(mode='EDIT')

def delete_useless_bones(armature):
    # TODO - Optimize regex
    pattern = re.compile(r'Sp_(Hi|So)_.*0_[RL]_01|Sp_He_Ear0_[RL]_02|Sp_Ch_Collar0_[RL]_01|Sp_He_Hair2_[RL]_04|Sp_Hi_CSkirt[01]_([RL]|[FB][RL]|[FB][RL][RL])_0[12]|_Handle$|^Wrist_[RL]_')
    dont_delete = ['Sp_Hi_CSkirt0_FLL_01', 'Sp_Hi_CSkirt0_FRR_01']
    
    edit_bones = armature.data.edit_bones
    bones_to_delete = [bone for bone in edit_bones if bone.name not in dont_delete and pattern.search(bone.name)]
    
    for bone in bones_to_delete:
        edit_bones.remove(bone)
    
    print(f'Deleted {len(bones_to_delete)} bones')

def correct_bone_names(armature):
    pass # TODO - Implement this function

def correct_finger_bone_rotation(armature):
    pass # TODO - Implement this function

def hide_face_bones(armature):
    pattern = re.compile('Eye_|Eyebrow_|Mouth_|Tooth_')
    
    # Hide in edit mode
    for bone in armature.data.edit_bones:
        if pattern.search(bone.name):
            bone.hide = True
    
    bpy.ops.object.mode_set(mode='POSE')
    # Hide in pose/object mode
    for bone in armature.data.bones:
        if pattern.search(bone.name):
            armature.data.bones[bone.name].hide = True

def fixIK(armature):
    pass # Add leg IK, foot IK
            

# Start the cleaning process
delete_useless_bones(armature)
hide_face_bones(armature)
fixIK(armature)
correct_bone_names(armature)
correct_finger_bone_rotation(armature)

# Restore previous mode
bpy.ops.object.mode_set(mode=previous_mode)