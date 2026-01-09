import bpy
import re

obj = bpy.context.active_object
previous_mode = obj.mode # Store current edit more so we can restore it later

# Check if current selected object is an armature
if not obj or obj.type != 'ARMATURE':
    raise TypeError("Active object is not an armature.")

# Switch to edit mode
bpy.ops.object.mode_set(mode='EDIT')

def delete_useless_bones(obj):
    case_insensitive_pattern = re.compile('_handle', re.IGNORECASE)
    # case_sensitive_pattern = re.compile('')
    
    edit_bones = obj.data.edit_bones
    bones_to_delete = [bone for bone in edit_bones if case_insensitive_pattern.search(bone.name)]
    
    for bone in bones_to_delete:
        edit_bones.remove(bone)
    
    print(f'Deleted {len(bones_to_delete)} bones')

def correct_bone_names(obj):
    pass # TODO - Implement this function

def correct_finger_bone_rotation(obj):
    pass # TODO - Implement this function

def hide_face_bones(obj):
    pass # TODO - Hide face bones because they're all too detailed

# Start the cleaning process
delete_useless_bones(obj)
correct_bone_names(obj)
correct_finger_bone_rotation(obj)
hide_face_bones(obj)

# Restore previous mode
bpy.ops.object.mode_set(mode=previous_mode)