Project Management {#project_management}
=======================

*	[Overview](@ref proj_overview) 
*	[Create Project](@ref proj_creation)
*	[Configure Modules](@ref module_config)
*	[Create Shared Module](@ref module_creation)
*   [Create Project Module](@ref project_module_creation)
*	[Package Project For Release](@ref package_linux)
*	[Custom CMake](@ref custom_cmake)
	*	[Project](@ref custom_cmake_proj)
	*	[Module](@ref custom_cmake_module)
	*	[Third Party Dependencies](@ref custom_cmake_thirdparty)
		*	[macOS RPATH Management](@ref macos_thirdparty_library_rpath)
*	[Path Mapping System](@ref path_mapping)

# Overview {#proj_overview}

This document explains how to create, maintain and share a NAP project or module. Although a typical NAP project is an application, it doesn't have to be: it can also be a service or library. That's why we refer to it as a project instead of an application in this document.

All project management utilities reside in the `tools` directory under the NAP root. Convenience shortcuts to regenerate the solution and package the application also sit within each project. We'll go over the basic tasks here and then cover some more advanced topics in the [Custom CMake](@ref custom_cmake) section for those who want to take things further.

We will use the *unix* shell syntax in this document, for convenience and readability. If you're on Windows and using the prompt, simply replace `./*.sh` with `*.bat`. Any exception to this rule will be clearly documented.

*This document assumes you are working from a pre-compiled distributable NAP package. However, some people prefer working with NAP directly from source. Fortunately most instructions in this document are the same for both contexts, except some paths. Additional information is provided when this is the case.*

## Create Project {#proj_creation}

Follow these steps to create a new project titled `MyFirstApp`.

1. Open a terminal
2. Browse to the NAP framework directory
3. Create the project
```
./tools/create_app.sh MyFirstApp
```

The project will be located in `apps/MyFirstApp`. This directory contains your application source-code, assets, makefiles (Linux) or visual studio solution (Windows) and build instructions.

Within each project folder you'll find the `app.json` file which defines various project specific settings, such as: the name of your app , which modules to include and which content to load:

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

### The Project Module

The most important module here is `napMyFirstApp`. This is your **application module**, located in the `module` directory of your project. This directory contains the [resources](@ref resources) and [components](@ref component_ov) that are specific to your project. This module is created and added by the build system when the project is created. You can omit the creation of this module by appending `--no-module` to `tools/create_app.sh`.


## Configure Modules {#module_config}

You can add modules to your project by modifying the `RequiredModules` property in of `app.json`. The module name should match the module directory name in `/system_modules` or `/modules`. For example: add *napaudio* to add audio functionality to your project or *napmidi* to add mini functionality to your project. These modules are part of the core release and located in `/system_modules`. [Shared modules](@ref module_creation) are stored in `/modules`.

**Run `./regenerate.sh` inside your project folder to update the solution. Always run this script after making changes to `app.json`.**

## Create Shared Module {#module_creation}

Follow the steps below to create a shared module named `MyFirstModule`.
1. Open a terminal
2. Change into your NAP framework directory
3. Create the module
```
./tools/create_module MyFirstModule
```

The module will be created in `modules/napMyFirstModule`. This directory contains your module source-code, assets and build instructions. This module is *not* project specific and can be included in every NAP application.

To include this module in your project add `napMyFirstModule` to the list of [RequiredModules](@ref module_config). 


## Create Project Module {#project_module_creation}

Unlike the shared module created in the previous section, a project module is specific to a single project. Working with a project module has the benefit of containing all code related to the project within the project's directory whilst retaining the ability to create components which can be worked on via Napkin and integrated into your project structure.

**Note that by default the project module is always created and included when you [create a new project](@ref proj_creation), unless explicitly omitted using the `--no-module` during project creation.**


Follow the steps below to add a project module to `MyFirstApp`.
1. Open a command prompt
2. Change into your NAP framework directory
3. Create the module
```
./tools/create_project_module MyFirstProject
```

The module will be created in `apps/MyFirstApp/module` and added to your `app.json`.

## Package Project For Release {#package_linux}

Packaging a project provides an archive containing the project, its data, all required libraries and optionally Napkin.  In the NAP beta release projects are packaged to XZipped tarballs which when extracted provide for direct access to the project data and JSON, allowing for easy editing once deployed.  Options for creating installers for projects may be explored for a future NAP release.  At this time all packaged projects use release build configuration.

Packaging a project with default settings:
1. Navigate to your project
```
cd projects/myfirstproject
```
2. Run package
```
./package
```

By default projects are compressed and contain Napkin.  Projects can be left uncompressed in a folder by adding the option `--no-zip`.  Napkin can be left out via `--no-napkin`.  Excluding Napkin can save a considerable amount of space if you don't intend on using it.  Other minor options and shorthand versions of the options above can be viewed by running `package --help`.

Project packaging is also accessible from by command prompt in the NAP root via the command `./tools/package_project PROJECT_NAME`.  The same options as above apply.

# Custom CMake {#custom_cmake}

For the NAP beta release we've focused on providing a streamlined environment for people to start making projects and modules against the framework along with of course some testing out of the demos.  However we've also provided some extensibility in the <a href="https://cmake.org/" target="_blank">CMake</a> system for people who would like to take things a little further.

CMake itself is vast and complex system and far beyond the scope of this document but we look forward to hearing from you and getting feedback on limitations reached with the current hooks we've provided for custom CMake logic.

Included below is information on how to add custom CMake logic to your projects and modules, a preview into the world of including third party dependencies cross platform through to packaging with projects, plus a little something extra for those who need even more flexibility.

## Project {#custom_cmake_proj}

Those looking to add extra CMake logic at the project level are able to via a hook provided with a `project_extra.cmake` file in the project root directory.

If `project_extra.cmake` exists it will be included into the project template when the solution is regenerated.  Within `project_extra.cmake` `${PROJECT_NAME}` can be used as in any standard CMake project and `${NAP_ROOT}` points to the root of the NAP installation.  `CMakeLists.txt` within the project root shouldn't be modified (and may be updated in future releases of NAP).

Below is an example of a simple `project_extra.cmake` with an added include path:
```
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_LIST_DIR}/pathToHeaders)
```

In this example <a href="https://cmake.org/cmake/help/v3.6/command/target_include_directories.html" target="_blank">target_include_directories</a> is used with `${PROJECT_NAME}` referring to the project target and `CMAKE_CURRENT_LIST_DIR` being used to refer to the project root directory.  It's important to remember that `project_extra.cmake` is included within NAP's existing CMake project and as such doesn't replace the existing template and as a result this limits what functions make sense within this supplementary file.

When a project is packaged the entire `data` directory from the project is included, alongside the core libraries, the modules and their third party dependencies.  If you need to include anything extra into the packaged project do so using CMake's <a href="https://cmake.org/cmake/help/v3.6/command/install.html" target="_blank">install</a> command.  Below is an example `project_extra.json` installing an extra file `example.txt` from the project root into the packaged project.

```
install(FILES ${CMAKE_CURRENT_LIST_DIR}/example.txt DESTINATION .)
```

## Module {#custom_cmake_module}

Similar to the [custom project CMake above](@ref custom_cmake_proj) NAP provides a hook for custom logic in user modules by the way of a `module_extra.cmake` file in the module root directory.

The same limitations and approaches apply to this supplementary CMake logic file as to `project_extra.cmake`: `${PROJECT_NAME}` identifies the module target, `CMakeLists.txt` shouldn't be replaced, and this file is included into our standard NAP module CMake project.

## Third Party Dependencies {#custom_cmake_thirdparty}

The focus here will be on including a new thirdparty dependency into a module but the same steps apply for including it instead directly into a project, substituting `module_extra.cmake` with `project_extra.cmake`.

The steps provided create a CMake module for the third party library, which we bring in as an import library.  There are other ways to implement this with CMake but we'll here be focused on an import library approach using a CMake module.

Let's work on with an imaginary libfoo that we want to bring into our user module mod_myfirstmodule.  We're going to keep the thirdparty library sitting alongside the module, but this is of course up to you.  Let's envisage that we have libfoo prebuilt for all three platforms as a shared library.

The first step for including a new third party library will be to make (or import) a CMake module file.  Many third party libraries will come with a CMake module ready for your use.  Below we're going to create a simple one from scratch.

Within the `cmake` directory in the NAP root create a CMake module file `Findfoo.cmake` with the following:

```
# Setup our fictional library paths
set(FOO_DIR ${NAP_ROOT}/user_modules/mod_myfirstmodule/thirdparty/libfoo)
set(FOO_INCLUDE_DIRECTORIES ${FOO_DIR}/include)
if (WIN32)
    set(FOO_LIBS_DIR ${FOO_DIR}/msvc/bin)
    set(FOO_LIBS ${FOO_LIBS_DIR}/libfoo.lib)
    set(FOO_LIBS_DLL ${FOO_LIBS_DIR}/libfoo.dll)
elseif(APPLE)
    set(FOO_LIBS_DIR ${FOO_DIR}/macos/bin)
    set(FOO_LIBS ${FOO_LIBS_DIR}/libfoo.dylib)
    set(FOO_LIBS_DLL ${FOO_LIBS})
else()
    set(FOO_LIBS_DIR ${FOO_DIR}/linux/bin)
    set(FOO_LIBS ${FOO_LIBS_DIR}/libfoo.so)
    set(FOO_LIBS_DLL ${FOO_LIBS})
endif()

# Hide from CMake GUI
mark_as_advanced(FOO_DIR)
mark_as_advanced(FOO_LIBS_DIR)

# Standard find package handling
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(foo REQUIRED_VARS FOO_DIR FOO_LIBS FOO_INCLUDE_DIRECTORIES)

# Setup our shared import library
add_library(foo SHARED IMPORTED)

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

Now let's add libfoo into our user module.

Create a file named `module_extra.cmake` in the root of your module directory containing the following:

```
if(NOT TARGET foo)
    find_package(foo REQUIRED)
endif()
set(MODULE_NAME_EXTRA_LIBS foo)

add_include_to_interface_target(mod_fooworker ${FOO_INCLUDE_DIRECTORIES})
```

CMake's <a href="https://cmake.org/cmake/help/v3.6/command/find_package.html" target="_blank">find_package</a> has been used to locate the module, populating `MODULE_NAME_EXTRA_LIBS` will link libfoo to the module and `add_include_to_interface_target` adds the include directory. The first parameter to `add_include_to_interface_target` should be the name of your module.

At this stage the library is now available to include and link on all platforms however if we attempt to run a project using the module on Windows the DLL won't be found.

Let's use a post-build command via <a href="https://cmake.org/cmake/help/v3.6/command/add_custom_command.html" target="_blank">add_custom_command</a> to copy the third party DLL into the project directory by adding the following into the `module_extra.cmake`:

```
if(WIN32)
    # Add post-build step to copy libfoo to bin on Windows
    add_custom_command(TARGET ${PROJECT_NAME}
                       POST_BUILD
                       COMMAND ${CMAKE_COMMAND} 
                               -E copy
                               $<TARGET_FILE:foo>
                               $<TARGET_FILE_DIR:${PROJECT_NAME}> 
                       )
endif()
```

Your module with its libfoo third party dependency will now build and run on all three platforms.

The last consideration is to ensure the third party shared library is include in the packaged project.  Due to the fact that we've already copied the DLL into the project bin directory on Windows we have already completed that step there.  However on macOS and Linux we need to add this as a step using CMake's <a href="https://cmake.org/cmake/help/v3.6/command/install.html" target="_blank">install</a> command.  Add the following to your `module_extra.cmake`, noting that we're installing the library into the `lib` directory within the package:
```
if(UNIX)
    # Install libfoo into lib directory in packaged project on macOS and Linux
    install(FILES $<TARGET_FILE:foo> DESTINATION lib)
endif()
```

In the end with a minor simplification your `module_extra.cmake` should look like this:
```
if(NOT TARGET foo)
    find_package(foo REQUIRED)
endif()
set(MODULE_NAME_EXTRA_LIBS foo)

add_include_to_interface_target(mod_fooworker ${FOO_INCLUDE_DIRECTORIES})

if(WIN32)
    # Add post-build step to copy libfoo to bin on Windows
    add_custom_command(TARGET ${PROJECT_NAME}
                       POST_BUILD
                       COMMAND ${CMAKE_COMMAND} 
                               -E copy
                               $<TARGET_FILE:foo>
                               $<TARGET_FILE_DIR:${PROJECT_NAME}> 
                       )
elseif(UNIX)
    # Install libfoo into the lib directory of packaged projects on macOS and Linux
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

If that install name were allowed to remain this way any library linked against libout123.0.dylib would look for it at the path shown above. What we want to end up with instead is having our library found in its relative position within the NAP framework directory.

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
