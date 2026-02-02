all:
ifeq ($(OS),Windows_NT)
	.\build.bat
else
	./build.sh
endif
	python launcher.pyz gr
