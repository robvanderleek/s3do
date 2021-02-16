import logging

import boto3
import click
from botocore.exceptions import ClientError, NoCredentialsError

from s3do.utils import do_for_all_objects


@click.command()
@click.argument('bucket')
@click.argument('prefix', required=False)
def inventory(bucket, prefix):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s')
    try:
        client = boto3.client('s3')

        def print_object(o):
            print(f'{bucket},{o["Key"]}')

        do_for_all_objects(client, bucket, prefix, print_object)
    except (ClientError, NoCredentialsError) as e:
        logging.error(e)
