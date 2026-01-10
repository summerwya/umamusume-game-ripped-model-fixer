import bpy
import re

armature = bpy.context.active_object
previous_mode = armature.mode

# Check if current selected object is an armature
if not armature or armature.type != 'ARMATURE':
    raise TypeError("Active object is not an armature.")

# Switch to edit mode
bpy.ops.object.mode_set(mode='EDIT')

# Hide useless bones in pose mode
def hide_useless_bones(armature):
    # TODO - Optimize regex
    hide_these = list(map(re.compile, [
        r'Sp_He_Hair\d_[RL]_0[12]',
        r'Sp_(Hi|So)_.*0_[RL]_01',
        r'Sp_He_Ear0_[RL]_02',
        r'Sp_Ch_Collar0_[RL]_01',
        r'Sp_He_Hair2_[RL]_04',
        r'^Sp_He_Hair0_C_01$',
        r'^Sp_He_Acc0_[RL]_01$',
        r'_Handle$',
        r'^Wrist_[RL]_',
        r'^M_Line',
        r'Sp_Ch_Collor_[RL]_01',
        r'_attach$',

        # Bones that deform but uncecessary
        r'^Eyelashes_[LR]$',
        r'^Eye.*',
        r'^Cheek_[RL]$',
        r'^Cheek_offset.*',
        r'^Mouth_',
        r'^Tooth_',
    ]))
    dont_hide_these = list(map(re.compile, [
        r'CSkirt\d_[RL]_\d+$',
        r'Sp_He_Hair2_[RL]_01$',
        r'^Eye_[RL]$'
    ]))
    
    bpy.ops.object.mode_set(mode='POSE')
    for bone in armature.data.bones:
        if any(r.search(bone.name) for r in dont_hide_these):
            continue
        
        if any(pattern.search(bone.name) for pattern in hide_these):
            bone.hide = True
            print(f'Hidden {bone.name}')

def correct_bone_names(armature): # TODO - MOST IMPORTANT function, read from CSV file for correct bone names
    # Blender name -> JP, EN
    translation: dict[str, tuple[str, str]] = {}
    for bone in armature.pose.bones:
        if bone.name not in translation:
            continue
        
        mmd_bone = bone.mmd_bone
        mmd_bone.name_j = translation[bone.name][0]
        mmd_bone.name_e = translation[bone.name][1]
        print(f'Renamed {bone.name}')

def correct_finger_bone_rotation(armature):
    pass # TODO - Implement this function

def add_and_fix_IK(armature):
    pass # TODO - Add leg IK, foot IK, and add bones? This is one of the most important parts

def hide_extra_eyebrows(armature):
    all_attributes = dir(armature.pose.bones['Eye_L'])
    for attr in all_attributes:
        print(attr)

# Start the cleaning process
print('Started')
hide_useless_bones(armature)
add_and_fix_IK(armature)
correct_bone_names(armature)
correct_finger_bone_rotation(armature)

# Restore previous mode
bpy.ops.object.mode_set(mode=previous_mode)