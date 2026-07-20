import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('Full Labeled Set,csv')
df = df.copy()
df['broad_category'] = df['broad_category'].fillna("Other / Unknown")
df['Prod']   = df['Prod'].fillna("Unknown Product")



agg = df.groupby(['broad_category', 'Prod']).agg(
    national_estimate=('Weight', 'sum'),           # weighted national total
    Amputation=('Amputation', 'sum'),              # count of true cases
    Fatality=('Fatality', 'sum'),
    Hospitalized=('Hospitalized', 'sum'),
    avg_Severity=('Severity', 'mean'),             # average severity
    raw_count=('Weight', 'size')                   # optional: number of cases in sample
).reset_index()

# Round the average severity for nicer display
agg['avg_Severity'] = agg['avg_Severity'].round(2)

fig = px.treemap(
    agg,
    path=['broad_category', 'Prod'],
    values='national_estimate',
    color='avg_Severity',
    color_continuous_scale=['#2ca02c', '#98df8a', '#ffbb78', '#ff7f0e', '#d62728'],  # stronger gradient
    range_color=(0, 0.8),          # force the scale
    title=("Injury Treemap (National Estimates). "
           "Severity Codes: Fatality=8, Amputation=4, Hospitalization=2, All else=0"
           )
)

fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>" +
        "National Estimate: %{value:,.0f}<br>" +   # ← rounds to integer + commas
        "Severity: %{customdata[0]}"               # adjust if needed
    )
)

fig.update_layout(
    coloraxis_colorbar=dict(
        title="Avg Severity",
        tickvals=[0, 0.5, 1, 1.5, 2, 2.5, 3]
    )
)

fig.show()

# Save versions
fig.write_html("injury_treemap_diagnosis_severity.html")
fig.write_image("injury_treemap_diagnosis_severity.png", width=1400, height=900, scale=2)


