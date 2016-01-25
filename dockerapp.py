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

def build(docker_build_cli, path, vhost):
    """
    Builds a Docker image based on a path to a Dockerfile containing folder,
    and gives a vhost as a name to allow tracking builds and start
    containers based on the vhost name.
    """
    for response in docker_build_cli.build(path=path, tag=vhost,
                                           rm=True, decode=True):
        if 'error' in response:
            raise Exception("Error building docker image: " +
                            response['error'])


def deploy(docker_build_cli, docker_web_cli, vhost, command=None):
    """
    Saves an image from the Docker build machine and loads it on the Docker web
    machine.
    """
    image = docker_build_cli.get_image(vhost)
    docker_web_cli.load_image(image.data)
    container = docker_web_cli.create_container(
            image=vhost, command=command, ports=[80],
            host_config=docker_web_cli.create_host_config(
                port_bindings={80: None}), name=vhost)
    docker_web_cli.start(container=container.get('Id'))
    return(container)
