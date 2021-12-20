# How to Generate Catalog Metadata

There are two approaches to generating catalog metadata; you can either generate the required metadata from a scraper or, if the data is not acquired with a scraper, you can define the [CatalogMetadata](https://github.com/GSS-Cogs/csvwlib/blob/main/csvcubed/csvcubed/models/cube/qb/catalog.py) yourself.

Whether you decide to define your catalog metadata in Python or using JSON, make sure that the name of the file matches with the expected [naming conventions](./Naming%20Convention.md), e.g. `{cube-name}-catalog-metadata.json`.

## Using a Scraper

```python
from csvcubed.models.cube.qb.catalog import CatalogMetadata

scraper = Scraper(seed='info.json')

# Acquisition of the data from the scraper happens here.

# The scraper can be instructed to generate the catalog metadata by taking information 
# from the info.json file and adding metadata from the publications' website.
catalog_metadata: CatalogMetadata = scraper.as_csvqb_catalog_metadata()

catalog_metadata.to_json_file('catalog-metadata.json')
```

## Manually Defining Catalog Metadata

Note that the below code samples show you how to download all of the relevant catalog metadata fields. It is not necessary to define all of these fields. Strictly speaking, defining the `title` is the only definition which is **required**.

### In Python

```python
from csvcubed.models.cube.qb.catalog import CatalogMetadata
from datetime import datetime

catalog_metadata: CatalogMetadata = CatalogMetadata(
    title="Some Dataset",
    summary="Some catalog item summary",
    description="Some catalog item description",
    identifier="some-dataset-identifier",
    keywords=[
        "Some key word"
    ],
    theme_uris=[
        "http://gss-data.org.uk/def/gdp#the-theme-uri"
    ],
    landing_page_uris=[
        "http://department-website.gov.uk/this-dataset/download"
    ],
    creator_uri="https://www.gov.uk/government/organisations/department-which-created-this-dataset",
    publisher_uri="https://www.gov.uk/government/organisations/department-which-published-this-dataset",
    license_uri="http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    dataset_issued=datetime(2020, 10, 5),
    dataset_modified=datetime(2020, 10, 5),
    public_contact_point_uri="mailto:some-contact-point@department-website.gov.uk"
)

catalog_metadata.to_json_file('catalog-metadata.json')
```

### In JSON

```json
{
    "title": "Some Dataset",
    "identifier": "some-dataset-identifier",
    "summary": "Some catalog item summary",
    "description": "Some catalog item description",
    "creator_uri": "https://www.gov.uk/government/organisations/department-which-created-this-dataset",
    "publisher_uri": "https://www.gov.uk/government/organisations/department-which-published-this-dataset",
    "landing_page_uris": [
      "http://department-website.gov.uk/this-dataset/download"
    ],
    "theme_uris": [
        "http://gss-data.org.uk/def/gdp#the-theme-uri"
    ],
    "keywords": [
        "Some key word"
    ],
    "dataset_issued": "2020-01-05T00:00:00",
    "dataset_modified": "2020-01-05T00:00:00",
    "license_uri": "http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    "public_contact_point_uri": "mailto:some-contact-point@department-website.gov.uk"
}
```

**N.B. We do not currently have a schema file to help you write these JSON files.**

## Further Information

* [CatalogMetadata Python Definition](https://github.com/GSS-Cogs/csvwlib/blob/main/csvcubed/csvcubed/models/cube/qb/catalog.py) - Defines the fields and validations which are performed on the `catalog-metadata.json` files upon ingestion in [infojson2csvqb](https://github.com/GSS-Cogs/gss-utils/blob/csvwlib-integration/gssutils/csvcubedintegration/infojson2csvqb/README.md).
* [CatalogMetadata API Documentation](https://ci.floop.org.uk/job/GSS_data/job/csvwlib/job/main/lastSuccessfulBuild/artifact/csvcubed/docs/_build/html/csvcubed.models.cube.qb.html#catalog-metadata-dcat) - Contains an up-to-date list of all of the properties contained on the CatalogMetadata class.
