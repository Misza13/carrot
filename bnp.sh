#!/bin/bash

rm -rf build carrot_mc.egg-info dist
python setup.py sdist bdist_wheel
twine upload dist/*