#!/bin/bash

# should be run in the docker container.
# builds the binary wheels

set -e -x

# code from https://github.com/pypa/python-manylinux-demo/blob/master/travis/build-wheels.sh
# Compile wheels
for PYBIN in /opt/python/{cp35-cp35m,cp36-cp36m,cp37-cp37m,cp38-cp38}/bin; do
    "${PYBIN}/pip" install -r /io/dev-requirements.txt
    cd /io/
    "${PYBIN}/python" setup.py bdist_wheel -d /wheelhouse/
    cd /
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
# for PYBIN in /opt/python/*/bin/; do
#     "${PYBIN}/pip" install python-manylinux-demo --no-index -f /io/wheelhouse
#     (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
# done
