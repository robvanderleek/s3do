def _get_objects_batch(client, bucket, token):
    if token:
        return client.list_objects_v2(Bucket=bucket, MaxKeys=1000, ContinuationToken=token)
    else:
        return client.list_objects_v2(Bucket=bucket, MaxKeys=1000)


def _get_objects_batch_with_prefix(client, bucket, prefix, token):
    if token:
        return client.list_objects_v2(Bucket=bucket, MaxKeys=1000, Prefix=prefix, ContinuationToken=token)
    else:
        return client.list_objects_v2(Bucket=bucket, MaxKeys=1000, Prefix=prefix)


def _get_objects_batch_all_versions(client, bucket, marker):
    if marker:
        return client.list_object_versions(Bucket=bucket, MaxKeys=1000, KeyMarker=marker)
    else:
        return client.list_object_versions(Bucket=bucket, MaxKeys=1000)


def _get_objects_batch_all_versions_with_prefix(client, bucket, prefix, marker):
    if marker:
        return client.list_object_versions(Bucket=bucket, MaxKeys=1000, Prefix=prefix, KeyMarker=marker)
    else:
        return client.list_object_versions(Bucket=bucket, MaxKeys=1000, Prefix=prefix)


def do_for_all_objects_all_versions(client, bucket, prefix, func):
    has_more = True
    key_marker = None
    while has_more:
        if prefix:
            object_list = _get_objects_batch_all_versions_with_prefix(client, bucket, prefix, key_marker)
        else:
            object_list = _get_objects_batch_all_versions(client, bucket, key_marker)
        if 'Versions' in object_list:
            entries = object_list['Versions']
            for e in entries:
                func({'VersionId': e['VersionId'], 'Key': e['Key']})
        has_more = object_list['IsTruncated']
        key_marker = object_list['NextKeyMarker'] if has_more else None


def do_for_all_objects(client, bucket: str, prefix, func):
    has_more = True
    token = None
    while has_more:
        if prefix:
            object_list = _get_objects_batch_with_prefix(client, bucket, prefix, token)
        else:
            object_list = _get_objects_batch(client, bucket, token)
        if 'Contents' in object_list:
            for o in object_list['Contents']:
                func(o)
        has_more = object_list['IsTruncated']
        token = object_list['NextContinuationToken'] if has_more else None
