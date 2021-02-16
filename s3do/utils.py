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


def do_for_all_objects(client, bucket, prefix, func):
    has_more = True
    token = None
    while has_more:
        if prefix:
            object_list = _get_objects_batch_with_prefix(client, bucket, prefix, token)
        else:
            object_list = _get_objects_batch(client, bucket, token)
        for o in object_list['Contents']:
            func(o)
        has_more = object_list['IsTruncated']
        token = object_list['NextContinuationToken'] if has_more else None
