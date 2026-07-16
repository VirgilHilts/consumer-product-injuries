import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NEISS Injury Explorer", layout="wide")
st.title("NEISS Injury Treemap (National Estimates)")
st.markdown("**Colored by Average Severity** — Fatality=8, Amputation=4, Hospitalized=2, All else=0")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('aggregated.csv')
    df = df.copy()
    return df

agg = load_data()


# Filters
col1, col2 = st.columns([3, 1])
with col1:
    selected_categories = st.multiselect(
        "Filter Broad Categories",
        options=sorted(agg['broad_category'].unique()),
        default=sorted(agg['broad_category'].unique())
    )

with col2:
    min_sev = st.slider("Minimum Avg Severity", 0.0, 3.0, 0.0, 0.05)

# Filtered data
filtered = agg[
    (agg['broad_category'].isin(selected_categories)) & 
    (agg['avg_Severity'] >= min_sev)
]

# Treemap
fig = px.treemap(
    filtered,
    path=['broad_category', 'Prod'],
    values='national_estimate',
    color='avg_Severity',
    color_continuous_scale=['#2ca02c', '#98df8a', '#ffbb78', '#ff7f0e', '#d62728'],
    range_color=(0, 1.0),
    title="Injury Treemap (National Estimates)"
)

# In the treemap hover template (make sure it shows clean numbers)
fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>" +
        "National Estimate: %{value:,.0f}<br>" +   # this already rounds nicely
        "Avg Severity: %{color:.2f}"
    )
)
fig.update_layout(height=800)
st.plotly_chart(fig, use_container_width=True)

# Summary table
st.subheader("Summary Table")
st.dataframe(filtered.sort_values('national_estimate', ascending=False), use_container_width=True)

# Downloads
st.download_button("Download Treemap as HTML", fig.to_html(), "injury_treemap.html")
st.download_button("Download Data as CSV", filtered.to_csv(index=False), "injury_data.csv")
