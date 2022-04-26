import bpy


class VIEW3D_PT_load_unreal_pbr_material(bpy.types.Panel):
    bl_label = 'Unreal PBR Material'
    bl_region_type = 'UI'
    bl_category = 'Unreal PBR Material'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        self.layout.operator('rom_unreal_pbr.make_pbr_material')


def register():
    bpy.utils.register_class(VIEW3D_PT_load_unreal_pbr_material)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_load_unreal_pbr_material)


if __name__ == "__main__":
    register()
