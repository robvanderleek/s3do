#!/usr/bin/env python
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


cli_entry_point.add_command(tag.tag)
cli_entry_point.add_command(inventory.inventory)

if __name__ == '__main__':
    cli_entry_point()
