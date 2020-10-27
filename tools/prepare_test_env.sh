#!/usr/bin/env bash

# TODO: maybe install collection to temp place
#ansible-galaxy collection install community.general 
ansible-playbook playbooks/prepare_test_env.yaml -e ansible_python_interpreter=`which python`

