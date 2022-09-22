import numpy as np
import pandas as pd
import altair as alt
from pyodide.http import open_url

alt.renderers.set_embed_options(theme='dark')

url="https://raw.githubusercontent.com/felicyairenea/Snapchat-Project/main/data/IN-ADH-90-days.csv"
df = pd.read_csv(open_url(url),parse_dates=["Date"])
df = df.drop(columns=["video_id", 'inventory_id', 'campaign_id', 'adgroup_id', 'UU'], index=None)

df["click_through_rate"] = df.clicks/df.impressions
df["cost_per_thousand_impressions"] = df.cost_usd/df.impressions*1000
df["d1_retention_rate"] = df.d1_retention/df.installs
df["d7_retention_rate"] = df.d7_retention/df.installs
df["conversion_rate"] = df.installs/df.clicks
df["cost_per_conversion"] = df.cost_usd/df.installs

df = df[(df.d1_retention_rate >= df.d7_retention_rate)]
df = df.dropna()

df["ad_group"] = df.adgroup_name.apply(lambda x: x.split(":")[0])
df["ad_type"] = df.adgroup_name.apply(lambda x: x.split(":")[1])

df_group = df.groupby(["Date", "ad_group"]).mean().reset_index()

alt.data_transformers.disable_max_rows()

highlight= alt.selection(
    type='single', on='mouseover', fields=['Date'], nearest=True)

# CTR Analysis per Ad Group
g1 = alt.Chart(df_group).mark_line().encode(
    alt.X('yearmonth(Date):T',
         axis = alt.Axis(title="Date")),
    alt.Y('average(click_through_rate):Q',
         axis = alt.Axis(title="Average Click Through Rate (CTR)")),
    tooltip=['yearmonth(Date):T','average(click_through_rate)'],
    color=alt.Color(
        'ad_group:N',
        legend=alt.Legend(
            title = 'Ad Group',
        )
    )
).properties(
    title = "Average Click Through Rate through Time per Ad Group"
).mark_line(interpolate="basis", color="#19615b"
).add_selection(highlight).interactive()

# CTR Analysis per Ad Type
df_group_2 = df.groupby(["Date", "ad_group","ad_type"]).mean().reset_index()

g2 = alt.Chart(df_group_2).mark_line().encode(
    alt.X('yearmonth(Date):T',
         axis = alt.Axis(title="Date")),
    alt.Y('average(click_through_rate):Q',
         axis = alt.Axis(title="Average Click Through Rate (CTR)")),
    color=alt.Color(
        'ad_type:N',
        legend=alt.Legend(
            title = 'Ad Group',
        )
    )
).properties(
    title = "Average Click Through Rate through Time per GMOB's Ad Type"
).transform_filter(
    alt.FieldOneOfPredicate(field='ad_group', oneOf=["gmob"])
).mark_line(interpolate="basis", color="#19615b").interactive()

g3 = alt.Chart(df_group_2).mark_line().encode(
    alt.X('yearmonth(Date):T',
         axis = alt.Axis(title="Date")),
    alt.Y('average(click_through_rate):Q',
         axis = alt.Axis(title="Average Click Through Rate (CTR)")),
    color=alt.Color(
        'ad_type:N',
        legend=alt.Legend(
            title = 'Ad Group',
        )
    )
).properties(
    title = "Average Click Through Rate through Time per MGDN's Ad Type"
).transform_filter(
    alt.FieldOneOfPredicate(field='ad_group', oneOf=["mgdn"])
).mark_line(interpolate="basis", color="#19615b").interactive()

g4 = alt.Chart(df_group_2).mark_line().encode(
    alt.X('yearmonth(Date):T',
         axis = alt.Axis(title="Date")),
    alt.Y('average(click_through_rate):Q',
         axis = alt.Axis(title="Average Click Through Rate (CTR)")),
    color=alt.Color(
        'ad_type:N',
        legend=alt.Legend(
            title = 'Ad Group',
        )
    )
).properties(
    title = "Average Click Through Rate through Time per Youtube's Ad Type"
).transform_filter(
    alt.FieldOneOfPredicate(field='ad_group', oneOf=["youtube"])
).mark_line(interpolate="basis", color="#19615b").interactive()

# CPM Analysis Per Ad Group
g5 = alt.Chart(df_group).mark_line().encode(
    alt.X('yearmonth(Date):T',
          axis = alt.Axis(title="Date")),
    alt.Y('average(cost_per_thousand_impressions):Q',
         axis = alt.Axis(title="Average Cost per Thousand Impressions")),
    color=alt.Color(
        'ad_group:N',
        legend=alt.Legend(
            title = 'Ad Group'
        )
    )
).properties(
    title="Average Cost per Thousand Impressions through Time per Ad Group"
).mark_line(
    interpolate="basis", color="#19615b"
).interactive()

# Conversion Rate Analysis per Ad Group
g6 = alt.Chart(df_group).mark_line().encode(
    alt.X('yearmonth(Date):T',
          axis = alt.Axis(title="Date")),
    alt.Y('average(conversion_rate):Q',
         axis = alt.Axis(title="Average Conversion Rate")),
    color=alt.Color(
        'ad_group:N',
        legend=alt.Legend(
            title = 'Ad Group',
        )
    )
).properties(
    title = "Average Conversion Rate through Time per Ad Group"
).mark_line(interpolate="basis", color="#19615b")

# Conversion Rate Analysis per Ad Type
g7 = alt.Chart(df_group_2).mark_line().encode(
    alt.X('yearmonth(Date):T',
          axis = alt.Axis(title="Date")),
    alt.Y('average(conversion_rate):Q',
         axis = alt.Axis(title="Average Conversion Rate")),
    color=alt.Color(
        'ad_type:N',
        legend=alt.Legend(title = 'Ad Type')
    )
).properties(
    title = "Average Conversion Rate through Time per MGDN's Ad Type"
).transform_filter(
    alt.FieldOneOfPredicate(field='ad_group', oneOf=["mgdn"])
).mark_line(interpolate="basis", color="#19615b")

g8 = alt.Chart(df_group_2).mark_line().encode(
    alt.X('yearmonth(Date):T',
          axis = alt.Axis(title="Date")),
    alt.Y('average(conversion_rate):Q',
         axis = alt.Axis(title="Average Conversion Rate")),
    color=alt.Color(
        'ad_type:N',
        legend=alt.Legend(title = 'Ad Type')
    )
).properties(
    title = "Average Conversion Rate through Time per Yooutube's Ad Type"
).transform_filter(
    alt.FieldOneOfPredicate(field='ad_group', oneOf=["youtube"])
).mark_line(interpolate="basis", color="#19615b").interactive()

# Cost Per Conversion Analysis
g9 = alt.Chart(df_group).mark_line().encode(
    alt.X('yearmonth(Date):T',
          axis = alt.Axis(title="Date")),
    alt.Y('average(cost_per_conversion):Q',
         axis = alt.Axis(title="Average Cost per Conversions")),
    color=alt.Color(
        'ad_group:N',
        legend=alt.Legend(
            title = 'Ad Group'
        )
    )
).properties(
    title="Average Cost per Conversions through Time per Ad Group"
).mark_line(
    interpolate="basis", color="#19615b"
).interactive()

base = alt.Chart(df_group).encode(
    alt.X('yearmonth(date):T', axis=alt.Axis(title="Date"))
)


alt.vconcat(g1, g5)|alt.vconcat(g6, g9)


