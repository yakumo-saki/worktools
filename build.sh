#!/bin/bash -eu

BASE_DIR=$(cd $(dirname $0);pwd)

cd $BASE_DIR
rm -rf ./build
rm -rf ./dist

python3 setup.py py2app

cd $BASE_DIR/dist
zip -r "WorkTools.zip" "Work Tools.app"

echo "BUILD DONE. dist/WorkTools.zip"
