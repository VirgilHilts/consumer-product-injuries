import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NEISS Injury Explorer", layout="wide")
st.title("NEISS Injury Explorer")
st.markdown("**National Estimates** — Colored by Average Severity")

# Load pre-aggregated data (much smaller)
@st.cache_data
def load_agg_all():
    return pd.read_csv('agg_all.csv')   # ← your pre-computed file

agg = load_agg_all()

# Optional: make sure numbers are clean
agg['national_estimate'] = agg['national_estimate'].round(0).astype(int)
agg['avg_Severity'] = agg['avg_Severity'].round(2)

# In streamlit_app.py
top_narr = pd.read_csv('top_3_narratives.csv')   

# Merge with agg
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
    title="All Injuries (National Estimates)",
    custom_data=['top_3_narratives']
)

fig_all.update_traces(
    hovertemplate="<b>%{label}</b><br>National Estimate: %{value:,.0f}<br>Avg Severity: %{color:.2f}"
)
fig_all.update_layout(height=750)

st.plotly_chart(fig_all, use_container_width=True)

# ==================== SERIOUS INJURIES ONLY ====================

st.subheader("Amputations & Fatalities Only")

def load_agg_serious():
    return pd.read_csv('agg_serious.csv')   # ← your pre-computed file

agg_serious = load_agg_serious()

agg_serious['national_estimate'] = agg_serious['national_estimate'].round(0).astype(int)
agg_serious['avg_Severity'] = agg_serious['avg_Severity'].round(2)

fig_serious = px.treemap(
    agg_serious,
    path=['broad_category', 'Prod'],
    values='national_estimate',
    color='avg_Severity',
    color_continuous_scale=['#ffbb78', '#ff7f0e', '#d62728'],
    range_color=(4.0, 8.0),
    title="Amputations & Fatalities Only (National Estimates)"
)

fig_serious.update_traces(
    hovertemplate="<b>%{label}</b><br>National Estimate: %{value:,.0f}<br>Avg Severity: %{color:.2f}"
)
fig_serious.update_layout(height=750)

st.plotly_chart(fig_serious, use_container_width=True)
