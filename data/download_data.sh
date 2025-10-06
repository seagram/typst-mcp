#!/bin/bash
LATEST_TAG=$(curl -s https://api.github.com/repos/typst-community/dev-builds/releases/latest | grep '"tag_name"' | sed 's/.*"tag_name": "\(.*\)".*/\1/')
curl -L -o docs.json https://github.com/typst-community/dev-builds/releases/download/${LATEST_TAG}/docs.json
