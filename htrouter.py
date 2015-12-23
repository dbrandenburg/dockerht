#!/usr/bin/env python3


def setup(cli, htrouter_status):
    """
    Create and start a new htrouter if htrouter_status is None, otherwise try
    starting an existing one.
    """
    if not htrouter_status:
        hipache_container = cli.create_container(
            "hipache", name="htrouter", ports=["80", "443", "6379"])
    cli.start('htrouter')
    htrouter_inspect = cli.inspect_container('htrouter')
    htrouter_status = htrouter_inspect['State']['Status']
    if htrouter_status == 'running':
        return htrouter_inspect
    else:
        return False


def update_router(cli):
    pass


def status(cli):
    print()
    return True
