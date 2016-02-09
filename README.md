# geojson-quirks

Tweak your data to interoperate with quirky GeoJSON readers

## Why

You've got valid GeoJSON; you know it's valid since you ran it through [`geojson-hint`](https://github.com/mapbox/geojsonhint). But for some reason another application, library or service doesn't like it. 

Well it turns out these quirks are pretty common in GeoJSON readers. In fact, they're so common that I'm writing a python library to encapsulate them, making it dead simple to **tweak the GeoJSON structure for the sake of interoperability**.

## Installation

```
pip install -e git+https://github.com/mapbox/geojson-quirks.git#egg=geojson-quirks
```

## Usage

```
$ geojson-quirks --help
Usage: geojson-quirks [OPTIONS] FEATURES...

  Tweak your data to interoperate with quirky GeoJSON readers

Options:
  --sequence / --no-sequence   Write a LF-delimited sequence of texts
                               containing individual objects or write a single
                               JSON text containing a feature collection
                               object (the default).
  --rs / --no-rs               Use RS (0x1E) as a prefix for individual texts
                               in a sequence as per http://tools.ietf.org/html
                               /draft-ietf-json-text-sequence-13 (default is
                               False).
  --gather-properties          any non-standard keys will be moved to
                               Features.properties
  --flatten                    flatten Feature.properties
  --string-id                  casts the Feature.id (if exists) to a string
  --add-id                     add an auto-incrementing integer as the
                               Feature.id
  --add-uuid                   add a unique string identifier as the
                               Feature.id
  --add-id-from-property TEXT  add a Feature.id from specified
                               Feature.properties object
  --override-id                Allow options that manipulate Feature.id to
                               overwrite
  --type-first                 Put type element at beginning of
                               FeatureCollection
  --help                       Show this message and exit.
```

### Key ordering

Some GeoJSON readers assume that the `"type": "FeatureCollection"` property comes at the very top of the file. 

```
geojson-quirks --type-first
```

### Feature Identifiers

Features can optionally contain an `id` but some GeoJSON readers require them. You can add a `Feature.id` using a unique identifier string

    geojson-quirks --add-uuid

Or an auto-incrementing integer id.

    geojson-quirks --add-id

GeoJSON writers sometime put the effective feature id in the properties object. You can grab an id from your existing properties

    geojson-quirks --id-from-property "FID"

By default, all of the above operations won't touch existing ids; if you want to overwrite them with new values

    geojson-quirks --add-uuid --override-id

Or convert ids to strings if your reader requires it.

    geojson-quirks --string-id

## Properties

GeoJSON features require a `type, geometry, properties` and optionally specifies an `id`.
However, it is valid to put other keys in there (see `foo` in the example below):

```
{
    "id": 1,
    "type": "Feature",
    "properties": {
        "fid": 9001,
        "nest": {
            "a": 1,
            "b": 2}},
    "geometry": {"type": "Point", "coordinates": [0, 0]},
    "foo": "bar"
}
```

Many GIS applications expect all important data to live in a flat key:value properties object. 

You can gather all "foreign" members into the properties object.

    geojson-quirks --gather-properties
    # feature.properties.foo == "bar"

And flatten nested properties members to make it more tabular GIS friendly

    geojson-quirks --flatten
    # feature.properties.nest_a == 1
