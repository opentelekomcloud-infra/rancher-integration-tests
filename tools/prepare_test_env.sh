#!/usr/bin/env bash

# TODO: maybe install collection to temp place
ansible-galaxy collection install community.general 
ansible-playbook playbooks/prepare_test_env.yaml -e ansible_python_interpreter=`which python`

RANCHER_BIND_HOST=$(ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')

export RANCHER_BIND_HOST
