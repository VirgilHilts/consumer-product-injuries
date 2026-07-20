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
    return pd.read_pickle('top_3_narratives.pkl')

top_narr = load_top_narr()

# Merge
agg = agg.merge(top_narr, on=['broad_category', 'Prod'], how='left')

# ==================== ALL INJURIES ====================
st.subheader("All Injuries")
fig_all = px.treemap(
    agg,
    path=['broad_category', 'Prod'],
    values='national_estimate',
    color='avg_Severity',
    color_continuous_scale=['#2ca02c', '#98df8a', '#ffbb78', '#ff7f0e', '#d62728'],
    range_color=(0, 1.0),
    title="All Injuries (National Estimates)"
)

fig_all.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>" +
        "National Estimate: %{value:,.0f}<br>" +
        "Avg Severity: %{color:.2f}<br><br>" +
        "<b>Top 3 Narratives:</b><br>" +
        "%{customdata[0]}"
    ),
    customdata=['top_3_narratives']
)
fig_all.update_layout(height=750)

st.plotly_chart(fig_all, use_container_width=True)

# ==================== SERIOUS INJURIES ONLY ====================
st.subheader("Amputations & Fatalities Only")

serious_agg = agg[agg['avg_Severity'] >= 2.0].copy()

fig_serious = px.treemap(
    serious_agg,
    path=['broad_category', 'Prod'],
    values='national_estimate',
    color='avg_Severity',
    color_continuous_scale=['#ffbb78', '#ff7f0e', '#d62728'],
    range_color=(2.0, 4.0),
    title="Amputations & Fatalities Only (National Estimates)"
)

fig_serious.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>" +
        "National Estimate: %{value:,.0f}<br>" +
        "Avg Severity: %{color:.2f}<br><br>" +
        "<b>Top 3 Narratives:</b><br>" +
        "%{customdata[0]}"
    ),
    customdata=['top_3_narratives']
)
fig_serious.update_layout(height=750)

st.plotly_chart(fig_serious, use_container_width=True)
