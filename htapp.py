#!/usr/bin/env python3
import tarfile


def build(docker_build_cli, path, vhost):
    for response in docker_build_cli.build(path=path, tag=vhost, decode=True):
        if 'error' in response:
            raise Exception("Error building docker image: {}".format(response['error']))


def deploy(docker_build_cli, docker_run_cli, vhost):
    command = "/bin/sh -c \"while true; do echo hello |nc -l 80;done\""
    image = docker_build_cli.get_image(vhost)
    docker_run_cli.load_image(image.data)
    container = docker_run_cli.create_container(image=vhost, command=command,
                                                ports=[80], name=vhost)
    response = docker_run_cli.start(container=container.get('Id'))



def remove():
    pass

if __name__ == "__main__":
    pass
