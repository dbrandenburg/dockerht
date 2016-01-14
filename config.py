#!/usr/bin/env python3

# Copyright 2016 Dennis Brandenburg <d.brandenburg@db-network.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

home_dir = os.getenv("HOME")
tmp_suffix = '_tmp'
docker_web_container = {
    #'url': 'https://192.168.99.100:2376',
    'ca_cert': home_dir + '/.docker/machine/machines/web/ca.pem',
    'client_cert': home_dir + '/.docker/machine/machines/web/cert.pem',
    'client_key': home_dir + '/.docker/machine/machines/web/key.pem'
}
docker_build_container = {
    #'url': 'https://192.168.99.101:2376',
    'ca_cert': home_dir + '/.docker/machine/machines/build/ca.pem',
    'client_cert': home_dir + '/.docker/machine/machines/build/cert.pem',
    'client_key': home_dir + '/.docker/machine/machines/build/key.pem'
}
