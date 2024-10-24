#!/usr/bin/env sh

test_command="poetry run coverage run tests/main.py"
EXIT=0
${test_command} || EXIT=$? \
  && poetry run coverage xml -o reports/coverage/coverage_report.xml \
  && poetry run coverage html --directory=reports/coverage/html \
  && echo "Code coverage: $(poetry run coverage report --format=total)%"
exit $EXIT
