#!/usr/bin/env python3

import sys
import re
import docker

import htrouter
import htregistry
import htapp
import config


class DockerHt:
    def __init__(self, config):
        """
        Initializes config and prepares build and run cli. If no docker url
        given for each cli connection, try fetching cli url from environment.
        """
        self.config = config
        try:
            self.docker_run_url = config.docker_run_url
            tls_config = docker.tls.TLSConfig(
                verify=config.docker_run_ca_cert,
                assert_hostname=False)
            self.docker_run_cli = docker.client.Client(
                base_url=self.docker_run_url, tls=tls_config)
        except AttributeError:
            kwargs = docker.utils.kwargs_from_env(assert_hostname=False)
            cf = kwargs['tls']
            self.docker_run_url = kwargs['base_url']
            self.docker_run_cli = docker.client.Client(**kwargs)
        try:
            self.docker_build_url = config.docker_build_url
            tls_config = docker.tls.TLSConfig(
                verify=config.docker_build_ca_cert,
                assert_hostname=False)
            self.docker_build_cli = docker.client.Client(
                base_url=self.docker_build_url, tls=tls_config)
        except AttributeError:
            kwargs = docker.utils.kwargs_from_env(assert_hostname=False)
            self.docker_build_url = kwargs['base_url']
            self.docker_build_cli = docker.client.Client(**kwargs)

    def setup(self):
        """
        Inspects the htrouter container and starts the htrouter setup by
        passing in the container's status. If inspection fails with a NotFound
        Docker error, None is passed in for the htrouter setup.
        """
        try:
            htrouter_inspect = self.docker_run_cli.inspect_container(
                self.config.ht_router_name)
            htrouter_status = htrouter_inspect['State']['Status']
        except docker.errors.NotFound:
            htrouter_status = None
        htrouter_inspect = htrouter.setup(self.docker_run_cli, htrouter_status)
        return htrouter_inspect

    def push_build(self, path, vhost):
        self.clean_old_containers()
        if vhost in self.container_names:
            self.docker_run_cli.rename(vhost, vhost + '_old')
        # Delete old host if exists
        htapp.build(self.docker_build_cli, path, vhost)
        htapp.deploy(self.docker_build_cli, self.docker_run_cli, vhost)

        for port, vhost in self.container_names_and_ports:
            target = 'http://127.0.0.1:' + port
            htrouter.update_router(vhost, target, self.redis_run_host)

    def clean_old_containers(self):
        for container in self.container_names:
            if container.endswith('_old'):
                self.docker_run_cli.stop(container)
                self.docker_run_cli.remove_container(container)

    @property
    def redis_run_host(self):
        """
        A property to extract the host part out of the docker_run_url. To be
        used for the Redis connection.
        """
        host = re.split('(://|:)', self.docker_run_url)[2]
        return host

    @property
    def container_names(self):
        """
        A property to return all containers of the run instance.
        """
        names = []
        containers = self.docker_run_cli.containers(all=True)
        for container in containers:
            name = container['Names'][0][1:]
            names.append(name)
        return names

    @property
    def container_names_and_ports(self):
        container_names_and_ports = []
        containers = self.docker_run_cli.containers(all=True)
        for container in containers:
            try:
                port = container['Ports'][0]['PublicPort']
                vhost = container['Names'][0][1:]
                container_names_and_ports.append((str(port), vhost))
            except (KeyError, IndexError):
                pass
        return container_names_and_ports

if __name__ == "__main__":
    dockerht = DockerHt(config)
    dockerht.clean_old_containers()
    print(dockerht.container_names_and_ports)
    #if dockerht.setup():
    #    print("Htrouter is running.")
    #else:
    #    print("Htrouter setup failed")
    dockerht.push_build("myapp", "www.vhostsa.com")
    #htrouter.update_router('www.foo.com', 'http://173.194.112.239:80', dockerht.redis_run_host)
