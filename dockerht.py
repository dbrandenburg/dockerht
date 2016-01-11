#!/usr/bin/env python3

import sys
import argparse
import re
import docker

import hipache
import dockerapp
import config


class DockerHt:
    def __init__(self, config):
        """
        Initializes the config and cli.
        """
        self.config = config
        self.docker_web_url, self.docker_web_cli = self.__init_docker_cli(
            config.docker_web_container)
        self.docker_build_url, self.docker_build_cli = self.__init_docker_cli(
            config.docker_build_container)
        self.hipache_container = hipache.Container(
            self.docker_web_cli, self.redis_host)

    def __init_docker_cli(self, container_config):
        """
        Prepares the build and web cli. If no docker url given for each cli
        connection, try fetching cli url from the environment.
        """
        try:
            docker_web_url = container_config['url']
            tls_config = docker.tls.TLSConfig(
                verify=True,
                ca_cert=container_config['ca_cert'],
                client_cert=(container_config['client_cert'],
                             container_config['client_key']),
                assert_hostname=False)
            docker_web_cli = docker.client.Client(
                base_url=container_config['url'], tls=tls_config)
        except KeyError:
            kwargs = docker.utils.kwargs_from_env(assert_hostname=False)
            cf = kwargs['tls']
            docker_web_url = kwargs['base_url']
            docker_web_cli = docker.client.Client(**kwargs)
        return docker_web_url, docker_web_cli

    def setup(self):
        """
        Initializes the hipache setup routine which is triggering a hipache
        Docker setup in case the machine is not existent.
        """

        hipache_inspect = self.hipache_container.setup()
        if hipache_inspect:
            print("hipache is running.")
        else:
            print("hipache setup failed")
            exit(1)
        return hipache_inspect

    def push_app(self, path, vhost, command):
        """
        Builds, pushes and makes a Docker container available via vhost.
        """
        self.remove_tmp_apps()
        dockerapp.build(self.docker_build_cli, path, vhost)
        if vhost in self.container_names:
            tmp_container_name = vhost + self.config.tmp_suffix
            self.docker_web_cli.rename(vhost, tmp_container_name)
            dockerapp.deploy(self.docker_build_cli, self.docker_web_cli, vhost,
                             command)
            self.hipache_container.update_all_vhosts(
                self.container_names_and_ports, self.config.tmp_suffix)
            self.docker_web_cli.stop(tmp_container_name)
            self.docker_web_cli.remove_container(tmp_container_name)

        else:
            dockerapp.deploy(self.docker_build_cli, self.docker_web_cli,
                             vhost, command)
            self.hipache_container.update_all_vhosts(
                self.container_names_and_ports, self.config.tmp_suffix)

    def remove_app(self, vhost):
        """
        Remove a particular Docker app container based on the vhost name.
        """
        self.docker_web_cli.stop(vhost)
        self.docker_web_cli.remove_container(vhost)
        self.hipache.delete_vhost(vhost)

    def remove_tmp_apps(self):
        """
        Stops and removes all temporary containers which names are ending with
        the tmp_suffix and might not have been removed due to unexpected script
        exits.
        """
        for vhost in self.container_names:
            if vhost.endswith(self.config.tmp_suffix):
                self.docker_web_cli.stop(vhost)
                self.docker_web_cli.remove_container(vhost)

    @property
    def redis_host(self):
        """
        A property to extract the host part out of the docker_web_url. To be
        used for the Redis connection.
        """
        host = re.split('(://|:)', self.docker_web_url)[2]
        return host

    @property
    def container_names(self):
        """
        A property which returns all containers of the web instance.
        """
        names = []
        containers = self.docker_web_cli.containers(all=True)
        for container in containers:
            name = container['Names'][0][1:]
            names.append(name)
        return names

    @property
    def container_names_and_ports(self):
        """
        A property which returns all container names ans ports as a list of
        tuples.
        """
        container_names_and_ports = []
        containers = self.docker_web_cli.containers(all=True)
        for container in containers:
            try:
                port = container['Ports'][0]['PublicPort']
                vhost = container['Names'][0][1:]
                container_names_and_ports.append((str(port), vhost))
            except (KeyError, IndexError):
                pass
        return container_names_and_ports

    def argument_parsing(self):
        parser = argparse.ArgumentParser(
            description="DockerHt is used to build and deploy Docker web " +
                        "applications as vhosts.")
        parser.add_argument('-a', '--app-dir', nargs=1, required=True,
                            help="Docker app directory.")
        parser.add_argument('-v', '--vhost', nargs=1, required=True,
                            help="Vhost to deploy.")
        parser.add_argument('-c', '--command', nargs=1, required=True,
                            help="Command to run.")
        args = vars(parser.parse_args())
        return args


if __name__ == "__main__":
    dockerht = DockerHt(config)
    args = dockerht.argument_parsing()
    app_dir = args['app_dir'][0]
    vhost = args['vhost'][0]
    command = args['command'][0]
    dockerht.setup()
    #command = "/usr/sbin/httpd -DFOREGROUND"
    dockerht.push_app(app_dir, vhost, command)
