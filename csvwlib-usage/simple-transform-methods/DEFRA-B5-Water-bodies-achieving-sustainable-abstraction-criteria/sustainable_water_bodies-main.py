# %%
import pandas as pd
from gssutils import *

# %%
metadata = Scraper(seed='sustainable_water_bodies-info.json')
metadata.select_dataset(title = lambda x: "B5" in x)
metadata.dataset.family = 'climate-change'

# %%
distribution = metadata.distribution(latest=True)

# %%
df = distribution.as_pandas(encoding='ISO-8859-1')

# %%
df.to_csv('sustainable_water_bodies-observations.csv', index=False)

# %%
catalog_metadata = metadata.as_csvqb_catalog_metadata()
catalog_metadata.to_json_file('sustainable_water_bodies-catalog-metadata.json')
