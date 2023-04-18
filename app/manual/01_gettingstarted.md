Getting Started {#getting_started}
=======================
* [Overview](@ref getting_started_overview)
* [Create a New Application](@ref create_blank_app)
* [Compile and Run](@ref compile_run)
* [Add Content](@ref add_content)
    * [Resource](@ref audio_resource)
    * [Entity](@ref audio_entity)
    * [Component](@ref audio_components)
    * [Scene](@ref content_scene)
* [Add Logic](@ref app_logic)
    * [Init](@ref app_init)
    * [Update](@ref app_update)
    * [Render](@ref app_render)
* [Package for Distribution](@ref app_package)

Overview {#getting_started_overview}
=======================

In this tutorial we're going to make a new application that renders a rotating textured cube to a window. You can change the rotation speed with a parameter. This tutorial assumes you are working from a pre-compiled NAP package, not the NAP source-code.

Create a New Application {#create_blank_app}
=======================
To create a new application:

- Use a terminal to navigate to the `tools` directory, inside the NAP installation root.
- Run `create_app.bat myapp` (Windows) or `./create_app.sh myapp` (macOS and Linux)

After creation your new application is located at `apps/myapp`. This directory contains your source-code, assets and build instructions. The `app.json` file in the root of the directory defines various project specific settings, such as: the name of your app , which modules to include and what content to load.

```
{
    "Type": "nap::ProjectInfo",
    "mID": "ProjectInfo",
    "Title": "myapp",
    "Version": "0.1.0",
    "RequiredModules": [
        "napapp",
        "napcameracontrol",
        "napparametergui",
        "napmyapp"
    ],
    "Data": "data/objects.json",
    "ServiceConfig": "",
    "PathMapping": "cache/path_mapping.json"
}
```

The most important module here is `napmyapp`. This is your *application module*, located inside the `myapp/module` directory. This is where you store application specific `Resources` and `Components`. 

Compile and Run {#compile_run}
================

Open the generated solution and select the `Release` configuration. Compile and run your application. You should see an empty window pop up:

![](@ref content/gs_new_app.png)

To learn more about setting up applications, modules and third-party dependencies read the [Project Management](@ref project_management) documentation.

Add Content {#add_content}
================

## Launch Napkin

We're going to use [Napkin](@ref napkin) to edit application content. 

Go to the `tools/napkin` directory and launch `napkin`

### Open Project

In Napkin click on `Project` -> `Open...` and browse to `apps/myapp`. Select `app.json`

![](@ref content/gs_napkin.png)

The `app.json` points to an external file that holds the content of your application. By default, application content is stored in `myapp/data/objects.json`. You use Napkin to author this content.

If Napkin fails to load the project make sure to [build](@ref compile_run) the application (in `Release` mode) at least once before loading it. This ensures that the custom application module `napmyapp` is compiled for you. The editor can then load and inspect it. All other modules (render, audio etc.) are pre-compiled and should work out of the box.

## The Textured Cube

Let's begin by adding the resources that define, when combined, a textured cube in NAP.

### Mesh {#cube_resource}

Start by creating a uniform [box mesh](@ref nap::BoxMesh) at the center of the scene.

Right-click on the `Resources` item inside the resource panel and select `Create Resource...`. Select the `nap::BoxMesh` and rename it to `CubeMesh`.

### Texture {#cube_texture}

Now load the [image](@ref nap::ImageFromFile) that we will apply as a texture. Following the steps above: create a `nap::ImageFromFile` resource and rename it to `CubeTexture`. 

If we now save the file and start the application it will fail to initialize because the `CubeTexture` doesn't point to a valid image on disk. We must provide it with one.

#### Configure Texture

Download this texture and move it to `myapp/data`. Select the `CubeTexture` in Napkin. Link in the image by clicking on the folder icon next to the `ImagePath` property in the inspector panel.

Note that all assets must be placed in the `data` directory. This allows the application to use relative paths instead of absolute paths.

### Shader {#cube_shader}

Next we create a [shader](@ref nap::ShaderFromFile) program that we use to render the cube. Create a `nap::ShaderFromFile` resource and rename it to `CubeShader`. 

If we now save the file and start the application it will fail to initialize because the shader doesn't point to a valid vertex and fragment shader on disk. We must link them in.

#### Configure Shader

Download the *cube.vert* and *cube.frag* to `myapp/data/shaders`. Select the `CubeShader` in Napkin. Link in the shaders by clicking on the folder icon next to the `VertShader` and `FragShader` properties in the inspector panel.

### Material

Let's add a [material](@ref nap::Material), so we can bind a texture to the shader and give it a color. Create a `nap::Material` resource and rename it to `CubeMaterial`. 

#### Configure Material

Now bind the texture and give it a color. Select the `CubeRenderComponent`. 

##### Set Color

Right-click on the `Uniforms` property in the inspector panel and add a `nap::UniformStruct` to it. Change the `name` property of the struct to *UBO*. Now right-click on the `Uniforms` property of the new struct and add a `nap::UniformVec3` to it. Change the `name` property of the new uniform vec3 to *color*.

You just set the (default) color of the cube to white by creating a binding in the material that targets the `UBO.color` uniform in the shader:

```
// uniform buffer inputs
uniform UBO
{
    vec3 color;   //< Cube color
} ubo;
````

#### Bind Texture

Right-click on the `Samplers` property in the inspector panel and add a `nap::Sampler2D`. Change the `name` property of the new sampler to *inTexture*. Now create a link to the texture by clicking on the (rings) icon to the right of the `Texture` property. Select the `CubeTexture` in the popup.

You just set the (default) texture of the cube to `CubeTexture` by creating a binding in the material that targets the `inTexture` sampler in the shader:

```
// unfiorm sampler inputs 
uniform sampler2D inTexture;	//< Cube texture
```

## Create Cube Entity {#audio_entity}

Continue by adding an entity that renders the cube to screen. 

Right click on the `Entities` item in the resource panel and select `Create Entity`. Double click on the new entity and change it's name to `CubeEntity`.



![](@ref content/gs_napkin_create_entity.png)

### Add  Components {#audio_components}

The `CubeEntity` needs 3 components: [Transformcomponent](@ref nap::TransformComponent) to position it, a [RotateComponent](@ref nap::RotateComponent) to rotate it and a [RenderableMeshComponent](@ref nap::RenderableMeshComponent) to render it.

Right click on the `CubeEntity` in the resource panel. Select `Add Component...` from the popup meny and select `nap::TransformComponent`. Rename the transform to `CubeTransformComponent`. 

Repeat these steps for the `nap::RotateComponent` and `nap::RenderableMeshComponent`. Rename them to `CubeRotateComponent` and `CubeRenderComponent`. 

The transform places the cube in the center of the scene. That's fine for now. The other 2 components need to be configured.

#### Configure Rotate Component

Select the `CubeRotateComponent` in the resource panel. Expand the `Axis` property in the inspector panel and change it to `0 1 0`. Next change the `Speed` property to `1.0`. This tells the component to rotate the cube 360* over the Y-axis in 1 second. 

#### Configure Render Component

We need to tell the component which mesh to render using what material. 

Select the `CubeRenderComponent` in the resource panel. Create a link to the cube mesh by clicking on the (rings) icon to the right of the `Mesh` property. Select the `CubeMesh` in the popup.

Expand the `MaterialInstance` item in the inspector panel and create a link to the cube material by clicking on the icon to the right of the `Material` property. Select the `CubeMaterial` in the popup.

## Scene {#content_scene}

What's left on the content side is to add the entity to the scene, otherwise it is not created (instantiated) on startup. 

Right-click on the `Scene` item in the scene panel, click on `Add Entity...` and select the `CubeEntity`. Save the file `File -> Save` and launch the app from your IDE or using the `AppRunner` in Napkin.

You should see the same window popup as before without any notable changes. That's because we did not tell the app to render the cube. NAP created and validated the cube entity and resources but isn't instructed to render it. We have to add some logic to the app that instructs the system to draw it.

If at this point the application fails to initialize check the ouput of the log. You probably missed a step. If that's the case try to fix it by tracing the error message.

Application {#app_logic}
==========================

Close Napkin and open the `newprojectapp.h` file located inside the `src` directory. This document, together with the `.cpp` file, contains the application runtime code. It allows you to control the flow of data and render specific objects to screen using the resources we just created.

## Init {#app_init}

The init method is used to initialize important parts of your application and store references to resources. For this example we need access to the `AudioEntity`. Add the following line of code to your application class declaration, right after `mGnomonEntity` in `newprojectapp.h`:

~~~{cpp}
ObjectPtr<EntityInstance>   mAudioEntity = nullptr;         ///< Pointer to the entity that plays back music
~~~

And add the following line of code to the end of the `NewProjectApp::init()` method of your application in `newprojectapp.cpp`:

~~~{cpp}
mAudioEntity = mScene->findEntity("AudioEntity");
~~~

We just created a link to the audio entity. We can use this link to manipulate the entity and it's components when the app is running.

## Update {#app_update}

The `update` method is called every frame. The parameter `deltaTime` indicates how many seconds have passed since the last update call. You should perform any app specific logic in here that does not concern rendering.

Because we set the property `AutoPlay` of the PlaybackComponent in the app structure file to `True`, the file starts playing automatically on startup. Let's add a button to start and stop playback at runtime. Add the following include directives to `newprojectapp.cpp`:

~~~{cpp}
#include <audio/component/playbackcomponent.h>
#include <imgui/imgui.h>
~~~

.. and add the following block of code to the `update` method:

~~~{cpp}
auto playbackComponent = mAudioEntity->findComponent<audio::PlaybackComponentInstance>();

// Draw some UI elements to control audio playback
ImGui::Begin("Audio Playback");
if (!playbackComponent->isPlaying())
{
  	if (ImGui::Button("Play"))
      	playbackComponent->start(0);
}
else 
{
  	if (ImGui::Button("Stop"))
      	playbackComponent->stop();
}
ImGui::End();
~~~

When we compile and run the app you should see a button. Click on it to start / stop the playback of the audio file.

![](@ref content/gs_result.png)

## Rendering {#app_render}

`render` is called after `update`. You use this call to render geometry and UI elements to a window or render target. You have to tell the renderer what you want to render and where to render it to. The button (recorded on `update`) is rendered when `mGuiService->draw()` is called. To learn more about rendering with NAP take a look at our [render documentation](@ref rendering). 

Package for Distribution {#app_package}
==========================

To create a distributable package of your application run `package.bat` (windows) or `./package` (macOS / Linux). Append `--help` for additional information. By default the application including Napkin and all assets is packaged for you.



