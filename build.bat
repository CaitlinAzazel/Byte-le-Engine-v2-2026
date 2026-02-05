@echo off
del /q *.pyz

xcopy /s/e/i "game" "wrapper/game"
xcopy /s/e/i "visualizer" "wrapper/visualizer"
xcopy /s/e/i "server" "wrapper/server"
python -m zipapp "wrapper" -o "launcher.pyz" -c
del /q/s "wrapper/game"
del /q/s "wrapper/visualizer"
del /q/s "wrapper/server"
