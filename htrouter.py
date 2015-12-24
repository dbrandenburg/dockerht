#!/usr/bin/env python3
import redis
import re


def setup(docker_run_cli, htrouter_status):
    """
    Create and start a new htrouter if htrouter_status is None, otherwise try
    starting an existing one.
    """
    if not htrouter_status:
        docker_run_cli.pull('hipache:0.2.8')
        hipache_container = docker_run_cli.create_container(
            'hipache:0.2.8', name='htrouter', ports=['80', '443', '6379'],
            host_config=cli.create_host_config(
                port_bindings={80: 80, 443: 443, 6379: 6379}))
    docker_run_cli.start('htrouter')
    htrouter_inspect = docker_run_cli.inspect_container('htrouter')
    htrouter_status = htrouter_inspect['State']['Status']
    if htrouter_status == 'running':
        return htrouter_inspect
    else:
        return False


def update_router(docker_run_url):
    proto, d, host, d, port = re.split('(://|:)', docker_run_url)
    redis_connection = redis.StrictRedis(
        host=host,
        port=6379,
        db=0)
    print(redis_connection.hkeys())


def status(cli):
    print()
    return True
update_router('tcp://192.168.99.100:2376')
