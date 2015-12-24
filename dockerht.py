import docker
import htrouter
import htregistry
import htapp
import sys
import config


class DockerHt:
    def __init__(self, config):
        """
        Initializes config and prepares build and run cli. If no docker url
        given for each cli connection, try fetching cli url from environment.
        """
        try:
            self.docker_run_url = config.docker_run_url
            self.docker_run_cli = docker.client.Client(self.docker_run_url)
        except AttributeError:
            kwargs = docker.utils.kwargs_from_env(assert_hostname=False)
            self.docker_run_url = kwargs['base_url']
            self.docker_run_cli = docker.client.Client(**kwargs)
        try:
            self.docker_build_url = config.docker_build_url
            self.docker_build_cli = docker.client.Client(self.docker_build_url)
        except AttributeError:
            kwargs = docker.utils.kwargs_from_env(assert_hostname=False)
            self.docker_build_url = kwargs['base_url']
            self.docker_build_cli = docker.client.Client(**kwargs)

    def setup(self, htrouter_name):
        """
        Inspects the htrouter container status and starts the htrouter setup by
        passing in the insepcted status. If inspection fails with a NotFound
        Docker error, None is passed in for the htrouter setup.
        """
        try:
            htrouter_inspect = self.docker_run_cli.inspect_container(
                htrouter_name)
            htrouter_status = htrouter_inspect['State']['Status']
        except docker.errors.NotFound:
            htrouter_status = None
        htrouter_inspect = htrouter.setup(self.docker_run_cli, htrouter_status)
        return htrouter_inspect

    def push_puild(self):
        httpapp.build()
        httpapp.deploy()

htportroute = DockerHt(config)
if htportroute.setup('htrouter'):
    print("Htrouter running.")
else:
    print("Htrouter Setup failed")
