FAQ {#faq}
=======================

*	[Where should I start?](@ref start)
*   [What are the various stages?](@ref stages)
*   [Why so many stages?](@ref why_stages)
*   [Is NAP difficult to learn?](@ref difficult_learn)
*   [What editor should I use?](@ref editor_pref)
*   [Can I create resources at runtime?](@ref runtime_resources)
*   [Can I spawn entities at runtime?](@ref runtime_entities)
*   [What is the order of processing?](@ref processing_order)
*   [Where to start with Vulkan in NAP?](@ref vulkan_nap)
*   [What are important directories?](@ref important_directories)

# Where should I start? {#start}

If you're completely new to NAP it's best to [download](https://github.com/napframework/nap/releases) the pre-compiled `packaged framework` and try out some of the demos. Start with `helloworld` demo and work your way up in difficulty. All demos are well documented and explain various core concepts, including their building blocks. 

Now, if you like what you see and want to start application development in NAP, we recommend working against [source](https://github.com/napframework/nap) instead of a package. The entire development team rolls like this, because we make frequent edits to the source code whilst developing the application; often on a seperate branch until ready for integration down-stream. Working against source also gives you deeper insight into the inner workings of the engine, details otherwise hidden behind an interface.

And contrary to what you might think, compiling and working with NAP from source is relatively straight forward and doesn't involve a lot of custom setup, compared to the framework release. The steps are explained in the online [.readme](https://github.com/napframework/nap?tab=readme-ov-file#compilation), which boil down to: Clone NAP, download and extract pre-compiled Qt, setup the `QT_DIR` environment variable, run the setup script and generate the solution. It won't take more than 10 minutes on most supported platforms, why? Because all third party dependencies are pre-compiled and should work out of the box.

# What are the various stages? {#stages}

NAP has 3 distinct stages (or levels):

1. NAP from Source; framework source code
2. NAP from Package; compiled framework package
3. NAP App; compiled distributable application

# Why so many stages? {#why_stages}

Good question! Having a pre-compiled binary release of the framework allows you to freeze and create a `snapshot` of the entire framework your application is developed against, which turns out to be very convenient when you *most* need it! You can choose to include the source code of your application, for easy distribution and runtime guarantees.

As we know, software is always in a state of flux and is likely unsupported, incompatible or broken 1, 2 or 5 years from now. Having a complete snapshot of the entire NAP stack helps you get back in when you don't want to; without having to gather all the various bits and pieces that are maybe no longer available, unsupported or broken. This becomes especially important when you are responsible for many projects, at many different locations on different operating systems. 

It is also a convenient way to share the project with external developers, without the need to provide them with access to all your modules, branches and other changes; parts of which might be private.

# Is NAP difficult to learn? {#difficult_learn}

Yes, in the beginning, until it clicks. If it doesn't click for you that's ok, don't beat yourself up over it! Some people like it, others don't. But those who do enjoy it often become really passionate about it.

With that out of the way; C++ already isn't the easiest language and concepts like [RTTI](https://en.wikipedia.org/wiki/Run-time_type_information), which are essential to how the editor and framework operate, can be especially challenging if you're new to these ideas. But once you grasp them, you’ll be rewarded with unmatched flexibility, speed, and modularity; transforming your intricate ideas into powerful tools or instruments.

And then there’s Vulkan: yes, it’s infamous for requiring hundreds of lines of code just to render a triangle. But here’s the good news; you don’t have to write all that code yourself. We’ve built a complete engine from scratch so you can start creating impressive visuals right away. In NAP, you won’t need to touch Vulkan unless you want to (and you really should, it’s incredible).

If you find the code challenging, we strongly suggest reading [Effective Modern C++]((https://www.oreilly.com/library/view/effective-modern-c/9781491908419/)) by Scott Meyers. The book clearly explains the many new concepts of modern C++ that we use everywhere in NAP.

# What editor should I use? {#editor_pref}

We generally recommend using [CLion](https://www.jetbrains.com/clion/) on both Linux and Windows. But my personal favorite is [Visual Studio](https://visualstudio.microsoft.com/) together with [Visual Assist](https://www.wholetomato.com/) on Windows; it's in my DNA - fast, complete, great debugger, pretty. But most in our team switched completely to Linux and are not coming back - their words not mine..

Also: don't generate 2 profiles at the same time in CLion, for example `Debug` & `Release`. Choose one *or* generate them one after the other - something in our build scripts prevents profiles from being generated at the same time in CLion and we haven't figured out what exactly.

# Can I create resources at runtime? {#runtime_resources}

Yes you can, you don't *have* to use the editor. We often use a mix, where the resources known in advance are authored in the editor and others created at runtime, often on `init()` of another resource.

If you create a resource at runtime you must manage it's lifetime, instead of relying on the `nap::ResourceManager`. The easiest way to do this is to move the created resource into a `unique_ptr` that you keep around until the resource that created it is destroyed. This ensures your resource is deleted and that hot-loading keeps working.

When you create a resource at runtime you must set all it's properties and then call `init()`, for example:

~~~~~~~~~~~~~~~{.cpp}
// Create resource
auto img = std::make_unique<nap::ImageFromFile>(core);
img->mID = "MyResource";

// Set properties
img->mImagePath = "imgs/test.jpg";
img->mGenerateLods = false;
img->mUsage = EUsage::Static;

// Initialize
if(!img->init(error))
    return false;

// Store it
mResource = std::move(img);
~~~~~~~~~~~~~~~

That's it! The resource manager does something similar, although it assigns the properties using `RTTI` because is has no idea what it is creating; it only knows what settings to assign and how to initialize it.

# Can I spawn entities at runtime? {#runtime_entities}

Yes you can, although less common but sometimes very useful. First you need to create a scene (resource) that can spawn, hold and update your entity resource:

~~~~~~~~~~~~~~~{.cpp}
// Create the scene
auto scene = std::make_unique<nap::Scene>(core);
scene->mID = "MyScene";

// Initialize the scene
if (!scene->init(error))
    return false;

// Store it
mScene = std::move(scene);
~~~~~~~~~~~~~~~

Next you create the entity to spawn including all of it's components, for example:

~~~~~~~~~~~~~~~{.cpp}
// Create the entity resource
auto entity = std::make_unique<nap::Entity>(core);
entity->mID = "MyEntity";

// Create and add a transform component
auto xform =  std::make_unique<nap::TransformComponent>()
xform->mID = "MyTransform";
entity->mComponents.emplace_back(xform.get());

// Spawn it!
auto entity_instance = mScene->spawn(*entity, error);
if(entity_instance == nullptr)
    return false;
...
~~~~~~~~~~~~~~~

The returned `entity_instance` is a handle to the entity spawned by your scene, which manages the entity for you. The entity is destroyed when the scene is destructed or by calling `Scene::Destroy`. The entites in your scene receive update calles every frame until the scene is destroyed.

# What is the order of processing? {#processing_order}

Parent entities are always updated before their children. This means that, if an entity has children, its components are processed first, followed by those of its descendants.

Components receive an `update()` call every frame in the **order of declaration** in the editor. This means that if your entity has 2 components in the following order: (1)transform, (2)renderer; the the transform is updated before the renderer. The final (global) transform is calculated after update, on `postUpdate()`.

Root entities are updated in no particular order. Child entities are updated in the **order of declaration**.

# Where to start with Vulkan in NAP? {#vulkan_nap}

If you have experience with OpenGL and want to get started with Vulkan in NAP, I recommend reading our [OpenGL to VUlkan](https://blog.nap-labs.tech/d0/dfd/md_articles_001_nap_opengl_to_vulkan) transition blog. That article explains how and why we ported our engine from OpenGL to Vulkan, and the impact this had on performance and portability. If you're not comfortable with real-time 3D Graphics yet, it's better to start with the basics; a good book and after that some code. This will make it much easier to understand Vulkan-related code in NAP Framework; why it's there and what it does. I’ve also hosted a number of NAP rendering workshops over the years, a collection of the slides can be found [here](https://blog.nap-labs.tech/d3/dd0/md_articles_006_nap_render_workshop).

The good news is: you don’t need to work with Vulkan directly unless you choose to! We’ve developed a full engine from the ground up, so you can render almost anything without ever issuing a single Vulkan command.

# What are important directories {#important_directories}

## For NAP Framework
Core engine: `core/src`  
RTTI information: `rtti/src`  
Utilities: `utility/src`  
Demos: `demos`  
Essential framework modules: `system_modules`    
Editor source: `tools/napkin`  
Build tools: `tools/buildsystem`  
User modules: `modules`  

## For your application
Source code: `src`  
App-specific module: `module/src`  
Data files: `data`  

## For your user module
Source code: `src`  
Third-party dependencies: `thirdparty`  
Data files: `data`  
