#!/bin/bash

if [ -z $WORKSPACE ]
then
    cd `dirname $0`/..
    WORKSPACE=`pwd`
fi

"$WORKSPACE"/ci/setup_python_venv.sh
virtualenv "$WORKSPACE"/ci/python_virtual_env

flake8 src/python

flake8rc=$?

nosetests --with-xunit \
         --with-coverage \
         --cover-package=src/python\
         --cover-xml \
         --cover-html \
         tests/python
rc=$?

deactivate

if [ $flake8rc -ne 0 ]
then
    echo "Formatting did not meet guidelines"
    exit $flake8rc
fi

exit $rc
