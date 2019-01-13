#!/bin/bash

cd carrot_mc/web_gui
npm install
npx webpack
cd ../..

rm -rf build carrot_mc.egg-info dist
python setup.py sdist bdist_wheel
twine upload dist/*