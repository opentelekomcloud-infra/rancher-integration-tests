#!/usr/bin/env bash

rancher_image=rancher/rancher:${RANCHER_VERSION:-v2.4.8}
selenium_image=selenium/standalone-chrome:${SELENIUM_VERSION:-3.141}

docker run -d -p 443:443 -p 8080:8080 --privileged --name rancher ${rancher_image}
docker run -d -p 4444:4444 --name selenium-chrome ${selenium_image}

# Auth on rancher
token=$(curl -k -X POST \
    https://localhost:443/v3-public/localProviders/local?action=login \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin"}' \
   2>/dev/null | jq ".token")

echo $token

# Set rancher url

