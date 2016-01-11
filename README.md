# DockerHt

NOTE: This software is still under development and in "Experimental State".

DockerHt (Docker HTTP tenants) is an easy solution to build and deploy web applications each at a time with a high number
of running Vhosts on a single host based on Docker and Hipache. This is perfect for small web applications, prototyping and
testing.

It makes use of the Docker API with docker-py and includes a setup procedure to run Hipache, a full featured distributed proxy
written in NodeJs, perfect to run a high number of VHosts. DockerHt supports different targets for building and running images
and works without the need of running a Docker registry.

As a requirement to run DockerHt you need to have at least one host running Docker, as well as a wildcard DNS entry pointing
to it. In order to test DockerHt simply install Docker including DockerMachine on your Mac computer, create two machines
called "build" and "web", configure the ip addresses corresponding to your VMs in config.py and place your application 
including your Dockerfile inside the myapp folder. Then run dockerht.py -h to get help about arguments.
