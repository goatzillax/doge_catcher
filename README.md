# doge_catcher

Super dirty motion detection script.

Requires python and mv-extractor (https://github.com/LukasBommes/mv-extractor)

The makefile is just to parallelize launch and allow for file-level restart, i.e.

    CORES=4
    make -f Makefile.dog_catcher -j ${CORES}

Should build the target list (Makefile.targets) with the SRC variable.
