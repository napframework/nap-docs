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
CONFIG_FILE = "nap.clang-format"

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


# get absolute path to the build output html dir, not required to exist
def get_output_dir():
    return "{0}/html".format(get_build_dir(), BUILD_DIR)


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
    config_file = "{0}/{1}".format(get_working_dir(), CONFIG_FILE)
    if not os.path.exists(config_file):
        raise Exception("can't find doxygen configuration file: " + config_file)
    return config_file


# copy content
def copy_directory(source, target):
    print("copy:{0} -> {1}".format(source, target))
    distutils.dir_util.copy_tree(source, target)


# copy file
def copy_file(source, target):
    print("copy: %s -> %s" % (source, target))
    shutil.copyfile(source, target)


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

    # delete build output
    shutil.rmtree(get_build_dir())

    # generate docs
    call(get_working_dir(), doxy_arg)

    # copy content
    copy_directory("{0}/content".format(get_working_dir()),
                   "{0}/content".format(get_output_dir()))

    # copy search
    copy_file("{0}/css/search.css".format(get_working_dir()),
              "{0}/search/search.css".format(get_output_dir()))

    # copy overrides
    copy_directory("{0}/overrides".format(get_working_dir()),
                   get_output_dir())

    # copy regular font
    copy_file("{0}/css/Manrope-Regular.ttf".format(get_working_dir()),
              "{0}/Manrope-Regular.ttf".format(get_output_dir()))

    # copy mono font
    copy_file("{0}/css/Inconsolata-Medium.ttf".format(get_working_dir()),
              "{0}/Inconsolata-Medium.ttf".format(get_output_dir()))
