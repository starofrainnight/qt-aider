
import os
import sys
import click
from distutils.version import LooseVersion


@click.command()
@click.argument('python_version')
def main(python_version):
    """Install Qt packages for python with specific version
    """

    python_version = LooseVersion(python_version)
    if sys.platform.startswith('linux'):
        # Install prebuilded pyside from qt.io
        os.system('%s -m pip install --index-url=http://download.qt.io/snapshots/ci/pyside/5.9/latest/ pyside2 --trusted-host download.qt.io' % sys.executable)
    elif sys.platform.startswith('win32'):
        if python_version < LooseVersion('3.5'):
            os.system('%s -m pip install PySide' % sys.executable)
        else:
            os.system('%s -m pip install PyQt5' % sys.executable)


if __name__ == '__main__':
    main()
