#!/bin/bash

shopt -s extglob

mkdir output

echo "Compiling map data..."
python compile_map_data.py

echo "Building launcher..."
cp -r game wrapper/game/
cp -r visualizer wrapper/visualizer/
mkdir -p wrapper/server
cp -r server/!(*_temp|logs) wrapper/server/
python -m zipapp wrapper -o output/launcher.pyz -c

echo "Copying extra files..."
cp -r client_package/* output/

echo "Build successful."
