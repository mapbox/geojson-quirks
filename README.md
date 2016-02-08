# geojson-quirks

Tweak your data to interoperate with quirky GeoJSON readers

## Why

Let's say you've got valid GeoJSON; you know it's valid since you ran it through [`geojson-hint`](https://github.com/mapbox/geojsonhint). But for some reason, another application, library or service doesn't like it. 

Well it turns out these quirks are pretty common in GeoJSON readers. In fact, they're so common that I'm writing a python library to encapsulate them, making it dead simple to **tweak the GeoJSON structure for the sake of interoperability**.

## Usage

What issues does this solve?

### Type first

Some GeoJSON readers assume that the `"type": "FeatureCollection"` property comes at the very top of the file. 

Pipe any FeatureCollection
```
echo '{
  "features": [ ... ],
  "type": "FeatureCollection"
}' | geojson-quirks --type-first
```

and get new (ordered) FeatureCollection on stdout
```
{
  "type": "FeatureCollection",
  "features": [ ... ]
}
```

### TODO


* add uuids
* stringify ids
* move all "foreign" members into properties
* flatten nested properties members to make it more tabular GIS friendly
