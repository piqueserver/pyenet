
from setuptools import setup
from distutils.extension import Extension
from distutils.core import run_setup

import os
import glob
import sys
import re

source_files = ["enet.pyx"]

_enet_files = glob.glob("enet/*.c")
source_files.extend(_enet_files)

lib_version = "1.3.17"
package_version = lib_version


with open('README.rst') as f:
   long_description = re.sub(r'[^\x00-\x7F]+', ' ', f.read())


from distutils.command.build_ext import build_ext as _build_ext
class build_ext(_build_ext):
    def run(self):

        from Cython.Build import cythonize
        compiler_directives = {'language_level': 2}
        self.extensions = cythonize(self.extensions,
              compiler_directives=compiler_directives)

        _build_ext.run(self)

        extra_args = sys.argv[2:]
        run_setup(os.path.join(os.getcwd(), "setup.py"), ['build_py'] + extra_args)


define_macros = [('HAS_POLL', None), ('HAS_FCNTL', None),
                 ('HAS_MSGHDR_FLAGS', None), ('HAS_SOCKLEN_T', None)]

libraries = []

if sys.platform == 'win32':
    define_macros.extend([('WIN32', None)])
    libraries.extend(['Winmm', 'ws2_32'])

if sys.platform != 'darwin':
    define_macros.extend([('HAS_GETHOSTBYNAME_R', None),
                          ('HAS_GETHOSTBYADDR_R', None)])

ext_modules = [
    Extension(
        "enet",
        sources=source_files,
        include_dirs=["enet/include/"],
        define_macros=define_macros,
        libraries=libraries,
        library_dirs=["enet/"])
]

setup(
    name='pyenet',
    # packages=['enet'],
    description='A python wrapper for the ENet library',
    long_description=long_description,
    url='https://github.com/piqueserver/pyenet/',
    maintainer='Andrew Resch, Piqueserver team',
    maintainer_email='samuel@swalladge.id.au',

    version=package_version,
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    setup_requires=['Cython>=3,<4'],
    install_requires=['Cython>=3,<4'],
)
