import logging

import boto3
import click
from botocore.exceptions import ClientError, NoCredentialsError

from s3do.utils import do_for_all_objects


def _tags_to_tagset(tags):
    result = []
    for t in tags:
        parts = t.split('=', 1)
        result.append({'Key': parts[0], 'Value': parts[1]})
    return result


def _get_callback(client, bucket, tagset):
    def tag_object(o):
        retries = 3
        while retries > 0:
            try:
                if 'VersionId' in o:
                    client.put_object_tagging(
                        Bucket=bucket,
                        Key=o['Key'],
                        VersionId=o['VersionId'],
                        Tagging={
                            'TagSet': tagset
                        }
                    )
                else:
                    client.put_object_tagging(
                        Bucket=bucket,
                        Key=o['Key'],
                        Tagging={
                            'TagSet': tagset
                        }
                    )
                return
            except Exception as e:
                print(e)
                if retries > 0:
                    retries -= 1
        logging.warning('Tagging failed for object: ' + bucket + '/' + o['Key'])

    return tag_object


def _tag_objects(client, bucket, prefix, tagset):
    do_for_all_objects(client, bucket, prefix, _get_callback(client, bucket, tagset))


@click.command()
@click.argument('bucket')
@click.argument('prefix', required=False)
@click.option('--tag', '-t', required=True, multiple=True)
def tag(bucket, prefix, tag):
    try:
        client = boto3.client('s3')
        tagset = _tags_to_tagset(tag)
        _tag_objects(client, bucket, prefix, tagset)
    except (ClientError, NoCredentialsError) as e:
        logging.error(e)
