import pandas as pd
import altair as alt
from pyodide.http import open_url

df = pd.read_csv(open_url("https://raw.githubusercontent.com/felicyairenea/Snapchat-Project/main/data/IN-ADH-90-days.csv"))

#data cleaning
df = df.drop(columns=['inventory_id', 'campaign_id', 'adgroup_id', 'video_id', 'UU'])
df = df.dropna(axis=0)

df['adgroup_name'] = df['adgroup_name'].str.split(':')
df['adgroup'] = df.adgroup_name.apply(lambda x: x[0])
df['adtype'] = df.adgroup_name.apply(lambda x: x[1])
df = df.drop(columns=['adgroup_name'])

group1 = df.groupby(['adgroup','adtype']).sum().reset_index()
print(group1.to_html())