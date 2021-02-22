import logging

import boto3
import click
from botocore.exceptions import ClientError, NoCredentialsError

from s3do.utils import do_for_all_objects


def get_callback(bucket):
    def print_object(o):
        print(f'{bucket},{o["Key"]}')

    return print_object


@click.command()
@click.argument('bucket')
@click.argument('prefix', required=False)
def inventory(bucket, prefix):
    try:
        client = boto3.client('s3')
        do_for_all_objects(client, bucket, prefix, get_callback(bucket))
    except (ClientError, NoCredentialsError) as e:
        logging.error(e)
