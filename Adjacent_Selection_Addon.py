23bl_info = {
    "name": "Adjacent Selection",
    "author": "Sergey Golubev",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Select > Select Linked",
    "description": "Select components adjacent to current selection.",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
}

### MAIN PART OF ADDON STARTS HERE

import bpy

def adj_verts_sel():  # Selecting adjacent vertices

    bpy.context.active_object.update_from_editmode()      
    start_sel = [v.index for v in bpy.context.active_object.data.vertices if v.select] # store indexes of selected components
    
    bpy.ops.mesh.select_more(use_face_step=False)   # select more
    bpy.context.active_object.update_from_editmode()
    new_sel = [v.index for v in bpy.context.active_object.data.vertices if v.select] # store indexes of new (bigger) selection

    adj_sel = [v for v in new_sel if v not in start_sel] # remove smaller (first) selection from bigger (after Select More)
    bpy.ops.mesh.select_all(action='DESELECT') # deselect all components
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for v in adj_sel:                          # select new components
        bpy.context.active_object.data.vertices[v].select = True 
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.context.tool_settings.mesh_select_mode[0] = True  # activate vertex selection mode
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT') # switch to vertex selection mode

def adj_edges_sel():  # Selecting adjacent edges
    bpy.context.active_object.update_from_editmode()
    start_sel = [v.index for v in bpy.context.active_object.data.edges if v.select] # store indexes of selected components
    
    bpy.ops.mesh.select_more(use_face_step=False)   # select more
    bpy.context.active_object.update_from_editmode()
    new_sel = [v.index for v in bpy.context.active_object.data.edges if v.select] # store indexes of new (bigger) selection

    adj_sel = [v for v in new_sel if v not in start_sel] # remove smaller (first) selection from bigger (after Select More)
    bpy.ops.mesh.select_all(action='DESELECT') # deselect all components
    bpy.ops.object.mode_set(mode = 'OBJECT')   
    for v in adj_sel:                          # select new components
        bpy.context.active_object.data.edges[v].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 
    bpy.context.tool_settings.mesh_select_mode[1] = True # activate edges selection mode
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE') # switch to edge selection mode

def adj_faces_sel():  # Selecting adjacent polygons
    bpy.context.active_object.update_from_editmode()
    if len([v for v in bpy.context.active_object.data.polygons if v.select]) > 0: # if at least 1 polygon selected
        bpy.context.active_object.update_from_editmode()
        start_sel = [v.index for v in bpy.context.active_object.data.polygons if v.select] # store indexes of selected components
    
        bpy.ops.mesh.select_more(use_face_step=False)   # select more
        bpy.context.active_object.update_from_editmode()
        new_sel = [v.index for v in bpy.context.active_object.data.polygons if v.select] # store indexes of new (bigger) selection

        adj_sel = [v for v in new_sel if v not in start_sel] # remove smaller (first) selection from bigger (after Select More)
        bpy.ops.mesh.select_all(action='DESELECT') # deselect all components
        bpy.ops.object.mode_set(mode = 'OBJECT')
        for v in adj_sel:                          # select new components
            bpy.context.active_object.data.polygons[v].select = True 
        bpy.ops.object.mode_set(mode = 'EDIT')
    else:      # if no polygons selected          
        bpy.context.active_object.update_from_editmode()
        start_sel = [v.index for v in bpy.context.active_object.data.polygons if v.select] # store indexes of selected components
    
        bpy.ops.mesh.select_more()   # select more
        bpy.context.active_object.update_from_editmode()
        new_sel = [v.index for v in bpy.context.active_object.data.polygons if v.select] # store indexes of new (bigger) selection
 
        adj_sel = [v for v in new_sel if v not in start_sel] # remove smaller (first) selection from bigger (after Select More)
        bpy.ops.mesh.select_all(action='DESELECT') # deselect all components
        bpy.ops.object.mode_set(mode = 'OBJECT')
        for v in adj_sel:                          # select new components
            bpy.context.active_object.data.polygons[v].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode[2] = True # activate polygons selection mode
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE') # switch to polygons selection mode
    
### MAIN PART OF ADDON ENDS HERE


### ADDON AND INTERFACE PART STARTS HERE

class OBJECT_OT_adj_verices(bpy.types.Operator):
    """Select vertices adjacent to current selection."""
    bl_label = "Adjacent vertices"
    bl_idname = "mesh.adj_verices"
    bp_options = {'REGISTER' , "UNDO"}
    
    def execute(self, context):
        
        adj_verts_sel()
        return {'FINISHED'}

class OBJECT_OT_adj_edges(bpy.types.Operator):
    """Select edges adjacent to current selection."""
    bl_label = "Adjacent edges"
    bl_idname = "mesh.adj_edges"
    bp_options = {'REGISTER' , "UNDO"}
    
    def execute(self, context):
        
        adj_edges_sel()
        return {'FINISHED'}
    
class OBJECT_OT_adj_faces(bpy.types.Operator):
    """Select polygons adjacent to current selection."""
    bl_label = "Adjacent polygons"
    bl_idname = "mesh.adj_polygons"
    bp_options = {'REGISTER' , "UNDO"}
    
    def execute(self, context):
        
        adj_faces_sel()
        return {'FINISHED'}



def adjacent_verts_button_components(self , context): # add separator button in components delete menu
    self.layout.separator()
    self.layout.operator(
            OBJECT_OT_adj_verices.bl_idname
            )
            
def adjacent_edges_button_components(self , context): # add separator button in components delete menu
    self.layout.operator(
            OBJECT_OT_adj_edges.bl_idname
            )
            
def adjacent_faces_button_components(self , context): # add separator button in components delete menu
    self.layout.operator(
            OBJECT_OT_adj_faces.bl_idname
            )




# Registration

def register():
    bpy.utils.register_class(OBJECT_OT_adj_verices)
    bpy.utils.register_class(OBJECT_OT_adj_edges)
    bpy.utils.register_class(OBJECT_OT_adj_faces)
    bpy.types.VIEW3D_MT_edit_mesh_select_linked.append(adjacent_verts_button_components)
    bpy.types.VIEW3D_MT_edit_mesh_select_linked.append(adjacent_edges_button_components)
    bpy.types.VIEW3D_MT_edit_mesh_select_linked.append(adjacent_faces_button_components)




def unregister():
    bpy.utils.unregister_class(OBJECT_OT_adj_verices)
    bpy.utils.unregister_class(OBJECT_OT_adj_edges)
    bpy.utils.unregister_class(OBJECT_OT_adj_faces)
    bpy.types.VIEW3D_MT_edit_mesh_select_linked.remove(adjacent_verts_button_components)
    bpy.types.VIEW3D_MT_edit_mesh_select_linked.remove(adjacent_edges_button_components)
    bpy.types.VIEW3D_MT_edit_mesh_select_linked.remove(adjacent_faces_button_components)



if __name__ == "__main__":
    register()

#VIEW3D_MT_edit_mesh_select_linked
### ADDON AND INTERFACE PART ENDS HERE
