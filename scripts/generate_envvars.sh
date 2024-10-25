#!/bin/bash

MD="ENVVARS.md"
MDTPL="ENVVARS.template.md"
JSONL="ENVVARS.jsonl"

echo "" > "${MD}"
echo "" > "${JSONL}"

poetry run python -m scripts dump-settings --json > "${JSONL}"
# apt install -y gettext-base
TABLE=$(poetry run python -m scripts dump-settings) envsubst < "${MDTPL}" > "${MD}"
