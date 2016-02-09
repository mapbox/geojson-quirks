import uuid
import collections


def _flatten(d, parent_key='', sep='_'):
    # http://stackoverflow.com/a/6027615/519385
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


native_feature_keys = ("type", "geometry", "properties", "id")


def tweak_feature(
    feature,
    gather_properties=False,
    flatten=False,
    string_id=False,
    add_id=None,
    add_uuid=False,
    override_id=False,
    id_property=False):
    """Adjust the non-geo parts of a GeoJSON Feature
    This is a top level function that defines the order of
    operations.
    """

    # Handle id functions first
    if 'id' not in feature or override_id:
        if add_id is not None:
            feature['id'] = add_id
        if add_uuid:
            feature['id'] = str(uuid.uuid4())
        if id_property:
            feature['id'] = feature['properties'][id_property]

    if 'id' in feature and string_id:
        feature['id'] = str(feature['id'])

    # Next gather foreign objects to properties
    if gather_properties:
        new_properties = {}
        del_properties = []
        for k, v in feature.items():
            if k not in native_feature_keys:
                new_properties[k] = v
                del_properties.append(k)
        feature['properties'].update(new_properties)
        for p in del_properties:
            del feature[p]

    # and flatten properties
    if flatten:
        feature['properties'] = _flatten(feature['properties'])

    return feature
