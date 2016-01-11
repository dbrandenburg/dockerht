#!/usr/bin/env python3
import redis
import docker


class Container:

    def __init__(self, docker_web_cli, redis_host):
        self.docker_web_cli = docker_web_cli
        self.redis_host = redis_host

    def status(self):
        """
        Tries fetching the status of the hipache container and return it.
        Returns None in case the container doesn't exist.
        """
        try:
            hipache_inspect = self.docker_web_cli.inspect_container('hipache')
            hipache_status = hipache_inspect['State']['Status']
        except docker.errors.NotFound:
            hipache_status = None
        return hipache_status

    def setup(self):
        """
        Create and start a new hipache if hipache_status is None, otherwise try
        starting an existing one or fail.
        """
        if not self.status():
            self.docker_web_cli.pull('hipache:0.2.8')
            hipache_container = self.docker_web_cli.create_container(
                'hipache:0.2.8', name='hipache', ports=['80', '443', '6379'],
                host_config=docker_web_cli.create_host_config(
                    network_mode='host'))
        self.docker_web_cli.start('hipache')
        hipache_inspect = self.docker_web_cli.inspect_container('hipache')
        hipache_status = hipache_inspect['State']['Status']
        if hipache_status == 'running':
            return hipache_inspect
        else:
            raise Exception('Hipache nor running correctly.')

    def update(self, vhost, target, redis_port=6379):
        """
        Updates the reverse proxy configuration vhost to backend:port in redis.
        """
        redis_connection = redis.StrictRedis(
            host=self.redis_host,
            port=redis_port,
            db=0)
        redis_connection.delete('frontend:' + vhost)
        redis_connection.rpush('frontend:' + vhost, vhost)
        redis_connection.rpush('frontend:' + vhost, target)
        keys = redis_connection.keys('*')
        print(redis_connection.lrange('frontend:' + vhost, 0, 2))

    def update_all(self, container_names_and_ports, ignore_suffix):
        """
        Updates all vhost configurations to point to the right port the docker
        container runs on. Ignores container names ending with ignore_suffix.
        """
        for port, vhost in container_names_and_ports:
            if not vhost.endswith(ignore_suffix):
                target = 'http://127.0.0.1:' + port
                self.update(vhost, target)