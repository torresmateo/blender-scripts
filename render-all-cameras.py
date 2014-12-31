import bpy
import os
import sys
from stat import *
import bpy

bl_info = {
    "name": "Render All Cameras",
    "description": "This script renders scene from all cameras and stores result to the .blend folder",
    "author": "Mateo Torres <torresmateo@gmail.com>",
    "version": (1, 0),
    "blender": (2, 72, 0),
    "location": "Toolshelf",
    "warning": "", # used for warning icon and text in addons panel
    "category": "Render"}



#----------------------------------------- Create panel in the toolshelf -------------------------------------------------

class CreateRenderAllCamerasPanel(bpy.types.Panel):
    bl_label = "Render All Cameras"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Render"

    def draw(self, context):
        
        # column buttons solution. Less space than single buttons ...
        layout = self.layout
        view = context.space_data
        # Three buttons
        col = layout.column(align=True)
        col.operator("scene.render_all_cameras", text="Render All Cameras")
# -------------------------------------------------------------------------------------------


class RenderAllCameras(bpy.types.Operator):
  """Render All Cameras"""
  bl_idname = "scene.render_all_cameras"
  bl_label = "Render All Cameras"
  bl_options = {'REGISTER', 'UNDO'}
 
  def execute(self, context):
    scene = bpy.context.scene
    for ob in scene.objects:
      if ob.type == 'CAMERA':
        bpy.context.scene.camera = ob
        print('Set camera %s' % ob.name )
        file = os.path.join(os.path.dirname(bpy.data.filepath), ob.name )
        bpy.context.scene.render.filepath = file
        bpy.ops.render.render( write_still=True )
    return {'FINISHED'}


# store keymaps here to access after registration
addon_keymaps = []
   

def register():
    bpy.utils.register_class(CreateRenderAllCamerasPanel)
    bpy.utils.register_class(RenderAllCameras)

      # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    kmi = km.keymap_items.new(RenderAllCameras.bl_idname, 'ONE', 'PRESS', ctrl=True, shift=True, alt=True)
    
    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(CreateRenderAllCamerasPanel)
    bpy.utils.unregister_class(RenderAllCameras)

      # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()
            
            
            