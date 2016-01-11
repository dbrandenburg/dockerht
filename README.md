# dockerht

NOTE: This software is still under development and in "Experimental State".

DockerHt (Docker HTTP tenant) is an easy solution to build and deploy a high number of web applications based on Docker to a
single host. This is perfect for small web applications, prototyping and testing.

It makes use of the Docker API with docker-py and includes a setup procedure to run Hipache, a full featured distributed proxy
written in NodeJs, perfect to run a high number of VHosts. DockerHt supports different targets for building and running images
and works without the need of running a Docker registry.

As a requirement to run DockerHt you need to have at least one VM running Docker, as well as a wildcard DNS entry pointing
to it. In order to test DockerHt simply install Docker including DockerMachine on your Mac computer, create two machines
called "build" and "web", and plave your Dockerfile and application inside the myapp folder. Then change your chost inside
dockerht.py.
