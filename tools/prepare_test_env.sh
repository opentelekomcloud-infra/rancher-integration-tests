#!/usr/bin/env bash

ansible-playbook playbooks/prepare_test_env.yaml -e ansible_python_interpreter=`which python`

export RANCHER_BIND_HOST=$(ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p')