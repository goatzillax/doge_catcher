# doge_catcher

Super dirty motion detection script.

Requires python, PIL/pillow, and mv-extractor (https://github.com/LukasBommes/mv-extractor)

Search uses a bitmap ("mask.bmp") to define search area.  White pixels are ignore, black pixels are valid.

The makefile is just to parallelize launch and allow for file-level restart, i.e.

    CORES=4
    make -f Makefile.dog_catcher -j ${CORES}

Should build the target list (Makefile.targets) with the SRC variable.
