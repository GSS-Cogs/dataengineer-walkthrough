# csvwlib-flavoured transforms
This only so far covers how to convert existing `gss-utils` transformations to new-style csvwlib transforms.

## Example 1 - Single-measure dataset with virtual measure/units
The `DEFRA-B5-Water-bodies-achieving-sustainable-abstraction-criteria` dataset has been converted to the new csvwlib-flavoured methods for CSV-W generation. These changes involve adopting new conventions regarding the naming of files and how to mange the transform. The generation of the csv-w exists outside of the transform python file for now.

The dataset is a basic csv file comprised of a known character encoding and three columns.

1. One existing dimension (i.e. `Year` is subPropertyOf `refPeriod`)
2. New dimension `Water body category` needs a codelist
3. Observations are tied to existing units and measures

The original transform pathified the contents of the dataset and used the `cubes()` class to output the transformed dataset and associated files. The new method skips initialising the cube class and instead uses the `CatalogMetadata` to capture attributes of the dataset not configured within the original `info.json`. The `CatalogMetadata` is output as `datasetname-metadata.json` to match the `datasetname-main.py` and `dataset-info.json` files. Additionally, the `dataset-observations.csv` is output without the transforms.

This new method, with updates to the `info.json` in the new `v1.1` release gives data engineers quick new ways to declare dataset-local dimensions with code lists. Including a reference to the `$schema` at the start of an `info.json` provides schema validation in both Visual Studio Code and PyCharm.

### Changes to python-pipeline
The differences below are a comparison using git's diff tool between `main.py` and `sustainable_water_bodies-main.py`

```diff
-# DEFRA-B5-Water-bodies-achieving-sustainable-abstraction-criteria
-
-#%%
-import json
+# %%
 import pandas as pd
 from gssutils import *
 
 # %%
-df = pd.DataFrame()
-cubes = Cubes('info.json')
-info = json.load(open('info.json'))
-
-# %%
-metadata = Scraper(seed='info.json')
+metadata = Scraper(seed='sustainable_water_bodies-info.json')
 metadata.select_dataset(title = lambda x: "B5" in x)
 metadata.dataset.family = 'climate-change'
 
 # %%
 distribution = metadata.distribution(latest=True)
-title = distribution.title
 
 # %%
 df = distribution.as_pandas(encoding='ISO-8859-1')
 
 # %%
-#Post Processing 
-df['Water body category'] = df['Water body category'].apply(pathify)
+df.to_csv('sustainable_water_bodies-observations.csv', index=False)
 
 # %%
-cubes.add_cube(metadata, df, title)
-cubes.output_all()
+catalog_metadata = metadata.as_csvqb_catalog_metadata()
+catalog_metadata.to_json_file('sustainable_water_bodies-catalog-metadata.json')
```

### Changes to the info.json
The differences below are made using `git diff --no-index` between `info.json` and `sustainable_water_bodies-info.json`. The main difference in `info.json` `v1.1` is that dimensions, attributes, measures, units, etc. are all explicitly declared instead of being implied based on the keys within the `column` declaration. This explitic notation allows for new functionality, like the new local codelist for `Water body category`.
```diff
 {
+    "$schema": "http://gss-cogs.github.io/family-schemas/dataset-schema-1.1.0.json",
     "id": "defra-b5-water-bodies-achieving-sustainable-abstraction-criteria",
     "title": "B5: Water bodies achieving sustainable abstraction criteria",
     "publisher": "Department for Environment Food & Rural Affairs",
     "description": "Part of The Outcome Indicator Framework, a comprehensive set of indicators describing  environmental change that relates to the 10 goals within the 25 Year Environment Plan. The framework contains 66  indicators, arranged into 10 broad themes. The indicators are extensive; they cover natural capital assets (for  example, land, freshwater, air and seas) and together they show the condition of these assets, the pressures  acting upon them and the provision of services or benefits they provide.",
     "landingPage": "https://oifdata.defra.gov.uk/2/",
     "datasetNotes": [
         "On landing page scroll down to dataset link with dataset title.",
         "Direct link to download: ",
         "https://oifdata.defra.gov.uk/en/data/2-5-1.csv",
         "Dashboard landing page is https://oifdata.defra.gov.uk/."
     ],
     "published": "2021-06-11",
     "families": [
-        "Climate Change"
+        "Climate-Change"
     ],
     "extract": {
         "source": "CSV",
         "stage": "Documented"
     },
     "transform": {
         "stage": [
             "Priority"
         ],
         "airtable": "recO1acFhSc60CNxF",
         "main_issue": 40,
         "columns": {
             "Year": {
-                "parent": "http://purl.org/linked-data/sdmx/2009/dimension#refPeriod",
+                "type": "dimension",
+                "uri": "http://purl.org/linked-data/sdmx/2009/dimension#refPeriod",
                 "value": "http://reference.data.gov.uk/id/year/{+year}"
             },
             "Water body category": {
-                "dimension": "http://gss-data.org.uk/def/climate-change/property/dimension/water-body-category",
+                "type": "dimension",
+                "new": {
+                    "label": "Water body category",
+                    "codelist": true
+                },
                 "value": "http://gss-data.org.uk/def/climate-change/concept/water-body-category/{water_body_category}"
             },
             "Value": {
+                "type": "observations",
                 "unit": "http://gss-data.org.uk/def/climate-change/concept/measurement-unit/percentage-change",
                 "measure": "http://gss-data.org.uk/def/climate-change/measure/surface-ground-water-bodies",
                 "datatype": "double"
            }
        }
    },
    "sizingNotes": "Small, simple CSV dataset",
    "notes": "Priority dataset for Climate Change Platform project."
}
```

### Differences in the output
Using the associated `.devcontainer.json` (or the docker container `gsscogs/databaker:test`) try running both pipelines and check the output. For less code and slightly more `info.json` keys, we now have a defined catalog entry, a local codelist (which generates both value/label pairs because the dataframe wasn't patified), and virtual columns.