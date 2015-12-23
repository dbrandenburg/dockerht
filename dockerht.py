import docker
import htrouter
import htregistry
import htapp
import sys


class HtPortRoute:
    def __init__(self):
        kwargs = docker.utils.kwargs_from_env(assert_hostname=False)
        self.cli = docker.client.Client(**kwargs)
        self.config = {'port': 80, 'domain': 'localhost'}

    def setup(self):
        """
        Inspects the htrouter container status and starts the htrouter setup by
        passing in the insepcted status. If inspection fails with a NotFound
        Docker error, None is passed in for the htrouter setup.
        """

        try:
            htrouter_inspect = self.cli.inspect_container('htrouter')
            htrouter_status = htrouter_inspect['State']['Status']
        except docker.errors.NotFound:
            htrouter_status = None
        htrouter_inspect = htrouter.setup(self.cli, htrouter_status)
        return htrouter_inspect

    def push_puild(self):
        httpapp.build()
        httpapp.deploy()

htportroute = HtPortRoute()
if htportroute.setup():
    print("Htrouter running.")
else:
    print("Htrouter Setup failed")
