import bpy

from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement

import re

from ..lib.material_creator_helper import MaterialCreatorHelper

p = re.compile('.*(Roughness|Occlusion|Metallic).*(Roughness|Occlusion|Metallic).*(Roughness|Occlusion|Metallic).*')


class OT_CreateMaterialFromPBRTextureSet(Operator, ImportHelper):
    bl_info = {
        "name": "My Test Add-on",
        "blender": (3, 1, 0),
        "category": "Object",
    }
    bl_idname = "rom_unreal_pbr.make_pbr_material"
    bl_label = "Make Material"

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
    )

    filter_glob: StringProperty(
        default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp',
        options={'HIDDEN'}
    )

    some_boolean: BoolProperty(
        name='Do a thing',
        description='Do a thing with the file you\'ve selected',
        default=True,
    )

    def __init__(self):
        self.material_name = None
        self.helper = MaterialCreatorHelper()

    def _create_material(self):
        self.material = bpy.data.materials.new(name=self.material_name)  # set new material to variable
        self.material.use_nodes = True

    def _load_images(self):
        texture_files = self.helper.get_texture_files()
        self.base_color_texture = bpy.data.images.load(filepath=texture_files.base_color.complete_file_path,
                                                       check_existing=True)
        self.orm_texture = bpy.data.images.load(filepath=texture_files.occlusion.complete_file_path,
                                                check_existing=True)
        self.normal_texture = bpy.data.images.load(filepath=texture_files.normal.complete_file_path,
                                                   check_existing=True)

    def _setup_nodes(self):
        def reposition_nodes():
            print("reposition_nodes")
            base_color_image_node.location = -500, 400
            orm_image_node.location = -1000, 0
            separate_rgb_node.location = -400, 0
            normal_image_node.location = -1000, -400
            separate_xyz_node.location = -700, -400
            math_node.location = -500, -400
            combine_xyz_node.location = -300, -400
            normal_map_node.location = -100, -400

        material = self.material
        print("got the material")

        nodes = material.node_tree.nodes
        node_principled = nodes.get('Principled BSDF')
        base_color_image_node = material.node_tree.nodes.new('ShaderNodeTexImage')
        normal_image_node = material.node_tree.nodes.new('ShaderNodeTexImage')

        print("created simpler nodes")
        separate_xyz_node = material.node_tree.nodes.new(type='ShaderNodeSeparateXYZ')
        print("created separate xyz node")
        combine_xyz_node = material.node_tree.nodes.new(type='ShaderNodeCombineXYZ')
        print("created combine xyz node")

        math_node = material.node_tree.nodes.new(type='ShaderNodeMath')
        print("created Math xyz node")
        math_node.operation = 'SUBTRACT'
        math_node.inputs[0].default_value = 1.0
        print("set up math node correctly")

        # create normal map node
        normal_map_node = material.node_tree.nodes.new(type='ShaderNodeNormalMap')

        orm_image_node = material.node_tree.nodes.new('ShaderNodeTexImage')
        separate_rgb_node = material.node_tree.nodes.new('ShaderNodeSeparateRGB')
        print("created Occlusion Roughness Metallic nodes")

        base_color_image_node.image = self.base_color_texture
        normal_image_node.image = self.normal_texture
        orm_image_node.image = self.orm_texture

        normal_image_node.image.colorspace_settings.name = 'Non-Color'
        orm_image_node.image.colorspace_settings.name = 'Non-Color'
        print("set up images")

        links = material.node_tree.links
        print("creating links")
        links.new(base_color_image_node.outputs["Color"], node_principled.inputs["Base Color"])
        links.new(orm_image_node.outputs["Color"], separate_rgb_node.inputs["Image"])
        links.new(separate_rgb_node.outputs["G"], node_principled.inputs["Roughness"])
        links.new(separate_rgb_node.outputs["B"], node_principled.inputs["Metallic"])
        links.new(normal_image_node.outputs["Color"], separate_xyz_node.inputs["Vector"])
        print("created basic links")

        links.new(separate_xyz_node.outputs["X"], combine_xyz_node.inputs["X"])
        links.new(separate_xyz_node.outputs["Z"], combine_xyz_node.inputs["Z"])
        links.new(separate_xyz_node.outputs["Y"], math_node.inputs[1])
        links.new(math_node.outputs[0], combine_xyz_node.inputs["Y"])
        links.new(combine_xyz_node.outputs["Vector"], node_principled.inputs["Normal"])
        links.new(combine_xyz_node.outputs["Vector"], normal_map_node.inputs["Color"])
        links.new(normal_map_node.outputs["Normal"], node_principled.inputs["Normal"])

        reposition_nodes()

    def execute(self, context):
        """Do something with the selected file(s)."""
        import os
        directory = self.directory
        for file_elem in self.files:
            complete_file_path = os.path.join(directory, file_elem.name)
            file_name = file_elem.name
            self.helper.add_file(file_name, complete_file_path)

        self.material_name = self.helper.get_material_name()

        if not self.helper.is_complete:
            return {'FINISHED'}

        self._create_material()
        self._load_images()
        self._setup_nodes()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_CreateMaterialFromPBRTextureSet)


def unregister():
    bpy.utils.unregister_class(OT_CreateMaterialFromPBRTextureSet)


# if __name__ == "__main__":
#     register()
#
#     # test call
#     bpy.ops.rom.make_pbr_material('INVOKE_DEFAULT')
