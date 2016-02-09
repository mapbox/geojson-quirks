import click
import cligj
import json
from collections import OrderedDict
from geojson_quirks import tweak_feature


@click.command('geojson-quirks')
@cligj.features_in_arg
@cligj.sequence_opt
@cligj.use_rs_opt
@click.option("--gather-properties", default=False, is_flag=True,
              help="any non-standard keys will be moved to Features.properties")
@click.option("--flatten", default=False, is_flag=True,
              help="flatten Feature.properties")
@click.option("--string-id", default=False, is_flag=True,
              help="casts the Feature.id (if exists) to a string")
@click.option("--add-id", default=False, is_flag=True,
              help="add an auto-incrementing integer as the Feature.id")
@click.option("--add-uuid", default=False, is_flag=True,
              help="add a unique string identifier as the Feature.id")
@click.option("--add-id-from-property", nargs=1, default=False,
              help="add a Feature.id from specified Feature.properties object")
@click.option("--override-id", default=False, is_flag=True,
              help="Allow options that manipulate Feature.id to overwrite")
@click.option("--type-first", default=False, is_flag=True,
              help="Put type element at beginning of FeatureCollection")
def main(features, sequence, use_rs, gather_properties, flatten,
         string_id, add_id, add_uuid, add_id_from_property,
         override_id, type_first):
    """Tweak your data to interoperate with quirky GeoJSON readers
    """
    if type_first and sequence:
        raise click.UsageError("--type-first cannot be used with --sequence")

    def process_features(features):
        for i, feature in enumerate(features):
            yield tweak_feature(
                feature,
                gather_properties=gather_properties,
                flatten=flatten,
                string_id=string_id,
                add_id=(i if add_id else None),
                add_uuid=add_uuid,
                override_id=override_id,
                id_property=add_id_from_property)

    if sequence:
        for feature in process_features(features):
            if use_rs:
                click.echo(b'\x1e', nl=False)
            click.echo(json.dumps(feature))
    else:
        if type_first:
            click.echo(json.dumps(
                OrderedDict([
                    ('type', 'FeatureCollection'),
                    ('features', list(process_features(features)))])))
        else:
            click.echo(json.dumps(
                {'type': 'FeatureCollection',
                 'features': list(process_features(features))}))
