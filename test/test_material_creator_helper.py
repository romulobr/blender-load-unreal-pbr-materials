from lib.material_creator_helper import MaterialCreatorHelper

MATERIAL_NAME = "Some_Long_Material_Name"

BASE_COLOR_FILE_PATH = "c:\\Some_Long_Material_Name_BaseColor.png"
BASE_COLOR_FILE_NAME = "Some_Long_Material_Name_BaseColor.png"

NORMAL_FILE_PATH = "c:\\Some_Long_Material_Name_Normal.png"
NORMAL_FILE_NAME = "Some_Long_Material_Name_Normal.png"

ORM_FILE_PATH = "c:\\Some_Long_Material_Name_OcclusionRoughnessMetallic.png"
ORM_FILE_NAME = "Some_Long_Material_Name_OcclusionRoughnessMetallic.png"


def test_is_complete():
    helper = MaterialCreatorHelper()
    helper.add_file(BASE_COLOR_FILE_NAME, BASE_COLOR_FILE_PATH)
    helper.add_file(NORMAL_FILE_NAME, NORMAL_FILE_PATH)
    helper.add_file(ORM_FILE_NAME, ORM_FILE_PATH)

    assert helper.is_complete() is True


def test_is_not_complete_has_nothing():
    helper = MaterialCreatorHelper()
    assert helper.is_complete() is False


def test_is_not_complete_missing_base_color():
    helper = MaterialCreatorHelper()
    helper.add_file(NORMAL_FILE_NAME, NORMAL_FILE_PATH)
    helper.add_file(ORM_FILE_NAME, ORM_FILE_PATH)

    assert helper.is_complete() is False


def test_is_not_complete_missing_occlusion_roughness_metallic():
    helper = MaterialCreatorHelper()
    helper.add_file(BASE_COLOR_FILE_NAME, BASE_COLOR_FILE_PATH)
    helper.add_file(NORMAL_FILE_NAME, NORMAL_FILE_PATH)

    assert helper.is_complete() is False


def test_is_not_complete_missing_normal():
    helper = MaterialCreatorHelper()
    helper.add_file(BASE_COLOR_FILE_NAME, BASE_COLOR_FILE_PATH)
    helper.add_file(BASE_COLOR_FILE_NAME, BASE_COLOR_FILE_PATH)

    assert helper.is_complete() is False


def test_get_material_name():
    helper = MaterialCreatorHelper()
    helper.add_file(BASE_COLOR_FILE_NAME, BASE_COLOR_FILE_PATH)
    helper.add_file(NORMAL_FILE_NAME, NORMAL_FILE_PATH)
    helper.add_file(ORM_FILE_NAME, ORM_FILE_PATH)

    assert helper.get_material_name() == MATERIAL_NAME
