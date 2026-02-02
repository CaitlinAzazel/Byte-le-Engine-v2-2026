#!/bin/bash

shopt -s extglob

test -e launcher.pyz && rm launcher.pyz
cp -r game wrapper/game/
cp -r visualizer wrapper/visualizer/
mkdir -p wrapper/server
cp -r server/!(*_temp|logs) wrapper/server/
python -m zipapp wrapper -o launcher.pyz -c
rm -r wrapper/game
rm -r wrapper/visualizer
rm -r wrapper/server
