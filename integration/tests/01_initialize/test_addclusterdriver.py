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

DRIVERS_URL = "/n/drivers/cluster"


def test_addclusterdriver(rancher_conf, login_page, cluster_list):
    # login as admin
    login_page.login(DRIVERS_URL, "admin", rancher_conf.rancher_password)
    # click "Add Cluster Driver"
    cluster_list.click_add_cluster_driver()
    # fill new cluster driver fields and click "Create""
    cluster_list.register_driver(
        rancher_conf.kontainer_driver_location,
        rancher_conf.kontainer_driver_ui_location,
        "*.otc.t-systems.com"
    )
    # wait until otccce driver state is "Active"
    cluster_list.wait_for_activation()
