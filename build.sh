#!/bin/bash

rm *.pyz
cp -r "game" "wrapper/game"
cp -r "visualizer" "wrapper/visualizer"
cp -r "server" "wrapper/server"
python -m zipapp "wrapper" -o "launcher.pyz" -c
rm -r "wrapper/game"
rm -r "wrapper/visualizer"
rm -r "wrapper/server"
