import logging

import boto3
import click
from botocore.exceptions import ClientError


def get_objects_batch(client, bucket, prefix, token):
    if token:
        return client.list_objects_v2(Bucket=bucket,
                                      MaxKeys=1000, Prefix=prefix, ContinuationToken=token)
    else:
        return client.list_objects_v2(Bucket=bucket,
                                      MaxKeys=1000, Prefix=prefix)


def list_objects(s3, bucket, prefix):
    has_more = True
    token = None
    while has_more:
        object_list = get_objects_batch(s3, bucket, prefix, token)
        for o in object_list['Contents']:
            print(f'{bucket},{o["Key"]}')
        has_more = object_list['IsTruncated']
        token = object_list['NextContinuationToken'] if has_more else None


@click.command()
@click.argument('bucket')
@click.argument('prefix', required=False)
def inventory(bucket, prefix):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s')
    try:
        client = boto3.client('s3')
        list_objects(client, bucket, prefix)
    except ClientError as e:
        logging.error(e)
