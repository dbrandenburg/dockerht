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

import redis
import docker


class Container:

    def __init__(self, docker_web_cli, redis_host, redis_port=6379):
        self.docker_web_cli = docker_web_cli
        redis_host = redis_host
        self.redis_connection = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            db=0)

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
                host_config=self.docker_web_cli.create_host_config(
                    network_mode='host'))
        self.docker_web_cli.start('hipache')
        hipache_inspect = self.docker_web_cli.inspect_container('hipache')
        hipache_status = hipache_inspect['State']['Status']
        if hipache_status == 'running':
            return hipache_inspect
        else:
            raise Exception('Hipache nor running correctly.')

    def delete_vhost(self, vhost):
        """
        Delete a particular vhost to not get served by hipache any further.
        """
        self.redis_connection.delete('frontend:' + vhost)

    def update_vhost(self, vhost, target):
        """
        Updates the reverse proxy configuration vhost to backend:port in redis.
        """
        self.redis_connection.delete('frontend:' + vhost)
        self.redis_connection.rpush('frontend:' + vhost, vhost)
        self.redis_connection.rpush('frontend:' + vhost, target)
        keys = self.redis_connection.keys('*')
        print(self.redis_connection.lrange('frontend:' + vhost, 0, 2))

    def update_all_vhosts(self, container_names_and_ports, ignore_suffix):
        """
        Updates all vhost configurations to point to the right port the docker
        container listens on. Ignores container names ending with
        ignore_suffix.
        """
        for port, vhost in container_names_and_ports:
            if not vhost.endswith(ignore_suffix):
                target = 'http://127.0.0.1:' + port
                self.update_vhost(vhost, target)
