#!/usr/bin/env python3
from lilaclib import *

pkgns = SimpleNamespace()

def download_archlinuxarm_pkgbuild(folder: str, name: str) -> List[str]:
    url = 'https://api.github.com/repos/archlinuxarm/PKGBUILDs/contents/{}/{}'.format(folder, name)
    logger.info('download PKGBUILD for %s.', name)
    info = s.get(url).json()

    files = [(x['name'], x['download_url']) for x in info]

    for filename, download_url in files:
        with open(filename, 'wb') as f:
            logger.debug('download file %s.', filename)
            data = s.get(download_url).content
            f.write(data)
    return files

def pre_build():
    pkgns.files = download_archlinuxarm_pkgbuild('extra', 'qt5-base')

    for line in edit_file('PKGBUILD'):
        if line.startswith('pkgname='):
            line = line.replace('qt5-base', 'qt5-base-gles')
        elif line.startswith('groups='):
            continue
        elif line.startswith('arch='):
            line = "arch=('aarch64')"
        elif line.startswith('package_qt5-base'):
            line = line.replace('qt5-base', 'qt5-base-gles')
            line += '\n  provides=("$pkgbase")'
            line += '\n  conflicts=("$pkgbase")'
        elif line.count('-prefix /usr'):
            line += '\n    -opengl es2 \\'

        print(line)

def post_build():
    git_add_files('PKGBUILD')
    git_commit()

if __name__ == '__main__':
    single_main()

