#!/bin/bash

shopt -s extglob

export CLIENT_PACKAGE_BUILD=true

mkdir -p output
rm output/*

echo "Activating venv..."
source .venv/bin/activate

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

if ! [[ -v CI ]]; then
	echo "Cleaning up..."
	rm -r wrapper/game
	rm -r wrapper/visualizer
	rm -r wrapper/server
fi

echo "Build successful."
