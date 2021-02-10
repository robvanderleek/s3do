#!/usr/bin/env python
import click

import tag


@click.group()
def cli_entry_point():
    pass;


cli_entry_point.add_command(tag.tag)

if __name__ == '__main__':
    cli_entry_point()
