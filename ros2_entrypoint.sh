#!/bin/bash
set -e

source /opt/ros/humble/setup.bash
source /workspaces/gal_orbits/install/setup.bash

exec "$@"