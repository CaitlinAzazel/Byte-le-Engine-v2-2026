#!/bin/bash

shopt -s extglob

export CLIENT_PACKAGE_BUILD=true

# GitHub Actions always have CI set as an environment variable
# this checks if CI is unset; we are running this locally
if ! [[ -v CI ]]; then
	if [[ -f output ]]; then
		echo "Cleaning old build..."
		rm -r output/*
	fi

	echo "Activating venv..."
	source .venv/bin/activate
fi

mkdir -p output

echo "Compiling map data..."
python compile_map_data.py

echo "Copying extra files..."
cp -r client_package/* output/
cp client_package/.gitignore output/ # wildcards dont match dotfiles by default
cp -r docs/ output/

IMAGES=output/visualizer/images
mkdir -p $IMAGES/staticsprites $IMAGES/spritesheets output/visualizer/fonts
echo "Copying assets..."
cp -r visualizer/images/staticsprites/!(*.txt) $IMAGES/staticsprites
cp -r visualizer/images/spritesheets/!(*.txt) $IMAGES/spritesheets
cp -r visualizer/fonts/!(*.txt) output/visualizer/fonts

echo "Building launcher..."
cp -r game wrapper/game/
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
