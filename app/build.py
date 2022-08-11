#!/usr/bin/env python3
import os
import subprocess
from sys import platform
import shutil
import distutils.dir_util
import shutil
import sys

NAP_DIR = "../nap"
BUILD_DIR = "../build"
OUTPUT_DIR = "/" + BUILD_DIR + "/html"
CONFIG_FILE = "/nap.clang-format"
CONTENT_DIR = "/content"
SEARCH_SOURCE = "/css/search.css"
FONT_FILE_SOURCE = "/css/Manrope-Regular.ttf"
MONO_FONT_FILE_SOURCE = "/css/Inconsolata-Medium.ttf"
OVERRIDE_DIR = "/overrides"
MONO_FONT_FILE_TARGET = OUTPUT_DIR + "/Inconsolata-Medium.ttf"
FONT_FILE_TARGET = OUTPUT_DIR + "/Manrope-Regular.ttf"
SEARCH_TARGET = OUTPUT_DIR + "/search/search.css"

# errors
ERROR_INVALID_NAP_VERSION = 2


def call(cwd, cmd):
    print('dir: %s' % cwd)
    print('cmd: %s' % cmd)
    proc = subprocess.Popen(cmd, cwd=cwd, shell=True)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise Exception(proc.returncode)
    return out


def call_collecting_output(cwd, cmd):
    print('dir: %s' % cwd)
    print('cmd: %s' % cmd)
    proc = subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise Exception(proc.returncode)
    return out


# working dir = dir script resides in
def get_working_dir():
    return os.path.dirname(os.path.realpath(__file__))


# absolute path to nap directory
def get_nap_dir():
    rel_dir = "{0}/{1}".format(get_working_dir(), NAP_DIR)
    if not os.path.exists(rel_dir):
        raise Exception("Directory {0} does not exist".format(rel_dir))
    return os.path.abspath(rel_dir)


# absolute path to the build directory
def get_build_dir():
    return os.path.abspath("{0}/{1}".format(get_working_dir(), BUILD_DIR))


# path to doxygen executable, should be installed by homebrew or apt when running
# linux / osx. Binary is bundled for windows in repo
def get_doxygen_path():
    if platform in ["linux", "linux2", "darwin"]:
        return "doxygen"

    # windows
    doxy_path = get_working_dir() + "/bin/doxygen.exe"
    if not os.path.exists(doxy_path):
        raise Exception("can't find doxygen executable: " + doxy_path)
    return doxy_path


# path to doxygen config file
def get_doxygen_config_file():
    doxy_conf = get_working_dir() + CONFIG_FILE
    if not os.path.exists(doxy_conf):
        raise Exception("can't find doxygen configuration file: " + doxy_conf)
    return doxy_conf


# copy content
def copy_content():
    source = get_working_dir() + CONTENT_DIR
    target = get_working_dir() + OUTPUT_DIR + CONTENT_DIR
    print("copy: %s -> %s" % (source, target))
    try:
        distutils.dir_util.copy_tree(source, target)
    except Exception as error:
        print("unable to copy content, are you running as admin? %s" % error)


# copy overrides
def copy_overrides():
    source = get_working_dir() + OVERRIDE_DIR
    target = get_working_dir() + OUTPUT_DIR
    print("copy: %s -> %s" % (source, target))
    try:
        distutils.dir_util.copy_tree(source, target)
    except Exception as error:
        print("unable to copy overrides, are you running as admin? %s" % error)


# copy search window
def copy_search():
    source = get_working_dir() + SEARCH_SOURCE
    target = get_working_dir() + SEARCH_TARGET
    print("copy: %s -> %s" % (source, target))
    try:
        shutil.copyfile(source, target)
    except Exception as error:
        print("unable to copy search stylesheet, are you running as admin? %s" % error)


# copy font
def copy_font(source, target):
    font_source = get_working_dir() + source
    font_target = get_working_dir() + target
    print("copy: %s -> %s" % (font_source, font_target))
    try:
        shutil.copyfile(font_source, font_target)
    except Exception as error:
        print("unable to copy font, are you running as admin? %s" % error)


def populate_env_vars():
    """Populate NAP framework version from cmake/version.cmake to environment variables NAP_VERSION_FULL and
    NAP_VERSION_MAJOR """

    # Fetch version from version.cmake
    version_file = os.path.join(get_nap_dir(), 'cmake/version.cmake')
    version_unparsed = call_collecting_output(get_working_dir(), 'cmake -P %s' % version_file)
    chunks = version_unparsed.decode('ascii', 'ignore').split(':')

    if len(chunks) < 2:
        raise Exception("Error passing invalid output from version.cmake: %s" % version_unparsed)

    version = chunks[1].strip()
    os.environ["NAP_VERSION_FULL"] = version
    os.environ["NAP_VERSION_MAJOR"] = '.'.join(version.split('.')[:-1])
    os.environ["NAP_WORKING_DIR"] = get_nap_dir()
    os.environ["NAP_BUILD_DIR"] = get_build_dir()


# main run
if __name__ == '__main__':
    # find doxygen executable
    doxy_path = get_doxygen_path()

    # find doxygen exe script
    doxy_conf = get_doxygen_config_file()

    # create subprocess arguments
    doxy_arg = "%s %s" % (doxy_path, doxy_conf)

    # populate NAP framework version from cmake/version.cmake to environment variables NAP_VERSION_FULL (eg. 0.1.0)
    # and NAP_VERSION_MAJOR (eg. 0.1) accessible in doxygen manual like $(NAP_VERSION_FULL), $(NAP_VERSION_MAJOR)
    populate_env_vars()

    # generate docs
    call(get_working_dir(), doxy_arg)

    # copy content
    copy_content()

    # copy search
    copy_search()

    # copy overrides
    copy_overrides()

    # copy fonts
    copy_font(FONT_FILE_SOURCE, FONT_FILE_TARGET)
    copy_font(MONO_FONT_FILE_SOURCE, MONO_FONT_FILE_TARGET)
