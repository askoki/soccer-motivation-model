#!/usr/bin/env bash

sh -c 'cd ../src/models/pso && python optimize.py'
sh -c 'cd ../src/models/nelder-mead && python optimize.py'