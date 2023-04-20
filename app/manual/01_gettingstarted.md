Getting Started {#getting_started}
=======================
* [Overview](@ref getting_started_overview)
* [Create a New Application](@ref create_blank_app)
* [Compile and Run](@ref compile_run)
* [Napkin](@ref napkin_editor)
    * [Launch Napkin](@ref launch_napkin)
    * [Open Project](@ref open_project_napkin)
    * [Configure App Runner](@ref configure_app_runner)
* [Create Cube Resources](@ref cube_resources)
    * [Mesh](@ref cube_mesh)
    * [Texture](@ref cube_texture)
    * [Shader](@ref cube_shader)
    * [Material](@ref cube_material)
* [Create Cube Entity](@ref cube_entity)
    * [Create Cube Components](@ref cube_components)
* [Scene](@ref content_scene)
* [Setup Application](@ref app_logic)
    * [Init](@ref app_init)
    * [Update](@ref app_update)
    * [Render](@ref app_render)
* [Package for Distribution](@ref app_package)

Overview {#getting_started_overview}
=======================

In this tutorial we're going to create a new NAP application that renders a rotating textured cube to a window. 

![](@ref content/gs_result.gif)

This tutorial assumes you are working from a pre-compiled distributable NAP package. However, some people prefer working with NAP directly from source. Fortunately most instructions in this document are the same for both contexts, with the exception of some paths. Additional information is provided when this is the case.

Create a New Application {#create_blank_app}
=======================

Use a terminal to navigate to the `tools` directory inside the NAP root and run  `create_app.bat rotatingcube` (windows) or `./create_app.sh rotatingcube` (unix)

After creation your new application is located at `apps/rotatingcube`. This directory contains your source-code, assets, solution and build instructions. The `app.json` file in the root of the directory defines various project specific settings, such as: the name of your app , which modules to include and which content to load:

```
{
    "Type": "nap::ProjectInfo",
    "mID": "ProjectInfo",
    "Title": "rotatingcube",
    "Version": "0.1.0",
    "RequiredModules": [
        "napapp",
        "napcameracontrol",
        "napparametergui",
        "naprotatingcube"
    ],
    "Data": "data/objects.json",
    "ServiceConfig": "",
    "PathMapping": "cache/path_mapping.json"
}
```

The most important module here is `naprotatingcube`. This is your *application module*, located inside the `apps/rotatingcube/module` directory. This module contains `resources` and `components` that you create specifically for this project. 

Read the [Project Management](@ref project_management) documentation to learn more about managing NAP applications and modules.

Compile and Run {#compile_run}
================

Navigate to `apps/rotatingcube` and run `build.bat` (windows) or `./build.sh` (unix) to compile the application. The app is compiled to the `bin` directory of your app. Navigate to the `bin/Release-*` folder and launch the `rotatingcube` executable in that directory. You should see the following window:

![](@ref content/gs_new_app.png)

*Note that when working from source the app is compiled to the `bin` directory in the nap root, not the application root*

Napkin {#napkin_editor}
================

We're going to use [Napkin](@ref napkin) to edit the application content. 

## Launch Napkin {#launch_napkin}

From the NAP project root, browse to the `tools/napkin` directory and launch the `napkin` executable. 

*Note that when working from source you must compile Napkin first. The compiled Napkin binary can be found in the `bin/Release-*/napkin` directory.*

## Open Project {#open_project_napkin}

- Click on `Project > Open...`
- Browse to `apps/rotatingcube`
- Select `app.json`

The `app.json` points to an external file that holds the *content* of your application. By default, application content is stored in `data/objects.json` (relative to the project root). You use Napkin to author *this* content. 

All externally sourced assets (such as images, audio, video, shaders etc.) that your content references must be placed in the `data` directory of your application, in this case `apps/rotatingcube/data`.

If Napkin fails to load the project make sure to [build](@ref compile_run) the application (in `Release` mode) at least once before loading it. This ensures that the custom application module `naprotatingcube` is compiled for you. The editor can then load and inspect it. All other modules (render, audio etc.) are pre-compiled and should work out of the box.

## Configure App Runner {#configure_app_runner}

The `AppRunner` allows you to start / stop the application you are working on. This is very useful when you are editing application content and frequently have to re-launch the application.

In the app runner panel:

- Click on the `...` button
- Browse to the `apps/rotatingcube/bin/Release-*` directory
- Select the `rotatingcube` executable
- Clock on the play button

![](@ref content/gs_open_project.gif)

Create Cube Resources {#cube_resources}
================

Let's begin by adding the resources that define, when combined, a textured cube in NAP.

## Mesh {#cube_mesh}

Start by creating a uniform [box mesh](@ref nap::BoxMesh) at the center of the scene. 

In the resources panel:

- Right-click on the `Resources` item
- Select `Create Resource`
- Select the `nap::BoxMesh`
- Double click on the new item 
- Rename it to `CubeMesh`

![](@ref content/gs_create_cubemesh.gif)

## Texture {#cube_texture}

Let's add the [image](@ref nap::ImageFromFile) that we want to apply as a texture. Following the steps above: create a `nap::ImageFromFile` resource and rename it to `CubeTexture`.

If we now save the file and start the application it will fail to initialize because the `CubeTexture` doesn't point to a valid image on disk. We must provide it with one.

### Configure Texture {#configure_cube_texture}

Download the [cube_texture.jpg](/content/cube_texture.jpg) and move it to `apps/rotatingcube/data`. 

Select the `CubeTexture` in the resources panel. Link in the image by clicking on the folder icon next to `ImagePath` in the inspector panel. Browse to the texture in the `data` directory and select it.

![](@ref content/gs_create_texture.gif)

## Shader {#cube_shader}

Next we create a [shader](@ref nap::ShaderFromFile) program that we use to render the cube. Create a `nap::ShaderFromFile` resource and rename it to `CubeShader`. 

### Configure Shader {#configure_cube_shader}

Download the [cube.vert](/content/cube.vert) and [cube.frag](/content/cube.frag) shader files and move them to `apps/rotatingcube/data/shaders`. 

Select the `CubeShader` in the resources panel. In the inspector panel click on the folder icon next to `VertShader` and select the `cube.vert` shader file. Continue by clicking on the folder icon next to `Fragshader` and select the `cube.frag` shader file.

![](@ref content/gs_create_cubeshader.gif)

## Material {#cube_material}

Let's add a [material](@ref nap::Material), so we can bind a texture to the shader and give it a color. Create a `nap::Material` resource, rename it to `CubeMaterial` and select it.

### Configure Material {#configure_cube_material}

#### Link Shader {#material_link_shader}

In the inspector panel click on the icon next to `Shader` and select the `CubeShader` in the popup. 

#### Bind Color {#bind_cube_color}

Right-click on `Uniforms` in the inspector panel and add a `nap::UniformStruct` to it. Expand the new item and change the `Name` to *UBO*. Right-click on the `Uniforms` property of the new struct and add a `nap::UniformVec3` to it. Expand the new item and change the `Name` to *color* and the `Value` to *1 1 1* (white).

You just set the (default) color of the cube to white by creating a binding in the material that targets the `UBO.color` uniform in the shader:

~~~{cpp}
// uniform buffer inputs
uniform UBO
{
    vec3 color;   //< Cube color
} ubo;
~~~

#### Bind Texture {#bine_cube_texture}

Right-click on `Samplers` in the inspector panel and add a `nap::Sampler2D`. Change the `Name` of the new sampler to *inTexture*. Now click on the rings icon next to `Texture` and select the `CubeTexture` in the popup.

You just set the (default) texture of the cube to `CubeTexture` by creating a binding in the material that targets the `inTexture` sampler in the shader:

~~~{cpp}
// unfiorm sampler inputs 
uniform sampler2D inTexture;	//< Cube texture
~~~

![](@ref content/gs_create_cubematerial.gif)

Create Cube Entity {#cube_entity}
================

Continue by adding an entity that renders the cube to screen. 

In the resources panel:

- Right click on the `Entities` item
- Select `Create Entity`
- Double click on the new entity
- Rename it to `CubeEntity`

![](@ref content/gs_create_cubeentity.gif)

## Create Cube Components {#cube_components}

The `CubeEntity` needs 3 components: [Transformcomponent](@ref nap::TransformComponent) to position it, a [RotateComponent](@ref nap::RotateComponent) to rotate it and a [RenderableMeshComponent](@ref nap::RenderableMeshComponent) to render it.

In the resources panel:

- Right click on the `CubeEntity`
- Select `Add Component...`
- Select `nap::TransformComponent`
- Double click on the new component
- Rename it to `CubeTransformComponent`

Repeat these steps for the `nap::RotateComponent` and `nap::RenderableMeshComponent`. Rename them to `CubeRotateComponent` and `CubeRenderComponent`. 

![](@ref content/gs_create_cubecomponents.gif)

### Configure Transform Component {#cube_transform_component}

Select the `CubeTransformComponent` in the resources panel and change the `UniformScale` in the inspector panel to *4.0*. This makes the box 4 times as large.

### Configure Rotate Component

Select the `CubeRotateComponent` in the resources panel. Expand the `Axis` property in the inspector panel and change it to `0 1 0`. Next change the `Speed` to *0.1*. This tells the component to rotate the cube 360 degrees over the Y-axis in 10 seconds. 

### Configure Render Component {#cube_render_component}

We need to tell the component which mesh to render using what material. 

Select the `CubeRenderComponent`. In the inspector panel click on the icon next to `Mesh` and select the `CubeMesh` in the popup. Continue by expanding the `MaterialInstance` item. Click on the icon next to `Material` and select the `CubeMaterial` in the popup.

![](@ref content/gs_configure_cubecomponents.gif)

Scene {#content_scene}
==========================

What's left on the content side is to add the entity to the scene, otherwise it is not created (instantiated) on startup. 

In the scene panel:

- Right-click on the `Scene` item
- Click on `Add Entity...`
- Select the `CubeEntity`

Save the file `File -> Save` and launch the app. You should see the same window popup as before without any notable changes. That's because we did not tell the app to render the cube. NAP created and validated the cube entity and resources but has no instructions to render it. We have to add some logic to the app that instructs the system to draw it.

If at this point the application fails to initialize check the ouput of the log. You probably missed a step. If that's the case try to fix it by tracing the error message.

![](@ref content/gs_add_cube_to_scene.gif)

Application {#app_logic}
==========================

Close Napkin and open the `rotatingcubeapp.h` file located inside the `apps/rotatingcube/src` directory. This document, together with the `.cpp` file, contains the application runtime code. It allows you to control the flow of data and render specific objects to screen using the resources we just created.

## Init {#app_init}

The init method is used to initialize important parts of your application and store references to resources. For this example we need access to the `CubeEntity`. Add the following line of code to your application class declaration, right after `mGnomonEntity` in `rotatingcubeapp.h`:

~~~{cpp}
ObjectPtr<EntityInstance>   mCubeEntity = nullptr;         ///< Pointer to the entity that plays back music
~~~

And add the following line of code to the end of the `::init()` method of your application in `rotatingcubeapp.cpp`:

~~~{cpp}
// Find the cube entity
mCubeEntity = mScene->findEntity("CubeEntity");
~~~

We just created a link to the cube entity. We can use this link to manipulate the entity and it's components when the app is running.

## Update {#app_update}

The `update` method is called every frame. The parameter `deltaTime` indicates how many seconds have passed since the last update call. You should perform any app specific logic in here that does not concern rendering.

Let's add a slider that controls the rotation speed of the cube. Add the following include directive to `rotatingcubeapp.cpp`:

~~~{cpp}
#include <rotatecomponent.h>
~~~

.. and add the following block of code to the `update` method, right after `processWindowEvents`:

~~~{cpp}
ImGui::Begin("Cube Controls");
auto& rotate_component = mCubeEntity->getComponent<nap::RotateComponentInstance>();
ImGui::SliderFloat("Rotation Speed", &rotate_component.mProperties.mSpeed, 0.0f, 1.0f);
ImGui::End();
~~~

## Rendering {#app_render}

`render` is called after `update`. You use this call to render geometry and UI elements to a window or render target. You have to tell the renderer what you want to render and where to render it to. We want to render our cube instead of the gnomon. To do that replace the following line:

~~~{cpp}
&mGnomonEntity->getComponent<RenderGnomonComponentInstance>()
~~~

with:

~~~{cpp}
&mCubeEntity->getComponent<RenderableComponentInstance>()
~~~

This tells the render engine to render the cube instead of the gnomon. The GUI is drawn last, on top of the rest, when  `mGuiService->draw()` is called. To learn more about rendering with NAP take a look at our [render documentation](@ref rendering).

![](@ref content/gs_app_setup.gif)

Package for Distribution {#app_package}
==========================

Navigate to `apps/rotatingcube` and run `package.bat` (windows) or `./package.sh` (unix) to create a distributable package of your application. Append `--help` for additional information. By default the application including Napkin and all assets is packaged for you.

*Note that when working from source the the `package` script is located in the NAP root.*



