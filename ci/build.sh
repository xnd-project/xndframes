#!/usr/bin/env bash
set -e
echo "Building xndframes"

conda build -c defaults -c conda-forge conda-recipes/xndframes --python=${PYTHON}