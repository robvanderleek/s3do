import logging

import boto3
import click
from botocore.exceptions import ClientError, NoCredentialsError

from s3do.utils import do_for_all_objects_all_versions


def _tags_to_tagset(tags):
    result = []
    for t in tags:
        parts = t.split('=', 1)
        result.append({'Key': parts[0], 'Value': parts[1]})
    return result


def get_callback(client, bucket, tagset):
    def tag_object(o):
        retries = 3
        while retries > 0:
            try:
                client.put_object_tagging(
                    Bucket=bucket,
                    Key=o['Key'],
                    VersionId=o['VersionId'],
                    Tagging={
                        'TagSet': tagset
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
    try:
        client = boto3.client('s3')
        tagset = _tags_to_tagset(tag)
        do_for_all_objects_all_versions(client, bucket, prefix, get_callback(client, bucket, tagset))
    except (ClientError, NoCredentialsError) as e:
        logging.error(e)
