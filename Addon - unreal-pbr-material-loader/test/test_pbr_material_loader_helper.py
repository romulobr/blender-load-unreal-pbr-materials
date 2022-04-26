import itertools

import pytest

from ..pbr_textures import PBRComponent
from ..pbr_material_loader_helper import PBRMaterialLoaderHelper


# file name:  Some_Long_Material_Name_BaseColor.png
# file name:  Some_Long_Material_Name_Normal.png
# file name:  Some_Long_Material_Name_OcclusionRoughnessMetallic.png

BASE_COLOR_FILE_PATH = "c:\\Some_Long_Material_Name_BaseColor.png"
BASE_COLOR_FILE_NAME = "Some_Long_Material_Name_BaseColor.png"

NORMAL_FILE_PATH = "c:\\Some_Long_Material_Name_Normal.png"
NORMAL_FILE_NAME = "Some_Long_Material_Name_Normal.png"

ORM_FILE_PATH = "c:\\Some_Long_Material_Name_OcclusionRoughnessMetallic.png"
ORM_FILE_NAME = "Some_Long_Material_Name_OcclusionRoughnessMetallic.png"

UNKNOWN_FILE_PATH = "c:\\Some_Long_Material_Name.png"
UNKNOWN_FILE_NAME = "Some_Long_Material_Name.png"


def test_unknown_file():
    classified_file = PBRMaterialLoaderHelper.classify_texture_files_by_name(UNKNOWN_FILE_NAME, UNKNOWN_FILE_PATH)
    assert classified_file.file_name is UNKNOWN_FILE_NAME
    assert classified_file.complete_file_path is UNKNOWN_FILE_PATH
    assert classified_file.is_base_color_texture is False
    assert classified_file.is_normal_texture is False
    assert classified_file.data_in_red_component is None
    assert classified_file.data_in_blue_component is None
    assert classified_file.data_in_green_component is None


def test_is_unknown_file():
    classified_file = PBRMaterialLoaderHelper.classify_texture_files_by_name(UNKNOWN_FILE_NAME, UNKNOWN_FILE_PATH)
    assert PBRMaterialLoaderHelper.is_unknown_file(classified_file) is True


def test_base_color_file():
    classified_file = PBRMaterialLoaderHelper.classify_texture_files_by_name(BASE_COLOR_FILE_NAME, BASE_COLOR_FILE_PATH)
    assert classified_file.file_name is BASE_COLOR_FILE_NAME
    assert classified_file.complete_file_path is BASE_COLOR_FILE_PATH
    assert classified_file.is_base_color_texture is True
    assert classified_file.is_normal_texture is False
    assert classified_file.data_in_red_component is None
    assert classified_file.data_in_blue_component is None
    assert classified_file.data_in_green_component is None


def test_normal_file():
    classified_file = PBRMaterialLoaderHelper.classify_texture_files_by_name(NORMAL_FILE_NAME, NORMAL_FILE_PATH)
    assert classified_file.file_name is NORMAL_FILE_NAME
    assert classified_file.complete_file_path is NORMAL_FILE_PATH
    assert classified_file.is_base_color_texture is False
    assert classified_file.is_normal_texture is True
    assert classified_file.data_in_red_component is None
    assert classified_file.data_in_blue_component is None
    assert classified_file.data_in_green_component is None


def test_occlusion_roughness_metallic_file():
    classified_file = PBRMaterialLoaderHelper.classify_texture_files_by_name(ORM_FILE_NAME, ORM_FILE_PATH)
    assert classified_file.file_name is ORM_FILE_NAME
    assert classified_file.complete_file_path is ORM_FILE_PATH
    assert classified_file.is_base_color_texture is False
    assert classified_file.is_normal_texture is False
    assert classified_file.data_in_red_component.value is PBRComponent.occlusion.value
    assert classified_file.data_in_green_component.value is PBRComponent.roughness.value
    assert classified_file.data_in_blue_component.value is PBRComponent.metallic.value


ALL_OCCLUSION_ROUGHNESS_METALLIC_FILE_NAME_VARIATIONS = [list(variation) for variation in list(
    itertools.permutations(["Occlusion", "Roughness", "Metallic"], 3))]


def name_to_enum(name):
    return PBRComponent[name.lower()]


ALL_EXPECTATIONS = [list(map(name_to_enum, variation)) for variation in
                    ALL_OCCLUSION_ROUGHNESS_METALLIC_FILE_NAME_VARIATIONS]

test_data = []

for index, variation in enumerate(ALL_OCCLUSION_ROUGHNESS_METALLIC_FILE_NAME_VARIATIONS):
    test_data.append(pytest.param(variation, ALL_EXPECTATIONS[index], id=str(variation)))


@pytest.mark.parametrize("combination,expectations", test_data)
def test_occlusion_roughness_metallic_file_variations(combination, expectations):
    print(combination)
    print(expectations)
    file_name = "".join(combination) + ".png"
    file_path = "c:\\" + file_name

    classified_file = PBRMaterialLoaderHelper.classify_texture_files_by_name(file_name, file_path)
    assert classified_file.file_name is file_name
    assert classified_file.complete_file_path is file_path
    assert classified_file.is_base_color_texture is False
    assert classified_file.is_normal_texture is False
    assert classified_file.data_in_red_component.value is expectations[0].value
    assert classified_file.data_in_green_component.value is expectations[1].value
    assert classified_file.data_in_blue_component.value is expectations[2].value
