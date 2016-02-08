import click
import cligj
import json
from collections import OrderedDict


@click.command('geojson-quirks')
@cligj.features_in_arg
@cligj.sequence_opt
@cligj.use_rs_opt
@click.option("--type-first", default=False, is_flag=True,
              help="Put type element at beginning of FeatureCollection")
def main(features, sequence, use_rs, type_first):
    if type_first and sequence:
        raise click.UsageError("--type-first cannot be used with --sequence")

    def process_features(features):
        for feature in features:
            # TODO
            # Massage features based on other options
            yield feature

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
