#!/usr/bin/env python3

import os, sys
import argparse

from .dependencies import Dependency
from .platforms import PlatformInfo
from .builder import Builder
from .utils import setup_print_progress

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('targets', default='kiwix-tools', nargs='?', metavar='TARGET',
                        choices=Dependency.all_deps.keys())
    parser.add_argument('--working-dir', default=".")
    parser.add_argument('--libprefix', default=None)
    parser.add_argument('--target-platform', default="native_dyn", choices=PlatformInfo.all_platforms)
    parser.add_argument('--verbose', '-v', action="store_true",
                        help=("Print all logs on stdout instead of in specific"
                              " log files per commands"))
    parser.add_argument('--hide-progress', action='store_false', dest='show_progress',
                        help="Hide intermediate progress information.")
    parser.add_argument('--skip-source-prepare', action='store_true',
                        help="Skip the source download part")
    parser.add_argument('--build-deps-only', action='store_true',
                        help="Build only the dependencies of the specified targets.")
    parser.add_argument('--build-nodeps', action='store_true',
                        help="Build only the target, not its dependencies.")
    parser.add_argument('--make-dist', action='store_true',
                        help="Build distrubution (dist) source archive")
    parser.add_argument('--make-release', action='store_true',
                        help="Build a release version")
    subgroup = parser.add_argument_group('advanced')
    subgroup.add_argument('--no-cert-check', action='store_true',
                          help="Skip SSL certificate verification during download")
    subgroup.add_argument('--clean-at-end', action='store_true',
                          help="Clean all intermediate files after the (successfull) build")
    subgroup.add_argument('--force-install-packages', action='store_true',
                          help="Allways check for needed packages before compiling")
    subgroup = parser.add_argument_group('custom app',
                                         description="Android custom app specific options")
    subgroup.add_argument('--android-custom-app',
                          help="The custom android app to build")
    subgroup.add_argument('--zim-file-url',
                          help="The url of the zim file to download")
    subgroup.add_argument('--zim-file-size',
                          help="The size of the zim file.")
    options = parser.parse_args()

    if options.targets == 'kiwix-android-custom':
        err = False
        if not options.android_custom_app:
            print("You need to specify ANDROID_CUSTOM_APP if you "
                  "want to build a kiwix-android-custom target")
            err = True
        if not options.zim_file_url and not options.zim_file_size:
            print("You need to specify ZIM_FILE_SIZE or ZIM_FILE_URL if you "
                  "want to build a kiwix-android-custom target")
            err = True
        if err:
            sys.exit(1)
    return options

def main():
    options = parse_args()
    options.working_dir = os.path.abspath(options.working_dir)
    setup_print_progress(options.show_progress)
    builder = Builder(options)
    builder.run()

