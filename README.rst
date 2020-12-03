Rancher Integration tests
=========================

Usage
-----

- execute `tools/prepare_rancher_env.sh` for starting docker containers
  (rancher and selenium) and setting rancher password
- execute `tox -e register` to only test driver registration
- execute `tox -e integration` to execute all tests


Notes
-----

- env.RANCHER_BIND_HOST - ip address to access rancher and selenium
- Rancher port by default is 8003
- Selenium port by default is 8004
- integration tests require:
  - env.OS_DOMAIN_NAME
  - env.OS_PROJECT_NAME
  - env.OS_USER_NAME
  - env.OS_PASSWORD
  - provisioned router rancher-otc-vpc-router
  - existing subnet under the router: rancher-default-subnet
  - existing keypair rancher-KeyPair
