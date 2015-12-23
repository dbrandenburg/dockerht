#!/usr/bin/env python3


def setup(cli):
    pass


def status(cli):
    container_list = cli.containers()
    for container in container_list:
        if '/registry' in container['Names']:
            return True
    return None
