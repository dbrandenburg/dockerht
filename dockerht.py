import docker
import htrouter
import htregistry
import htapp


class HtPortRoute:
    def __init__(self):
        kwargs = docker.utils.kwargs_from_env(assert_hostname=False)
        self.client = docker.client.Client(**kwargs)
        self.config = {'port': 80, 'domain': 'localhsot'}

    def setup(self):
        if not htrouter.status(self.client, self.config):
            htrouter.setup(self.client, self.config)

        if not htregistry.status():
            htregistry.setup()

    def push_puild(self):
        httpapp.build()
        httpapp.deploy()

htportroute = HtPortRoute()
htportroute.setup()
