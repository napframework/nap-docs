Project Management {#project_management}
=======================

*	[Introduction](@ref project_intro)
*	[Application](@ref app)
    *	[Create](@ref app_creation) 
    *   [Configure](@ref app_config)
    *	[Package](@ref app_package)
*   [User Module](@ref user_module) 
    *   [Install](@ref user_module_installation)
    *	[Create](@ref user_module_creation)
    *   [Configure](@ref user_module_config)
    *   [Share](@ref user_module_sharing)
*	[Custom CMake](@ref custom_cmake)
	*	[Application](@ref custom_cmake_app)
	*	[User Module](@ref custom_cmake_user_module)
	*	[Third Party Dependencies](@ref custom_cmake_thirdparty)
*	[Path Mapping System](@ref path_mapping)

# Introduction {#project_intro}

This document explains how to create, configure and share a NAP application or module. 

Although a typical NAP project is an application, it doesn't have to be: it can also be a service or library. All project management utilities reside in the `tools` directory under the NAP root. Convenience shortcuts to regenerate the solution and package the application also sit within each app. We'll go over the basic tasks here and then cover some more advanced topics in the [Custom CMake](@ref custom_cmake) section for those who want to take things further.

We will use the *unix* shell syntax in this document, for convenience and readability. If you're on Windows and using the prompt, simply replace `./*.sh` with `*.bat`. Any exception to this rule will be clearly documented.

*This document assumes you are working from a pre-compiled distributable NAP package. However, some people prefer working with NAP directly from source. Fortunately most instructions in this document are the same for both contexts, except some paths. Additional information is provided when this is the case.*

# Application {#app}

A NAP application is a pre-compiled program, made using NAP Framework, that runs stand-alone on a client machine.

## Create Application {#app_creation}

Follow these steps to create a new application titled `MyFirstApp`.

1. Open a terminal
2. Browse to the NAP framework directory
3. Create the application
```
./tools/create_app.sh MyFirstApp
```

The application will be located in `apps/MyFirstApp`. This directory contains your application source-code, assets, makefiles (Linux) or visual studio solution (Windows) and build instructions.

## Configure Application {#app_config}

Within each application folder you'll find the `app.json` file which defines various project specific settings, such as: the name of your app , which modules to include and which content to load:
```
{
    "Type": "nap::ProjectInfo",
    "mID": "ProjectInfo",
    "Title": "MyFirstApp",
    "Version": "0.1.0",
    "RequiredModules": [
        "napapp",
        "napcameracontrol",
        "napparametergui",
        "napMyFirstApp"
    ],
    "Data": "data/objects.json",
    "ServiceConfig": "",
    "PathMapping": "cache/path_mapping.json"
}
```

*Note that when working with NAP from source your new application is added to the overall solution in `solution_info.json`, which includes your app as a target for the build system. When you delete your application you must (manually) remove the application and application module from `solution_info.json`, otherwise the build system will fail to generate the solution.*

### The Application Module {#app_module}

The most important module is `napMyFirstApp`. This is your **application module**, located in the `module` directory of your app. This directory contains the [resources](@ref resources) and [components](@ref component_ov) that are specific to your application. This module is created and added by the build system when the app is created. You can omit the creation of the application module by appending `--no-module` to `tools/create_app.sh`.

### External Modules {#app_config_modules}

You can add external modules to your application by modifying the `RequiredModules` property in  `app.json`. The module name should match the module directory name in `/system_modules` or `/modules`. For example: add *napaudio* to add audio functionality or *napmidi* to add mini functionality to your application. 

- The `/system_modules` directory contains modules distributed with NAP. 
- The `/modules` directory contains [user modules](@ref user_module_creation).

**If you want your [application module](@ref app_module) to have access to the resources and components of an external module you must modify the `RequiredModules` property in `module/module.json` instead of `app.json`.**

**Run `./regenerate.sh` inside your application folder to update the solution. Always run this script after making changes to `app.json` or `module.json`**

## Package Application For Release {#app_package}

Run `./package.sh` to compile and install a *release* build of your application into a distributable package. The self-contained package contains everything that your app needs to run stand-alone when extracted (except system libraries), including: 

- Project Executable 
- Assets
- Shared Libraries
    - System Modules
    - User Modules
    - Third Party
- Napkin (optional).
- Licenses

The package is archived to a `.zip` on Windows and `tar.xz` on Linux. The package does not include system libraries such as the `Visual C++ redistributable`. Options for creating installers for projects may be explored for a future NAP release. 

Packaging an application with default settings:
1. Navigate to your application
```
cd apps/MyFirstApp
```
2. Run package
```
sh ./package.sh
```

By default, projects are compressed and contain Napkin.  Projects can be left uncompressed by adding the option `--no-zip`.  Napkin can be left out via `--no-napkin`.  Excluding Napkin can save a considerable amount of space if you don't intend on using it.  Other minor options and shorthand versions of the options above can be viewed by running `package --help`.

# User Module {#user_module}

A user module contains more generic (not app related) resources and components that can be added to your NAP application.

## Install User Module {#user_module_installation}

A list of publicly available user modules can be found at [modules.nap.tech](https://modules.nap.tech). These modules are created, maintained and shared by NAP users, independent of NAP Framework. 

### From ZIP {#user_module_installation_zip}

[Download](https://modules.nap.tech) the module as `.zip` archive from (for example) Github and install it into the nap `modules` directory:

1. Open a terminal
2. Change into your NAP framework directory
3. Install the module
```
./tools/install_module.sh ~/Downloads/napdatabase-main.zip
```

### From Repository {#user_module_installation_repo}

Clone the repository and set up the module in the nap `modules` directory:

1. Open a terminal
2. Change into your NAP modules directory
3. Clone the repository
```
cd modules
clone https://github.com/naivisoftware/napdatabase.git
```
4. Set it up
```
./../tools/setup_module.sh napdatabase
```

## Create User Module {#user_module_creation}

Follow the steps below to create a new module named `MyFirstModule`:

1. Open a terminal
2. Change into your NAP framework directory
3. Create the module
```
./tools/create_module.sh MyFirstModule
```

The module will be created in `modules/napMyFirstModule`. This directory contains your module source-code, assets and build instructions. This module is *not* app specific and can be added to every NAP application.

### Include {#user_module_include}

Add `napMyFirstModule` to the list of [RequiredModules](@ref app_config_modules) of your app or module to include it in your project.

## Configure User Module {#user_module_config}

Within each module folder you'll find the `module.json` file. This file defines various module specific settings, such as which modules it depends upon and which third-party library search paths to use.

### External Modules {#user_module_config_modules}

You can add dependencies to your module by modifying the `RequiredModules` property in  `module.json`. The module name should match the module directory name in `/system_modules` or `/modules`. For example: add *napaudio* to add audio functionality or *napmidi* to add mini functionality to your application.

**Run `./regenerate.sh` inside your application folder to update the solution if your application uses the configured module](). Always run this script after making changes to `app.json` or `module.json`**

### Library Search Paths {#user_module_config_search_paths}

A target that links to a NAP module, that depends on a third-party dynamic library, must know where to find it. Modify the `LibrarySearchPaths` property in `module.json` to add library search paths to any target (executable or module) that includes your module: 
```
"LibrarySearchPaths": {
    "Linux": [
        "{ROOT}/system_modules/napfont/thirdparty/freetype/linux/{BUILD_ARCH}/lib"
    ],
    "macOS": [
        "{ROOT}/system_modules/napfont/thirdparty/freetype/macos/{BUILD_ARCH}/lib"
    ]
}
```
This tells the build system to add the (above-mentioned) paths as [rpaths](https://en.wikipedia.org/wiki/Rpath) to any target that includes the *napfont* system module, based on the build configuration and NAP root directory. 

*Note that the `Windows` element of `LibrarySearchPaths` is currently not used. It will however, in a future version of NAP, replace the deprecated [WindowsDllSearchPaths](@ref user_module_config_dll_search). It is therefore recommended to already provide it.* 

### Windows DLL Search Paths {#user_module_config_dll_search}

This section only applies to Windows. If your module links to a dynamic (third party) library NAP must be made aware of where it can find it. Otherwise, Napkin won't be able to open the project because it cannot load the third-party library requested by your module.

You can tell the system where to attempt to find the li**brary by modifying the `WindowsDllSearchPaths` property in `module.json`. Take as an example the `module.json` of *napfont* in `system_modules`:
```
"WindowsDllSearchPaths": [
    "{ROOT}/system_modules/napfont/thirdparty/freetype/msvc/{BUILD_ARCH}/lib/Release",
    "{ROOT}/system_modules/napfont/thirdparty/freetype/msvc/{BUILD_ARCH}/lib/Debug"
],
```

This entry tells NAP to look for the `freetype.dll` (on which *napfont* depends) in the above-mentioned directories, both relative to the NAP root. Depending on the current build configuration the system will load either the Debug or Release version.

*Note that in a future version of NAP the `WindowsDllSearchPaths` property will be deprecated and replaced by the `Windows` element of [LibrarySearchPaths](@ref user_module_config_search_paths)*

## Share Your Module {#user_module_sharing}

You can share your module with others on [modules.nap.tech](https://modules.nap.tech). A typical module has the following content, which will be included when the module is shared:

| Content                 | Directory  | Required |
|:------------------------|------------|----------|
| source code             | src        | yes      |
| thirdparty dependencies | thirdparty | no       |
| demo application        | demo       | no       |

### Prepare

Run `tools/prepare_module_to_share` with as the input argument the module you want to share, for example:

```
cd tools
./prepare_module_to_share.sh MyFirstModule
```

This prepares a **copy** of the `MyFirstModule` module that is optimized for sharing. The copy of the module is moved next to the nap root. Add the --help flag for more information about the available options.

### Upload

Upload the contents of your module to a service of your liking, for example [Github](https://github.com) or [Gitlab](https://gitlab.com).

### Share

Share your module on [modules.nap.tech](https://github.com/napframework/nap-modules) by following the [registration procedure](https://github.com/napframework/nap-modules#register-your-module) in the readme.

# Custom CMake {#custom_cmake}

We've focused on providing a streamlined build environment for people to start making projects and modules, along with trying out some demos. However, we've also provided some extensibility in the <a href="https://cmake.org/" target="_blank">CMake</a> system for people who would like to take things a little further.

CMake itself is vast and complex system and far beyond the scope of this document but we look forward to hearing from you and getting feedback on limitations reached with the current hooks we've provided for custom CMake logic.

Included below is information on how to add custom CMake logic to your projects and modules, a preview into the world of including third party dependencies cross platform through to packaging with projects, plus a little something extra for those who need even more flexibility.

## Application {#custom_cmake_app}

You can add additional CMake logic at the application level by providing an `app_extra.cmake` file in the root of the application directory. If `app_extra.cmake` exists its content will be included into the application template when the solution is regenerated.  

Within `app_extra.cmake` `${PROJECT_NAME}` can be used as in any standard CMake project and `${NAP_ROOT}` points to the root of the NAP installation. Below is an example of a simple `app_extra.cmake` with an added include path:
```
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_LIST_DIR}/pathToHeaders)
```

In this example <a href="https://cmake.org/cmake/help/v3.6/command/target_include_directories.html" target="_blank">target_include_directories</a> is used with `${PROJECT_NAME}` referring to the project target and `CMAKE_CURRENT_LIST_DIR` being used to refer to the application root directory. It's important to remember that `app_extra.cmake` is included within NAP's existing CMake project and as such doesn't replace the existing template. As a result this limits what functions make sense within this supplementary file.

In rare cases it might be desirable to execute extra logic before the target is defined. A hook for that has been provided via `app_extra_pre_target.cmake`.

**Note that the `CMakeLists.txt` file within the application root should not be modified. It is automatically generated by the build system and will be overwritten when the solution is regenerated.**

### Installation Rules

When an application is packaged the entire `data` directory from the app is included, alongside the core libraries, the modules and their third party dependencies.  If you need to include anything extra into the packaged project do so using CMake's [install](https://cmake.org/cmake/help/latest/command/install.html) command.  Below is an example `app_extra.json` that install an extra file `example.txt` from the application root into the packaged application.

```
install(FILES ${CMAKE_CURRENT_LIST_DIR}/example.txt DESTINATION .)
```

## Module {#custom_cmake_module}

You can add additional CMake logic at the user module level by providing an `module_extra.cmake` file in the root of the module directory, similar to [app_extra.cmake](@ref custom_cmake_app). If `module_extra.cmake` exists its content will be included into the module template when the solution is regenerated.

## Third Party Dependencies {#custom_cmake_thirdparty}

This section explains how to add a third-party dependency to your module using the [module_extra.cmake](@ref custom_cmake_module) file. The same steps apply when adding a third-party dependency directly to your application, substituting `module_extra.cmake` with `app_extra.cmake`. We're going to use [CMake modules](https://cmake.org/cmake/help/book/mastering-cmake/chapter/Modules.html) for this. Although other options are available, this is the preferred method.

Let's add an imaginary (pre-built) dynamic library called `libfoo` to `napMyFirstModule`. All third-party dependencies are stored in the `thirdparty` directory directly under the project (module or app) root, in this case:
```
napMyFirstModule/thirdparty/libfoo
```

The first step for including `libfoo` will be to make (or import) a `CMake module file`. This file defines and exposes all the pieces of information you need to include the `libfoo` in your project. Many third party libraries will come with one ready for you to use, but we're going to create a simple one from scratch.

Create a `cmake_find_modules` directory inside the `thirdparty` directory:
```
napMyFirstModule/thirdparty/cmake_find_modules
```

Within the directory create a file called `Findfoo.cmake` and add the following content:
```
# Allows us to change lookup based on system architecture
include(${NAP_ROOT}/cmake/targetarch.cmake)
target_architecture(ARCH)

# Define libfoo directory
# Note: it's better to use find_path() instead of defining it directly. 
set(FOO_DIR ${NAP_ROOT}/modules/napMyFirstModule/thirdparty/libfoo)

# Setup paths using library directory
if(WIN32)
    set(FOO_INCLUDE_DIRECTORIES ${FOO_DIR}/msvc/${ARCH}/include/libfoo.h)
    set(FOO_LIBS_DIR ${FOO_DIR}/msvc/${ARCH}/bin)
    set(FOO_LIBS ${FOO_LIBS_DIR}/libfoo.lib)
    set(FOO_LIBS_DLL ${FOO_LIBS_DIR}/libfoo.dll)
endif()

# Hide from CMake GUI
mark_as_advanced(FOO_DIR)
mark_as_advanced(FOO_LIBS_DIR)

# Standard find package handling
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(foo REQUIRED_VARS FOO_DIR FOO_LIBS FOO_INCLUDE_DIRECTORIES)

# Setup our shared import library
add_library(libfoo SHARED IMPORTED)

# Set shared library and include directory on our import library
set_target_properties(foo PROPERTIES
                      IMPORTED_CONFIGURATIONS "Debug;Release"
                      IMPORTED_LOCATION_RELEASE ${FOO_LIBS_DLL}
                      IMPORTED_LOCATION_DEBUG ${FOO_LIBS_DLL}
                      )
                      
# Add Windows import library properties
if(WIN32)
    set_target_properties(foo PROPERTIES
                          IMPORTED_IMPLIB_RELEASE ${FOO_LIBS}
                          IMPORTED_IMPLIB_DEBUG ${FOO_LIBS}
                          )
endif()
```

It's time to add `libfoo` to `napMyFirstModule`. Create a file called `module_extra.cmake` in the root of the module directory (if it doesn't exist already) and add the following content:

```
# Find the package
if(NOT TARGET libfoo)
    find_package(libfoo REQUIRED)
endif()

# Add foo includes
target_include_directories(${PROJECT_NAME} PRIVATE ${FOO_INCLUDE_DIRECTORIES})

# Link in foo libraries
target_link_libraries(${PROJECT_NAME} PRIVATE libfoo)

if(WIN32)
    # Add post-build step to copy libfoo to bin on Windows
    add_custom_command(TARGET ${PROJECT_NAME}
                       POST_BUILD
                       COMMAND ${CMAKE_COMMAND} 
                               -E copy
                               $<TARGET_FILE:libfoo>
                               $<TARGET_FILE_DIR:${PROJECT_NAME}> 
                       )
endif()
```

So what did we do here? [find_package](https://cmake.org/cmake/help/latest/command/find_package.html) locates and imports the `libfoo` library into our project. We then include it with `target_include_directories` and link to it with `target_link_libraries`. Finally, to ensure the program runs on Windows we copy the DLL to the build output directory using a [custom build command](https://cmake.org/cmake/help/latest/command/add_custom_command.html).

The last consideration is to ensure the third party shared library is installed in the packaged application. Due to the fact that we've already copied the DLL to the project bin directory on Windows we've already completed that step there. However, if you're supporting macOS and Linux you need to add this as a step using CMake's [install](https://cmake.org/cmake/help/latest/command/install.html) command.  In that case append the following to `module_extra.cmake`, noting that we're installing the library into the `lib` directory within the package:
```
if(UNIX)
    # Install libfoo into lib directory in packaged project on macOS and Linux
    install(FILES $<TARGET_FILE:foo> DESTINATION lib)
endif()
```

### macOS RPATH Management {#macos_thirdparty_library_rpath}

One thing to keep an eye out for on macOS is the install name of the third party libraries that you're attempting to integrate.

The install name of a shared library can be viewed in macOS using the command `otool -D`. See this example, showing mpg123:
```
$ otool -D lib/libmpg123.0.dylib
lib/libmpg123.0.dylib:
/Users/username/mpg123-1.25.6/install/osx/lib/libmpg123.0.dylib
```

If that install name were allowed to remain this way any library linked against libmpg123.0.dylib would look for it at the path shown above. What we want to end up with instead is having our library found in its relative position within the NAP framework directory.

To achieve that let's update the library's install name, prefixing it with `@rpath`:
```
$ install_name_tool -id @rpath/libmpg123.0.dylib lib/libmpg123.0.dylib
```

We can then check the results by running `otool` again:
```
$ otool -D lib/libmpg123.0.dylib
lib/libmpg123.0.dylib:
@rpath/libmpg123.dylib
```

Anything using our library with the updated install name (in this case mpg123) would then need to be rebuilt to pull in the changed path.

One risk with RPATH management and third party libraries is in the case where you're integrating a library that you also have installed on your system via eg. Homebrew or MacPorts. In this case it's possible to unknowningly be building and running against the system-level third party library. There are a number of ways to detect this, one of which is while running your project using `lsof` in a terminal and grepping the output to ensure that the correct instance of your library is being used. If this issue goes unresolved you're likely to run into problems when the project or module is used on a another system.

# Path Mapping System {#path_mapping}

NAP uses a path mapping system based on simple JSON files to manage the directory relationships between the project binaries, Napkin and modules in the different arrangements of working against a Framework Release, from a Packaged App, or even against Source. The path mapping for the platform and context you're using will be deployed by the build system to `cache/path_mapping.json` relative to both the project directory and the project binary output.

In the very large majority of cases NAP will manage these paths for you and you won't need to pay attention to this system. There is however a provision for custom project-specific path mappings which get pulled in from the directory `config/custom_path_mappings` within the project directory, containing content similar to `tools/platform/path_mappings` in the Framework Release. Only the platforms and contexts you want to modify should be defined. NAP will locate these custom mappings and deploy them as expected. 

Custom path mappings are fairly beta at this stage and if you end up finding a need for them we would be interested in hearing from you, feel free to get in touch on the forum.