Editor {#napkin}
=======================
*	[What Is Napkin](@ref what_is_napkin)
*	[Launching Napkin](@ref launching_napkin)
*	[General Structure](@ref napkin_structure)
	*	[Opening a Project](@ref napkin_project_management)
	* 	[Document Management](@ref napkin_doc_management)
	*	[Resource Management](@ref napkin_res_management)
*	[Panels](@ref napkin_panels)
	* [Resources](@ref napkin_resources)
	* [Scene](@ref napkin_scene)
	* [Configuration](@ref napkin_configuration)
	* [Apprunner](@ref napkin_apprunner)
	* [Inspector](@ref napkin_inspector)
	* [Modules](@ref napkin_modules)
	* [Mesh Preview](@ref napkin_mesh_preview)
	* [Texture Preview](@ref napkin_texture_preview)
	* [Instance Properties](@ref instance_properties)
	* [Log](@ref napkin_log)
	* [Curve](@ref napkin_curve)

What is Napkin? {#what_is_napkin}
=======================

Napkin allows you to create and edit application content, associated with a specific NAP project. NAP's main storage format is JSON, which we consider to be quite a readable format. But as projects get larger, it helps to have a more ergonomical view on the data you are creating. Napkin helps you do that. Fire up the editor, launch your NAP application and edit your file to see the changes you make reflected in real time. Files work cross platform and can be shared between Windows and Linux.

![](@ref content/napkin.png)

### Terminology
The following jargon will be used in this document:
	- `File > New` A menu item called *New* in the menu *File* in the menu bar at the top of the window or your screen
	- `LMB` Click left mouse button
	- `RMB` Click right mouse button
	- `CTRL + X` Press the *X* key while holding *CTRL* (on Windows) or *CMD* (the curly symbol on Mac)

Launching Napkin {#launching_napkin}
=======================

After downloading and extracting the NAP package, you can find Napkin inside the `tools/napkin` directory. When building Napkin from source it will be placed in the `binary` output directory, inside a folder called `napkin`. Napkin is also included with packaged projects. This allows others to edit application content after compilation.

See [Project Management](@ref project_management) for further details, including how to disable including Napkin in packaged projects. 

General Structure {#napkin_structure}
=======================

Content and configuration settings are stored in `.json` files. Both can be created and edited using Napkin. The app and Napkin share the same code base. If you adjust and recompile a `Resource` or `Component`, Napkin will reflect those changes in the editor.

Opening a Project {#napkin_project_management}
-----------------------

To open a project:
- `Project > Open Project...`<br>

Use the file browser to select the project you want to load. The project is a `.json` file with the name: `app.json`. The `app.json` file points to a `Data` and `ServiceConfig` file. Both documents can be edited by napkin. The `Data` file contains application content, the [ServiceConfig](@ref service_config) file contains application configuration settings.

Before Napkin can load the `Data` file it will attempt to load all the `RequiredModules`. Every module has it's own set of dependencies, which will be resolved as well. If loading succeeds, Napkin can safely create and edit files because it can access all the resources exposed by the modules. You can safely launch multiple instances of Napkin to work on multiple projects at once.

Document Management {#napkin_doc_management}
-----------------------

To make a new data file: 
- `File > New` or `CTRL + N` creates an empty document.<br> 

To open a different data file:
- `File > Open...` or `CTRL + O` <br>

To save the data file:
- `File > Save` or `CTRL + S` <br>

To save the data file under a different name:
- `File > Save as...`<br> 

To reload the data file:
- `File > Reload`<br> 

To set the data file as project default:
- `File > Set as project default`<br>

Configuration Management {#napkin_config_management}
-----------------------

To make a new config file: 
- `Configuration > New` creates an empty document.<br>

To open a different config file:
- `Configuration > Open...`<br>

To save the config file:
- `Configuration > Save`<br>

To save the config file under a different name:
- `Configuration > Save as...`<br>

To set the config file as project default:
- `Configuration > Set as project default`<br>

Resource Management {#napkin_res_management}
-----------------------

Every document contains [Resources](@ref resources) and [Entities](@ref scene_overview).

A resource is a stand alone building block that is always created and initialized on startup of your application. An entity is a special type of resource, which isn't created by default. Only entities that are part of your [Scene](@ref scene_setup) are instantiated. You can add the same entity to the same scene multiple times, each with different settings.

### Create Resource {#new_resource} ###
- In the resources panel, `RMB` on `Resources` and choose `Create Resource...`.
- Select a resource from the list of available resources.
- Double `LMB` on the newly created resource to change it's name.
- Select the newly created resource to edit it's properties.

### Edit Resource {#edit_resource_props} ###
- Select a resource in the Resources panel.
- Edit it's properties in the Inspector panel.

### Create Group {#new_group}
- In the resources panel, `RMB` on `Resources` and choose `Create Group...`.
- Select a group type from the list of available groups.
- Double `LMB` on the newly created group to change it's name.
- `RMB` on the group to add new or existing resources.
- `RMB` on the group and select `Create Group` to create a sub group.
 
### Create Entity {#new_entity} ###
- In the resources panel, `RMB` on `Entities` and choose `Create Entity`.<br>
- Double `LMB` on the newly created entity to change it's name.<br> 
- You can delete the Entity by using `RMB` and choosing `Delete`.<br>

### Add Component to Entity {#new_component} ###
- `RMB` on your entity and choose `Add Component`. <br> 
- Pick the component from the list of available components.<br> 
- Which Component types are exposed depends on which modules are loaded.<br>

### Add Entity to Scene {#add_entity} ###
- In the resources Panel: Ensure there is at least 1 scene available.
	- Otherwise create one.
- In the Scene panel: `RMB` on a scene and choose `Add Entity...`.<br> 
- Pick an entity from the list of available entities.<br> 

### Delete Entity from Scene {#delete_entity} ###
- In the Scene panel: `RMB` on an entity and select `Delete Instance`.

### Override Instance Property {#in_prop_override} ###
- In the Scene panel: Select the Component.
- Edit the properties of the selected Component in the Inspector panel.

### Remove Instance Property Override {#in_prop_remove} ###
- In the Scene panel: Select the Component.
- In the Inspector panel: `RMB` on the propery to clear.
- Select `Remove override`

Panels {#napkin_panels}
=======================

Napkin consists of several dockable panels that you can arrange yourself.<br>
All panels showing lists of items that can be filtered by name, type or value from the textinput at the top.

Resources {#napkin_resources}
-----------------------

Shows all the resources and entities that are part of your application. Select a resource or component of an entity to edit their default properties. Every resource (under the `Resources` item) is created when the document is loaded. Entities (under the `Entities` item) are not created by default. Only entities that have been added to the scene will be [instantiated](@ref resources_instances).

![](@ref content/napkin-panel-resources.png)
 
Scene {#napkin_scene}
-----------------------

Shows the entities that will be instantiated when the document is loaded. You can add the same entity to the same scene multiple times and override properties on a per instance basis. Components that are marked with a different color have property overrides applied to them.

Note that an empty (`new`) file does not contain a `Scene` resource by default, you must explicitly [create](@ref new_resource) one. The new scene is available directly after creation.


![](@ref content/napkin-panel-scene.png)

Configuration {#napkin_configuration}
-----------------------

Shows all the service configurations. You can edit a configuration in the [Inspector](@ref  napkin_inspector)

![](@ref content/napkin-panel-configuration.png)

AppRunner {#napkin_apprunner}
-----------------------

Allows you to start / stop the application you are working on. 

- Click on the `...` button to browse to the executable.

![](@ref content/napkin-panel-apprunner.png)

If your application logs object names in the proper format, you can double-click log messages with that link in the log panel and it will highlight the appropriate object/property in the editor.  
 
Curve {#napkin_curve}
-----------------------

The  Curve panel allows for visual editing of a function curve.

![](@ref content/napkin-panel-curve.png)

- Select a FloatFCurve resource in the resources panel.
- Open the Curve panel and start editing.

Controls:
- `LMB` on curve points or tangent handles to select them
- `SHIFT + LMB` on curve points to add them to the selection
- `CTRL + LMB` add a point on the curve at the clicked location
- `LMB + drag` in the background to rubberband select point handles or tangent handles
- `ALT + MMB` pan the view
- `ALT + RMB` zoom the view horizontally
- `SHIFT + RMB` zoom the view vertically
- `SHIFT + ALT + RMB` zoom the view both vertically and horizontally
- `F` to frame the selected handles inside the view (if no handles are selected, frame all)
- `A` to frame the entire curve inside the view
- Use the buttons in the toolbar or `RMB` in the curve view to change the interpolation of segments.
- Tangent handles can be "broken" for discontinuous curves or "aligned" for c2 continuous curves.

Because of the one-dimensional evaluation nature of function curves, the editor will keep you from creating curves with "overhang" (ie. curves that have multiple solutions). In order to do so, the effective distance of the tangent handles will be limited.   
 
Inspector {#napkin_inspector}
-----------------------
This panel shows the **properties** for the currently selected object.

![](@ref content/napkin-panel-inspector.png)

- If an object is selected in the `Resources` panel you are editing the default (shared) properties
- If an object is selected in the `Scene` panel you are editing unique instance properties
- If an object is selected in the `Configuration` panel you are editing service configuration properties

Most properties are changed by typing in a new value in the `value` column. Some values like `Pointers` provide a button next to the field that allows you to select the target object. File properties have their own button that shows a file selection dialog in which you can select the file.

Modules {#napkin_modules}
-----------------------
Shows all currently loaded modules by Napkin. The modules expose all available components and resources to Napkin and the running application.

Mesh Preview {#napkin_mesh_preview}
-----------------------
Allows you to inspect a mesh in 3D, including all of it's properties such as: light information, triangle count, available vertex attributes, connectivity, topology, bounds etc. Every type of mesh is supported, including triangular and non-triangular meshes like the [nap::Circle](@ref nap::Circle) and [nap::Line](@ref nap::Line).

![](@ref content/napkin-panel-mesh-preview.png)

To load a mesh resource:

- Select a [mesh](@ref nap::IMesh) in the resources panel.
- `RMB` on the mesh and select `Load into Mesh Preview`

Resources that are a [mesh](@ref nap::IMesh) are eligable. Loading happens on a different thread, independent from the editor. If the load operation fails an error is reported in the [log panel](@ref napkin_log). Property changes that you make to the *loaded* mesh are reflected in the mesh preview panel. This allows you to inspect the mesh using different settings, without the need to re-load your application. A quick way to test this is to change the `Polygon Mode` of a loaded mesh.

NAP ships with many meshes, including primtive 3D shapes such a [box](@ref nap::BoxMesh), [sphere](@ref nap::SphereMesh), [plane](@ref nap::PlaneMesh) and [torus](@ref nap::TorusMesh). For testing and / or shading purposes you can use a [humanoid](@ref nap::HumanoidMesh), [toy](@ref nap::ToyMesh), [shader ball](@ref nap::ShaderBallMesh) and [lucy](@ref nap::LucyMesh) mesh. Simple polygon shapes are available in the form of a [line](@ref nap::Line), [circle](@ref nap::Circle), [rectangle](@ref nap::Rectangle) etc. To load your own mesh, use a [geometry from file](@ref nap::GeometryFromFile) or [mesh from file](nap::MeshFromFile) resource. More about meshes can be found in the [render documentation](@ref rendering).


Texture Preview {#napkin_mesh_preview}
-----------------------
Allows you to inspect a 2D texture and cubemap in 2D *and* 3D, including all of it's properties such as: resolution, channels, bit depth etc. Every type of 2D texture and cubemap is supported, including the [nap::ImageFromFile](@ref nap::ImageFromFile) and [nap::CubeMapFromFile](@ref nap::CubeMapFromFile).

![](@ref content/napkin-panel-texture-preview.png)

To load a 2D texture resource:

- Select a [2D texture](@ref nap::Texture2D) in the resources panel.
- `RMB` on the texture and select `Load into Texture Preview`.

![](@ref content/napkin-panel-cubemap-preview.png)

To load a cubemap resource:

- Select a [cubemap](@ref nap::TextureCube) in the resources panel.
- `RMB` on the cubemap and select `Load into Texture Preview`.

Resources that are a [2D texture](@ref nap::Texture2D) or [cubemap](@ref nap::TexturCube) are eligable. Loading happens on a different thread, independent from the editor. If the load operation fails an error is reported in the [log panel](@ref napkin_log). Property changes that you make to the *loaded* texture are reflected in the texture preview panel. This allows you to inspect the texture using different settings, without the need to re-load your application. A quick way to test this is to change the `Width` and `Height` of a loaded cubemap.

NAP ships with a couple of 2D textures and cubemaps for testing purposes, including the [uv test texture](@ref nap::UVTestTexture), [test cube map](@ref nap::TestCubeMap) and [sunset cube map](@ref nap::SunsetCubeMap). To load your own texture, use an [image from file](@ref nap::ImageFromFile) or [cubemap from file](@ref nap::CubeMapFromFile) resource.

You can apply the loaded texture to a custom mesh, to do so:

- Select a [mesh](@ref nap::IMesh) in the resources panel.
- `RMB` on the mesh and select `Load into Texture Preview`

When a texture is loaded, the preview will attempt to load the mesh and apply it. However, the mesh must include a valid uv vertex attribute; otherwise, the texture cannot be applied, the operation will fail, and an error will be logged.

Instance Properties {#instance_properties}
-----------------------
Shows all component instance property overrides.

![](@ref content/napkin-panel-modules.png)

Log {#napkin_log}
-----------------------

Shows Napkin related messages. If you're [running your application from Napkin](@ref napkin_apprunner) the output will be shown in this window too.
![](@ref content/napkin-panel-log.png)

Each message has a Log Level attached that will indicate its severity:
	- `fine` and `debug` messages are usually not that interesting and will not be shown by default, they're mostly for figuring out the more specific details of your application and the editor.<br>
	- `info` messages communicate a notable state change in the editor or your application.
	- `warning` indicates you should probably look what is being said.
	- `fatal` means something is not right and are very useful for discovering why something doesn't work.

Use the filter to find specific messages. The dropdown on the top-right of this panel allows you to show or hide messages based on their level, in order of importance. `warning` is more important than `debug`. If a message pops up that has been underlined, you can double `RMB` it to reveal the object or property that message is saying something about.

![](@ref content/napkin-panel-instance-props.png)

Napkin allows you to edit resource properties and instance properties. Instance properties are unique per instance where resource properties are shared by all instances. Only properties of a component can be overridden per instance because a component is instantiated, together with the entity the component belongs to. Select a resource in the resources panel to edit shared properties. Select a component in the scene panel to edit unique properties. 

