This live demonstration is designed to show how quick it is to spin up a new dataset and get it into rdf

# Python transform
The python transform uses pandas and melt to take a multi-measure QB and output it in the necessary format.
```python
# %%
from gssutils import *
import pandas as pd
# %%
scraper = Scraper(seed="sweden_at_eurovision-info.json")
scraper
# %%
data = pd.read_csv("sweden_eurovision.csv")
data
# %%
data = pd.melt(data, id_vars=["Artist", "Song", "Year", "Marker"], value_vars=[
    "People On Stage", "Rank in Grand Final"], var_name="Measure", value_name="Observation")
data
# %%
data["Units"] = data["Measure"].apply(
    lambda x: "people" if x == "People On Stage" else "none")
data
# %%
data.to_csv("sweden_at_eurovision-observations.csv", index=False)
# %%
catalog = scraper.as_csvqb_catalog_metadata()
# %%
catalog.to_json_file("sweden_at_eurovision-catalog-metadata.json")
```

# `Info.json`
The `info.json` uses the schema validation to suggest what we need filling in, and creates the necessary components from the data as described in the markup.
```json
{
    "$schema": "http://gss-cogs.github.io/family-schemas/dataset-schema-1.1.0.json",
    "title": "Sweden at Eurovision",
    "id": "sweden-at-eurovision",
    "description": "Swedish entries at Eurovision",
    "published": "2021-10-13",
    "landingPage": "https://www.sixonstage.com/",
    "publisher": "Six on stage",
    "dataURL": "http://example.com/file.csv",
    "families": [
        "Eurovision"
    ],
    "transform": {
        "airtable": "rec84747382947543",
        "columns": {
            "Artist": {
                "type": "dimension"
            },
            "Song": {
                "type": "attribute"
            },
            "Year": {
                "type": "dimension",
                "new": {
                    "subPropertyOf": "http://purl.org/linked-data/sdmx/2009/dimension#refPeriod",
                    "codelist": false
                },
                "value": "https://reference.data.gov.uk/id/year/{+year}"
            },
            "Marker": {
                "type": "attribute"
            },
            "Measure": {
                "type": "measures"
            },
            "Observation": {
                "type": "observations"
            },
            "Units": {
                "type": "units"
            }
        }
    }
}
```

# Build command
Docker is used to serialise the csvw into valid RDF, though we're only concerned so far with the main transformation
```shell
docker run -it --rm -v $(pwd):/workspace -w /workspace gsscogs/csv2rdf sh -c 'csv2rdf -u artist.csv-metadata.json -m annotated | sed -e "s/file\:\//http\:\/\//" | riot --syntax=Turtle --output=Turtle' > artist.ttl
docker run -it --rm -v $(pwd):/workspace -w /workspace gsscogs/csv2rdf sh -c 'csv2rdf -u year.csv-metadata.json -m annotated | sed -e "s/file\:\//http\:\/\//" | riot --syntax=Turtle --output=Turtle' > year.ttl
docker run -it --rm -v $(pwd):/workspace -w /workspace gsscogs/csv2rdf sh -c 'csv2rdf -u sweden-at-eurovision.csv-metadata.json -m annotated | sed -e "s/file\:\//http\:\/\//" | riot --syntax=Turtle --output=Turtle' > dataset.ttl

```