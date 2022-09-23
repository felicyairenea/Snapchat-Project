import json
import pandas as pd
import altair as alt
from pyodide.http import open_url

df = pd.read_csv(open_url("https://raw.githubusercontent.com/felicyairenea/Snapchat-Project/main/data/IN-ADH-90-days.csv"), parse_dates=["Date"])

#data cleaning
df = df.drop(columns=['inventory_id', 'campaign_id', 'adgroup_id', 'video_id', 'UU'])
df = df.dropna(axis=0)

df['adgroup_name'] = df['adgroup_name'].str.split(':')
df['adgroup'] = df.adgroup_name.apply(lambda x: x[0])
df['adtype'] = df.adgroup_name.apply(lambda x: x[1])

df["d1_retention_rate"] = df.d1_retention/df.installs
df["d7_retention_rate"] = df.d7_retention/df.installs
df["click_through_rate"] = df.clicks/df.impressions
df["conversion_rate"] = df.installs/df.clicks

df = df[(df.d1_retention_rate >= df.d7_retention_rate)]
df = df.drop(columns=['adgroup_name'])

group1 = df.groupby(['adgroup','adtype']).mean().reset_index()

# for key data
# =====================

sum_of_clicks = sum(df["clicks"])
sum_of_impressions = sum(df["impressions"])
max_CTR = max(group1["click_through_rate"])
max_conversion = max(group1["conversion_rate"])
from_date = min(df['Date']).strftime('%B %d')
to_date = max(df['Date']).strftime('%B %d')


key_data = [
    round(sum_of_clicks,3),
    round(sum_of_impressions,3),
    round(max_CTR,3),
    round(max_conversion,3),
    [
        from_date,
        to_date,
        from_date,
        to_date,
        from_date,
        to_date,
        from_date,
        to_date,
    ]
    
]

print(json.dumps(key_data))
