#!/usr/bin/env python3
from lilaclib import *

pkgns = SimpleNamespace()

def pre_build():
    pkgns.files = download_official_pkgbuild('qt5-declarative')

    for line in edit_file('PKGBUILD'):
        if line.startswith('pkgname=qt5-declarative'):
            print('pkgname=qt5-declarative-gles')
            line = '_' + line
        elif line.startswith('arch='):
            line = "arch=('aarch64')"
        elif line.startswith('depends='):
            line = line.replace('qt5-base', 'qt5-base-gles')
        elif line.startswith('groups='):
            continue
        elif line.startswith('conflicts='):
            print('provides=("$_pkgname")')
            line = 'conflicts=("$_pkgname" "qtchooser")'
        elif 'pkgname' in line:
            line = line.replace('pkgname', '_pkgname')

        print(line)

def post_build():
    git_add_files('PKGBUILD')
    git_commit()

if __name__ == '__main__':
    single_main()
