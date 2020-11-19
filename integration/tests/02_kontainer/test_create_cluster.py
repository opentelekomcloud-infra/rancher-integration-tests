# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import time

from pyasli.conditions import missing

from integration.tests.helpers.timeouts import (
    CLUSTER_ACTIVE, CLUSTER_DELETED,
    CLUSTER_DELETING, CLUSTER_PROVISIONING
)


def test_cce_cluster_lifecycle(rancher_conf, signed_in, cluster_list,
                               assure_cluster_driver, new_cluster_select,
                               cluster_config, cleanup_cluster):
    cluster_list.open()

    # open creation page
    cluster_list.click_new_cluster()

    # select OTC CCE
    new_cluster_select.click_new_cce_cluster()

    # setup new cluster

    cluster_config.set_name(rancher_conf.cluster_name)

    # login in OTC
    cluster_config.input_credentials(
        rancher_conf.cce_domain_name,
        rancher_conf.cce_user_name,
        rancher_conf.cce_password,
        rancher_conf.cce_project_name,
    )

    # next: Cluster Configuration
    cluster_config.next()
    time.sleep(3)  # don't rush or lists won't be able to load in time
    # use default cluster configuration

    # next: network configuration
    cluster_config.next()
    # select required VPC
    cluster_config.select_vpc(rancher_conf.vpc_name)
    # select required Subnet
    cluster_config.select_subnet(rancher_conf.subnet_name)

    # next: Cluster Floating IP
    cluster_config.next()

    # next: Node Configuration
    cluster_config.next()
    cluster_config.select_key_pair(rancher_conf.keypair_name)

    # next: Nodes disk configuration
    cluster_config.next()
    # use default configuration
    # finish creation
    cluster_config.next()

    # =====
    # find cluster row in list
    my_cluster = cluster_list.cluster_row(rancher_conf.cluster_name)
    my_cluster.state.assure('Provisioning', CLUSTER_PROVISIONING)
    my_cluster.state.assure('Active', CLUSTER_ACTIVE)
    # remove cluster
    cluster_list.delete(rancher_conf.cluster_name)

    # wait for cluster to start deleting
    my_cluster.state.assure('Removing', CLUSTER_DELETING)

    # wait for cluster to end deleting
    my_cluster.should_be(missing, CLUSTER_DELETED)
