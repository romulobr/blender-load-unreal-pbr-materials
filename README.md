
# blender-load-unreal-pbr-materials

This simple add-on will allow you to create PBR materials from the unreal substance painter format with one click.

How to use
--
Install the add on, it will create a panel called Unreal PBR Material in your 3d view, if you click on it, there' s a button inside the panel, press the button, point to your files and that' s it.


Current Limitations
--
* It should Work with any files that are in the format:
```
Material_Name_BaseColor.(png|jpg|tiff|etc)
Material_Name_Normal.(png|jpg|tiff|etc)
Material_Name_OcclusionRoughnessMetallic.(png|jpg|tiff|etc) `
```

```OclussionRoughnessMetallic``` can actually be in any order in your file, it will separate the RGB components correctly and connect them.

* You need to click the button each time for every material.

I intend to make a batch functionality where you can point to a folder and it will materials according to the textures in there, but I' m not sure if people actually want that and I don't really use it like that.

Let me know if you think I should support different file format variations

It will try to load the images, connect the nodes correctly in the material and save it with ```Material_Name```

I made this for me, but wanted to release it as I think it's quite useful and assembling those nodes is always an annoyance to me.

It's my first add-on, any feedback is appreciated, if you think more features could make it usable to you, just let me know.
 
Special thanks to [BlackStartx](https://github.com/BlackStartx/) who made the awesome [pycharm blender plugin](https://github.com/BlackStartx/PyCharm-Blender-Plugin) which helped so much to achieve this.

  

Thanks,
Rom