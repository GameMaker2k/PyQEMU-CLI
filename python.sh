#!/bin/bash

pyver="$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1)"

if [ "${pyver}" -eq 2 ]; then
 python "$@"
fi

if [ "${pyver}" -eq 3 ]; then
 python2 "$@"
fi
