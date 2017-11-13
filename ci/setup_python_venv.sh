#!/bin/bash

virtualenv $HOME/python_automation_virtual_env
source $HOME/python_automation_virtual_env/bin/activate

pip install --upgrade setuptools==33.1.1
pip install autoflake==0.6.6
pip install autopep8==1.2.2
pip install click==6.7
pip install coverage==4.1
pip install flake8==2.5.4
pip install mock==1.3.0
pip install nose==1.3.7
pip install pexpect==4.2.1
pip install requests==2.9.1

echo "Now copy and paste this into your terminal:"
echo source $HOME/python_automation_virtual_env/bin/activate
