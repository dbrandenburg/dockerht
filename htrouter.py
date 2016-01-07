#!/usr/bin/env python3
import redis
import re


def setup(docker_run_cli, htrouter_status):
    """
    Create and start a new htrouter if htrouter_status is None, otherwise try
    starting an existing one or fail.
    """
    if not htrouter_status:
        docker_run_cli.pull('hipache:0.2.8')
        hipache_container = docker_run_cli.create_container(
            'hipache:0.2.8', name='htrouter', ports=['80', '443', '6379'],
            host_config=docker_run_cli.create_host_config(
                port_bindings={80: 80, 443: 443, 6379: 6379}))
    docker_run_cli.start('htrouter')
    htrouter_inspect = docker_run_cli.inspect_container('htrouter')
    htrouter_status = htrouter_inspect['State']['Status']
    if htrouter_status == 'running':
        return htrouter_inspect
    else:
        return False


def update_router(vhost, target, redis_host, redis_port=6379):
    redis_connection = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        db=0)
    redis_connection.rpush('frontend:' + vhost, target)
    dbs = redis_connection.keys()
    print(dbs)

if __name__ == "__main__":

    docker_run_url = 'tcp://192.168.99.100:2376'
    host = re.split('(://|:)', docker_run_url)[2]
    update_router('frontend:www.foo.com', 'http://173.194.112.239:80', host)
