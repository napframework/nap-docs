# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#!/usr/bin/env python3
import os
import subprocess
import distutils.dir_util
import shutil
from git_repo import Repository
import argparse

NAP_DIR = "../nap"
BUILD_DIR = "../build"
DOCS_DIR = "../docs"
CONFIG_FILE = "nap.clang-format"
NAP_REPO = "https://github.com/napframework/nap.git"


# run process
def call(cwd, cmd):
    print('dir: %s' % cwd)
    print('cmd: %s' % cmd)
    proc = subprocess.Popen(cmd, cwd=cwd, shell=True)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise Exception(proc.returncode)
    return out


# collect output from proc
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
    return os.path.abspath(rel_dir)


# absolute path to the build directory
def get_build_dir():
    return os.path.abspath("{0}/{1}".format(get_working_dir(), BUILD_DIR))


# get absolute path to the build output html dir, not required to exist
def get_output_dir():
    return "{0}/html".format(get_build_dir(), BUILD_DIR)


# get absolute path to (hosted) docs directory
def get_docs_dir():
    rel_path = "{0}/{1}".format(get_working_dir(), DOCS_DIR)
    return os.path.abspath(rel_path)


# get absolute path to root directory
def get_root_dir():
    rel_path = "{0}/..".format(get_working_dir())
    return os.path.abspath(rel_path)


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
    """
    Generate nap tech documentation using Doxygen.
    Output is stored in the /docs directory.
    Intermediate build info is stored in /build directory
    """

    # options
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--push-changes', action="store_true", help="Push changes to remote")
    args = parser.parse_args()

    # clone NAP and pull
    nap_repo = Repository(get_nap_dir(), NAP_REPO)
    nap_repo.pull()

    # populate NAP framework version from cmake/version.cmake to environment variables NAP_VERSION_FULL (eg. 0.1.0)
    # and NAP_VERSION_MAJOR (eg. 0.1) accessible in doxygen manual like $(NAP_VERSION_FULL), $(NAP_VERSION_MAJOR)
    populate_env_vars()

    # delete build dir
    if os.path.exists(get_build_dir()):
        shutil.rmtree(get_build_dir())

    # delete output dir
    if os.path.exists(get_docs_dir()):
        shutil.rmtree(get_docs_dir())

    # generate docs
    call(get_working_dir(), "doxygen {0}".format(get_doxygen_config_file()))

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

    # copy html contents of build step to docs
    print("move:{0} -> {1}".format(get_output_dir(), get_docs_dir()))
    shutil.move(get_output_dir(), get_docs_dir())

    # copy cname file
    copy_file("{0}/CNAME".format(get_working_dir()), "{0}/CNAME".format(get_docs_dir()))
