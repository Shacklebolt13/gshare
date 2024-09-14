#!/bin/bash
# This script will remove all files from ./media folder, where filename != .gitingore
find ./media/logs -type f ! -name '.gitignore' -exec rm -f {} \;
find ./media/raw -type f ! -name '.gitignore' -exec rm -f {} \;
