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
import pytest

from integration.tests.helpers.timeouts import DRIVER_ACTIVATING


@pytest.mark.registration
def test_add_cluster_driver(cleanup_cluster_driver, signed_in,
                            cluster_driver_list, api_client,
                            rancher_conf):
    cluster_driver_list.open()

    # click "Add Cluster Driver"
    cluster_driver_list.click_add_cluster_driver()

    # fill new cluster driver fields and click "Create"
    cluster_driver_list.register_driver(
        rancher_conf.kontainer_driver_location,
        rancher_conf.kontainer_driver_ui_location,
        '*.otc.t-systems.com'
    )

    # wait until CCE driver state is "Active"
    cluster_driver_list.driver_row.state.assure('Activating', DRIVER_ACTIVATING)
    cluster_driver_list.driver_row.state.assure('Active')
