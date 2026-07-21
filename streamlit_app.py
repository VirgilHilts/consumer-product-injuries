import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NEISS Injury Explorer", layout="wide")
st.title("NEISS Injury Explorer")
st.markdown("**National Estimates** — Colored by Average Severity")

# Load pre-aggregated data
@st.cache_data
def load_agg():
    return pd.read_csv('agg_all.csv')

agg = load_agg()

# Clean numbers
agg['national_estimate'] = agg['national_estimate'].round(0).astype(int)
agg['avg_Severity'] = agg['avg_Severity'].round(2)

# Load top 3 narratives with clickable links
@st.cache_data
def load_top_narr():
    return pd.read_csv('top_3_narratives.csv')

top_narr = load_top_narr()

# Merge
agg = agg.merge(top_narr, on=['broad_category', 'Prod'], how='left')

# ==================== ALL INJURIES ====================
st.subheader("All Injuries")
print(agg.columns)

fig = px.treemap(
    agg,
    path=['broad_category', 'Prod'],
    values='national_estimate',
    color='avg_Severity',
    color_continuous_scale=['#2ca02c', '#98df8a', '#ffbb78', '#ff7f0e', '#d62728'],
    range_color=(0, 1.0),
    title="All Injuries (National Estimates)",
    custom_data=agg[['top_3_narratives']] 
)

fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>" +
        "National Estimate: %{value:,.0f}<br>" +
        "Avg Severity: %{color:.2f}<br><br>" +
        "<b>Top 3 Narratives:</b><br>" +
        "%{customdata}"
    )
)


fig.update_layout(height=750)

st.plotly_chart(fig, use_container_width=True)

# ==================== SERIOUS INJURIES ONLY ====================
st.subheader("Amputations & Fatalities Only")

agg = pd.read_csv('agg_serious.csv')
agg = agg.merge(top_narr, on=['broad_category', 'Prod'], how='left')

fig = px.treemap(
    agg,
    path=['broad_category', 'Prod'],
    values='national_estimate',
    color='avg_Severity',
    color_continuous_scale=['#ffbb78', '#ff7f0e', '#d62728'],
    range_color=(2.0, 8.0),
    title="Amputations & Fatalities (National Estimates)",
    custom_data=agg[['top_3_narratives']]  
)

fig.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>" +
        "National Estimate: %{value:,.0f}<br>" +
        "Avg Severity: %{color:.2f}<br><br>" +
        "<b>Top 3 Narratives:</b><br>" +
        "%{customdata}"
    )
)

fig.update_layout(height=750)

st.plotly_chart(fig, use_container_width=True)
