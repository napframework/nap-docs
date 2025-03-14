Installation {#install}
=======================

*	[Overview](@ref build_env_overview)
*	[Development Environments](@ref ides)
*	[Windows](@ref win64)
	*	[Setup Your Build Environment](@ref setup_build_env_win64)
	*	[Run Your First Demo](@ref run_demo_win64)
*	[Linux](@ref linux) 
	*	[Desktop](@ref linux_desktop)
	*	[Raspberry Pi](@ref linux_pi)
	*	[Display Server](@ref linux_ds)
	*	[Setup Your Build Environment](@ref setup_build_env_linux)
	*	[Run Your First Demo](@ref run_demo_linux)

# Overview {#build_env_overview}

Installing the NAP release involves extracting the archive and running our script to guide you through dependency installation. Projects reside within the framework folder structure, and as such we recommend extracting the release into a user directory instead of a system directory. For example on Windows something like `My Documents` is a more suitable location than `C:\\Program Files.`

The prerequisites installation script is called `check_build_environment` and can be found in the tools directory within the release.  The script attempts to verify that your build environment is ready for NAP and is designed to be re-run until all checks are successfully passed.

# Development Environments {#ides}

NAP $(NAP_VERSION_FULL) supports `Visual Studio 2019 & 2022` on Windows and `make files` on Linux. Instead of using these environments you can use [Visual Studio Code](https://code.visualstudio.com/) or [CLion](https://www.jetbrains.com/clion) to author your code. Although we don't officially support these environments others have confirmed that they work as expected. Both `Visual Studio Code` and `CLion` can be configured using CMake, which is the system NAP uses to build and package applications.

# Windows {#win64}

## Setup Your Build Environment {#setup_build_env_win64}

NAP $(NAP_VERSION_FULL) supports `Windows 10 & 11 (x86_64)` with `Visual Studio 2019 or 2022`.

Download and install <a href="https://visualstudio.microsoft.com/downloads/" target="_blank">Visual Studio 2022</a>. This link points to the community edition which can be used for free. Make sure to select `Desktop development with C++` when installing Visual Studio, including `MSVC v143 - VS 2022 C++ x64/x86` and the `Windows 10 SDK`. Other settings are optional.

1. Extract `NAP-$(NAP_VERSION_FULL)-Win64-x86_64.zip` using Explorer (or your preferred tool)
2. In `NAP-$(NAP_VERSION_FULL)-Win64-x86_64\tools` run `check_build_environment.bat` to guide you through installing prerequisites, following the instructions

## Run Your First Demo {#run_demo_win64}

1. Navigate to `NAP-$(NAP_VERSION_FULL)-Win64-x86_64\demos\helloworld` in Explorer
2. Run `regenerate.bat`
3. Open the generated Visual Studio solution (shown in Explorer)
4. Select the `Release` configuration
5. Click the run button

# Linux {#linux}

## Desktop {#linux_desktop}

NAP $(NAP_VERSION_FULL) supports `Ubuntu Linux 22.04 & 24.04` on `x86-64` machines using `GCC`. Although NAP is known to run on other distros: `Ubuntu` is currently the only supported Linux desktop environment.

## Raspberry Pi {#linux_pi}

Only the `Raspberry Pi 4 & 5` running `Raspbian bookworm (v12, arm64)` is 'fully' supported. Headless applications and services without graphics should run on older models, although this has not been tested. Please note that although most demos work fine, we did run into minor render issues with the `heightmap` and `computeflocking` demos. Using a more recent (upstream) driver improved overall performance and resolved most known render issues.

## Display Server {#linux_ds}

When `Wayland` is configured as the display server, NAP applications and Napkin (the editor) will rely on `XWayland` for compatibility. It is recommended to use `X11` instead of Wayland until Wayland is (fully) supported.

## Setup Your Build Environment {#setup_build_env_linux}

1. Extract the release:
```
tar jxvf NAP-0.*.tar.bz2
```
2. Run the `check_build_environment` script to guide you through installing prerequisites, following the instructions:
```
cd NAP-0.*
./tools/check_build_environment
```
3. If any changes are required re-run `check_build_environment` after those changes have been made to verify the final environment

## Run Your First Demo {#run_demo_linux}

1. Navigate to the helloworld demo
```
cd demos/helloworld
```
2. Generate the Unix makefiles and build the solution
```
./build.sh
```
3. Run the demo
```
cd bin/GNU-Release-*
./helloworld
```