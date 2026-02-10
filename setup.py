from setuptools import setup, Extension
from Cython.Build import cythonize

import glob
import sys

source_files = ["enet.pyx"]

_enet_files = glob.glob("enet/*.c")
source_files.extend(_enet_files)


define_macros = [('HAS_POLL', None), ('HAS_FCNTL', None),
                 ('HAS_MSGHDR_FLAGS', None), ('HAS_SOCKLEN_T', None)]

libraries = []

if sys.platform == 'win32':
    define_macros.extend([('WIN32', None)])
    libraries.extend(['Winmm', 'ws2_32'])

if sys.platform != 'darwin':
    define_macros.extend([('HAS_GETHOSTBYNAME_R', None),
                          ('HAS_GETHOSTBYADDR_R', None)])

ext_modules = cythonize(
    [Extension(
        "enet",
        sources=source_files,
        include_dirs=["enet/include/"],
        define_macros=define_macros,
        libraries=libraries,
        library_dirs=["enet/"])],
    compiler_directives={'language_level': 2},
)

setup(
    ext_modules=ext_modules,
)
