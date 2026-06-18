# By summerwya, https://github.com/summerwya/umamusume-game-ripped-model-fixer

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
    
        r'Sp_(Hi|So)_.*0_[RL]_01',
        r'Sp_He_Ear0_[RL]_02',
        r'Sp_Ch_Collar0_[RL]_01',
    
        r'^Sp_He_Acc0_[RL]_01$',
        r'_Handle$',
        r'^Wrist_[RL]_',
        r'^M_Line',
        r'Sp_Ch_Collor_[RL]_01',
        r'_attach(_[RL])?$',
        r'_Attach(_[RL])?$',
        r'^Sp_He_Ear0_[RL]_01$',
        
        # Taken from GoldShip
        r'MSkirt0_[RL]_02$',
        r'MSkirt0_[BF][RL]_02$',
        r'MSkirt0_[BF][RL][RL]_02$',
        r'MSkirt0_[BF]_02$',
        r'MSkirt0_BR_02$',

        # Bones that deform but unnecessary
        r'^Eyelashes_[LR]$',
        r'^Eye.*',
        r'^Cheek_[RL]$',
        r'^Cheek_offset.*',
        r'^Mouth_',
        r'^Tooth_',
    ]))
    dont_hide_these = list(map(re.compile, [
        r'.*CSkirt\d_[RL]_\d+$',
        r'Sp_He_Hair2_[RL]_01$',
        r'^Eye_[RL]$',
        r'.*MSkirt\d_[BF][RL]_0[12]$',
        r'.*MSkirt\d_[BF][RL][RL]_0[12]$',
        r'.*Belt\d_[RL]_0[12]$',
#        r'.*Hair4_[CRL]'
    ]))
    override_hide = list(map(re.compile, [
        
    ]))
    
    bpy.ops.object.mode_set(mode='POSE')
    for bone in armature.data.bones:
        if any(r.search(bone.name) for r in dont_hide_these) and not any(r.search(bone.name) for r in override_hide):
            continue
        
        if any(pattern.search(bone.name) for pattern in hide_these):
            bone.hide = True
            print(f'Hidden {bone.name}')

def hide_extra_eyebrows(armature):
    for child in armature.children:
        if not child.name.endswith('_mesh'):
            continue
        print('Hiding extra eyebrows')
        
        keys = child.data.shape_keys.key_blocks
        
        name_R = 'EyeBrow_23_R(Offset_L)[M_Mayu]'
        name_L = 'EyeBrow_24_L(Offset_R)[M_Mayu]'
        
        keys[name_R].value = keys[name_R].slider_max
        keys[name_L].value = keys[name_L].slider_max
        return
    
    print('Mesh not found')

# Start the cleaning process
print('Started')
hide_useless_bones(armature)
try:
    hide_extra_eyebrows(armature)
except Exception:
    pass

# Restore previous mode
bpy.ops.object.mode_set(mode=previous_mode)
