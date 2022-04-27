from .operators.load_unreal_pbr_material import register as register_open_files
from .operators.load_unreal_pbr_material import unregister as unregister_open_files
from .panel.ui_panel import register as register_panel
from .panel.ui_panel import unregister as unregister_panel

bl_info = {
    "name": "PBR Material Unreal Format",
    "blender": (3, 1, 0),
    "category": "Material",
}


def register():
    register_open_files()
    register_panel()


def unregister():
    unregister_open_files()
    unregister_panel()
