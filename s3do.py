#!/usr/bin/env python
import logging
import sys

import click

from s3do import inventory, tag


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)


@click.group()
def cli_entry_point():
    pass


cli_entry_point.add_command(inventory.inventory)
cli_entry_point.add_command(tag.tag)

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s')
    cli_entry_point()
