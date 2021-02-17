import logging

import boto3
import click
from botocore.exceptions import ClientError, NoCredentialsError

from s3do.utils import do_for_all_objects_all_versions


def get_handler(client, bucket):
    def tag_object(o):
        retries = 3
        while retries > 0:
            try:
                client.put_object_tagging(
                    Bucket=bucket,
                    Key=o['Key'],
                    VersionId=o['VersionId'],
                    Tagging={
                        'TagSet': [
                            {'Key': 'HealthData', 'Value': 'True'},
                            {'Key': 'DataType', 'Value': 'Raw'}
                        ]
                    }
                )
            except:
                if retries > 0:
                    retries -= 1
        logging.warning('Tagging failed for object: ' + bucket + '/' + o['Key'])

    return tag_object


@click.command()
@click.argument('bucket')
@click.argument('prefix', required=False)
@click.option('--tag', '-t', required=True, multiple=True)
def tag(bucket, prefix, tag):
    target = bucket
    if prefix:
        target += f'/{prefix}'
    try:
        client = boto3.client('s3')
        do_for_all_objects_all_versions(client, bucket, prefix, get_handler(client, bucket))
    except (ClientError, NoCredentialsError) as e:
        logging.error(e)
