import pandas as pd
import altair as alt
from pyodide.http import open_url

df = pd.read_csv(open_url("https://raw.githubusercontent.com/felicyairenea/Snapchat-Project/main/data/IN-ADH-90-days.csv"))

alt.renderers.set_embed_options(theme='dark')

#data cleaning
df = df.drop(columns=['inventory_id', 'campaign_id', 'adgroup_id', 'video_id', 'UU'])
df = df.dropna(axis=0)

df['adgroup_name'] = df['adgroup_name'].str.split(':')
df['adgroup'] = df.adgroup_name.apply(lambda x: x[0])
df['adtype'] = df.adgroup_name.apply(lambda x: x[1])
df = df.drop(columns=['adgroup_name'])

#trying to transform daily data into weekly data
new_df = df.copy()
new_df['Date'] = pd.to_datetime(new_df['Date'])
new_df.index = new_df['Date']
new_df = new_df.resample('W').mean()
new_df = new_df.reset_index()

alt.data_transformers.disable_max_rows()

pts = alt.selection(type = 'single', encodings=['x'])

circ = alt.Chart(new_df).mark_circle(color='goldenrod').encode(
    alt.X('Date:T', title='Weekly Date'),
    alt.Y('cost_usd:Q', title='Average Cost (in USD)'),
    alt.Size('installs:Q', 
        scale=alt.Scale(range=[0,1000]),
        legend=alt.Legend(orient='bottom', titleOrient='left')
        ),
    tooltip = ['Date','cost_usd','impressions','clicks']
).add_selection(
    pts
)

rect = alt.Chart(new_df).mark_bar().encode(
    alt.X('impressions:Q', bin=alt.BinParams(maxbins=8)),
    alt.Y('clicks:Q', bin=alt.BinParams(maxbins=8)),
    color=alt.condition(pts, 'd1_retention:Q', alt.value('lightgray'), scale=alt.Scale(scheme='magma'),
    )
)

line = alt.Chart(new_df).mark_line(color='lightcyan').encode(
    alt.X('Date:T'),
    alt.Y('d1_retention:Q'),
    tooltip=['Date','d1_retention','d7_retention']
)

circ | rect | line + line.mark_line(color='lightsalmon').encode(
    alt.Y('d7_retention:Q')
)