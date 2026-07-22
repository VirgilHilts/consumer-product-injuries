import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NEISS Injury Explorer", layout="wide")
st.title("NEISS Injury Explorer")
st.markdown("**National Estimates** — Colored by Average Severity")

# Load data
@st.cache_data
def load_agg():
    return pd.read_csv('agg_all.csv')

agg = load_agg()

agg['national_estimate'] = agg['national_estimate'].round(0).astype(int)
agg['avg_Severity'] = agg['avg_Severity'].round(2)

# Load top narratives
@st.cache_data
def load_top_narr():
    return pd.read_pickle('top_3_narratives.pkl')

top_narr = load_top_narr()
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

fig_all.update_layout(height=700)
st.plotly_chart(fig_all, use_container_width=True)

# Expandable narratives for All Injuries
with st.expander("Show Top 3 Narratives for All Injuries", expanded=False):
    st.dataframe(
        agg[['broad_category', 'Prod', 'top_3_narratives', 'national_estimate']]
        .sort_values('national_estimate', ascending=False),
        use_container_width=True
    )

# ==================== SERIOUS INJURIES ====================
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

fig_serious.update_layout(height=700)
st.plotly_chart(fig_serious, use_container_width=True)

with st.expander("Show Top 3 Narratives for Serious Injuries", expanded=False):
    st.dataframe(
        serious_agg[['broad_category', 'Prod', 'top_3_narratives', 'national_estimate']]
        .sort_values('national_estimate', ascending=False),
        use_container_width=True
    )

    
