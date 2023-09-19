#!/bin/bash
set -e

source /opt/ros/humble/setup.bash
source /workspaces/barvaz_test/install/setup.bash

exec "$@"