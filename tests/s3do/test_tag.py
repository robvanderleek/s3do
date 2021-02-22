from s3do.tag import _tags_to_tagset


def test_tag_to_tagset_empty_set():
    result = _tags_to_tagset([])

    assert len(result) == 0


def test_tag_to_tagset_one_element():
    result = _tags_to_tagset(('aap=noot',))

    assert len(result) == 1
    assert result[0]['Key'] == 'aap'
    assert result[0]['Value'] == 'noot'


def test_tag_to_tagset_two_elements():
    result = _tags_to_tagset(('aap=noot', 'mies=wim'))

    assert len(result) == 2
    assert result[0]['Key'] == 'aap'
    assert result[0]['Value'] == 'noot'
    assert result[1]['Key'] == 'mies'
    assert result[1]['Value'] == 'wim'
