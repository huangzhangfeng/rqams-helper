#!/usr/bin/env bash

set -e

UI_DIR=ui
UI_MODULE_DIR=rqams_helper/windows/ui

for file in "${UI_DIR}"/*.ui
do
  module_name=$(echo "${file}" | sed "s/^${UI_DIR}\///g" | sed "s/.ui$//g")
  pyside2-uic "${file}" -o "${UI_MODULE_DIR}/${module_name}.py" -x
done
