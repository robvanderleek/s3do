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


def get_objects_batch(client, bucket, prefix, marker):
    if marker:
        return client.list_object_versions(Bucket=bucket,
                                           MaxKeys=1000, Prefix=prefix, KeyMarker=marker)
    else:
        return client.list_object_versions(Bucket=bucket,
                                           MaxKeys=1000, Prefix=prefix)


def tag_all_versions(client, bucket, object_list):
    global objects_tagged
    objects = []
    entries = object_list['Versions']
    for e in entries:
        objects.append({'VersionId': e['VersionId'], 'Key': e['Key']})
        if dry_run_mode:
            log('Tagging: ' + e['Key'])
    if dry_run_mode:
        return
    else:
        for o in objects:
            tag_object(client, bucket, o, 3)
            objects_tagged += 1
            if objects_tagged % 1000 == 0:
                log('Tagged ' + str(objects_tagged) + ' objects...')


def tag_object(client, bucket, obj, retries):
    global failures
    try:
        client.put_object_tagging(
            Bucket=bucket,
            Key=obj['Key'],
            VersionId=obj['VersionId'],
            Tagging={
                'TagSet': [
                    {'Key': 'HealthData', 'Value': 'True'},
                    {'Key': 'DataType', 'Value': 'Raw'}
                ]
            }
        )
    except:
        if retries > 0:
            tag_object(client, bucket, obj, retries - 1)
        else:
            log('WARNING: Tagging failed for object: ' + bucket + '/' + obj['Key'])
            failures += 1


def print_usage():
    print('usage: {} <bucket> <folder>'.format(sys.argv[0]))
    sys.exit(1)


def print_dry_run_warning():
    print('')
    print('RUN THIS SCRIPT WITH:')
    print('    --yes-i-am-sure')
    print('TO REALLY TAG THESE FILES')


def tag_objects(bucket, prefix, dry_run_mode):
    client = boto3.client('s3')
    has_more = True
    key_marker = None

    while has_more:
        object_list = get_objects_batch(client, bucket, prefix, key_marker)
        if 'Versions' in object_list:
            tag_all_versions(client, bucket, object_list)
        has_more = object_list['IsTruncated']
        key_marker = object_list['NextKeyMarker'] if 'NextKeyMarker' \
                                                     in object_list else None
        if dry_run_mode:
            has_more = False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_usage()
    bucket = sys.argv[1]
    prefix = sys.argv[2]
    prefix = prefix + '/' if not prefix.endswith('/') else prefix
    log('Tagging all objects in: ' + bucket + '/' + prefix)
    dry_run_mode = '--yes-i-am-sure' not in sys.argv
    tag_objects(bucket, prefix, dry_run_mode)
    log(f'Tagged total number of objects: {objects_tagged}, failures: {failures}')
    if dry_run_mode:
        print_dry_run_warning()


@click.command()
@click.argument('bucket')
@click.argument('prefix', required=False)
@click.option('--tag', '-t', required=True, multiple=True)
def tag(bucket, prefix, tag):
    print(f'BUCKET: {bucket}')
    print(f'PREFIX: {prefix}')
    print(f'tag: {tag}')
