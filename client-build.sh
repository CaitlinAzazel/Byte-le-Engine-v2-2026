#!/bin/bash

shopt -s extglob
shopt -s dotglob

export CLIENT_PACKAGE_BUILD=true

# GitHub Actions always have CI set as an environment variable
# this checks if CI is unset; we are running this locally
if ! [[ -v CI ]]; then
	if [[ -f output ]]; then
		echo "Cleaning old build..."
		rm output/*
	fi

	echo "Activating venv..."
	source .venv/bin/activate
fi

mkdir -p output

echo "Compiling map data..."
python compile_map_data.py

echo "Copying extra files..."
cp -r client_package/!(.venv*) output/

echo "Building launcher..."
mkdir -p wrapper/game
cp -r game/!(map_data) wrapper/game/
cp -r visualizer wrapper/visualizer/
mkdir -p wrapper/server
cp -r server/!(*_temp|logs) wrapper/server/
python -m zipapp wrapper -o output/launcher.pyz -c


if ! [[ -v CI ]]; then
	echo "Cleaning up..."
	rm -r wrapper/game
	rm -r wrapper/visualizer
	rm -r wrapper/server
fi

echo "Build successful."
