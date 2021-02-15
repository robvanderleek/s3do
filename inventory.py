#!/usr/bin/env python
# Tags given folder (recursively, so all object, all versions) on S3 as:
#
#   {'HealthData': 'True', 'DataType': 'Raw'}
#
import boto3
from datetime import datetime

import click


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


import sys

sys.stdout = Unbuffered(sys.stdout)

objects_tagged = 0
failures = 0


def log(msg):
    now = datetime.now()
    print('[' + str(now.time()) + '] ' + msg)


def get_objects_batch(client, bucket, prefix, token):
    if token:
        return client.list_objects_v2(Bucket=bucket,
            MaxKeys=1000, Prefix=prefix, ContinuationToken=token)
    else:
        return client.list_objects_v2(Bucket=bucket,
            MaxKeys=1000, Prefix=prefix)


def list_objects(bucket, prefix):
    client = boto3.client('s3')
    has_more = True
    token = None
    while has_more:
        object_list = get_objects_batch(client, bucket, prefix, 
            token)
        for o in object_list['Contents']:
            print(f'{bucket},{o["Key"]}')
        has_more = object_list['IsTruncated']
        token = object_list['NextContinuationToken'] if has_more else None


def print_usage():
    print('usage: {} <bucket> <folder>'.format(sys.argv[0]))
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
    bucket = sys.argv[1]
    prefix = sys.argv[2]
    prefix = prefix + '/' if not prefix.endswith('/') else prefix
    list_objects(bucket, prefix)


@click.command()
@click.argument('bucket')
@click.argument('prefix', required=False)
@click.option('--tag', '-t', required=True, multiple=True)
def tag(bucket, prefix, tag):
    print(f'BUCKET: {bucket}')
    print(f'PREFIX: {prefix}')
    print(f'tag: {tag}')
