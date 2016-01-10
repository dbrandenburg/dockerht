#!/usr/bin/env python3


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
