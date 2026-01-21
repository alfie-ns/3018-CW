#!/bin/bash
read -p "3018-CW: Enter commit message: " msg
git add .
git commit -m "$msg"
git push origin main
