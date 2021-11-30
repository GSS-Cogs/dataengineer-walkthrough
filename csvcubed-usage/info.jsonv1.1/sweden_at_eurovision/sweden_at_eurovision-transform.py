
# %%
from gssutils import *
import pandas as pd

# %%
scraper = Scraper(seed="sweden_at_eurovision-info.json")
scraper
# %%
data = pd.read_csv("sweden_eurovision.csv")
# %%
data
# %%
df = pd.melt(data, id_vars=["Artist", "Song", "Year", "Marker"], value_vars=["People On Stage", "Rank in Grand Final"], var_name="Measure", value_name="Observation")
# %%
df
# %%
df["Units"] = df["Measure"].apply(lambda x: "people" if x == "People On Stage" else "none")
df
# %%
df.to_csv("sweden_at_eurovision-observations.csv", index=False)
# %%
catalog = scraper.as_csvqb_catalog_metadata()
# %%
catalog.to_json_file("sweden_at_eurovision-catalog-metadata.json")
# %%
