#!/bin/bash

TERMUX_INSTALL="$1"

if [ -z "$TERMUX_INSTALL" ]; then
    ON_DEVICE=1
    INSTALL="$PWD/out"
else
   INSTALL="$TERMUX_INSTALL"
fi 


cmake -H. -Bbuild/mm/ -DCMAKE_INSTALL_PREFIX=$INSTALL -DCMAKE_PREFIX_PATH=$INSTALL

cmake --build build/mm