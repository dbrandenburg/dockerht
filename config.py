import os

home_dir = os.getenv("HOME")
tmp_suffix = '_tmp'
docker_web_container = {
    #'url': 'https://192.168.99.100:2376',
    'ca_cert': home_dir + '/.docker/machine/machines/web/ca.pem',
    'client_cert': home_dir + '/.docker/machine/machines/web/cert.pem',
    'client_key': home_dir + '/.docker/machine/machines/web/key.pem'
}
docker_build_container = {
    #'url': 'https://192.168.99.101:2376',
    'ca_cert': home_dir + '/.docker/machine/machines/build/ca.pem',
    'client_cert': home_dir + '/.docker/machine/machines/build/cert.pem',
    'client_key': home_dir + '/.docker/machine/machines/build/key.pem'
}
