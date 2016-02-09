import pytest
from geojson_quirks import tweak_feature

@pytest.fixture
def feature():
    return {
        'id': 1,
        'type': "Feature",
        'properties': {
            'fid': 9001,
            'nest': {
                'a': 1,
                'b': 2}},
        'geometry': {
            'type': "Point",
            'coordinates': [0, 0]},
        'foo': 'bar'}


def test_id_overwrite(feature):
    f = tweak_feature(feature, override_id=False, add_uuid=True)
    assert f['id'] == 1
    f = tweak_feature(feature, override_id=True, add_uuid=True)
    assert f['id'] != 1


def test_id_num(feature):
    del feature['id']
    f = tweak_feature(feature, add_id=2)
    assert f['id'] == 2


def test_id_uuid(feature):
    del feature['id']
    f = tweak_feature(feature, add_uuid=True)
    assert len(f['id']) == len('4d43adbf-7ab7-4f73-9f0c-bf81fd5c474b')


def test_noop(feature):
    f = tweak_feature(feature)
    assert f == feature


def test_id_property(feature):
    del feature['id']
    f = tweak_feature(feature, id_property='fid')
    assert f['id'] == 9001


def test_id_property_fail(feature):
    del feature['id']
    with pytest.raises(KeyError):
        tweak_feature(feature, id_property='fud')


def test_id_string(feature):
    f = tweak_feature(feature, string_id=True)
    assert f['id'] == "1"


def test_id_chain(feature):
    del feature['id']
    f = tweak_feature(feature, string_id=True, id_property='fid')
    assert f['id'] == "9001"


def test_gather(feature):
    assert 'foo' in feature
    assert 'foo' not in feature['properties']
    f = tweak_feature(feature, gather_properties=True)
    assert 'foo' in f['properties']
    assert 'foo' not in f

def test_flatten(feature):
    f = tweak_feature(feature, flatten=True)
    assert f['properties']['fid'] == 9001
    assert f['properties']['nest_a'] == 1
    assert f['properties']['nest_b'] == 2
    assert 'nest' not in f['properties']
