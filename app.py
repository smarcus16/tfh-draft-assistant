import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(
    page_title="TFH Live Draft Assistant",
    page_icon="🏈",
    layout="wide"
)

# Sidebar for Sleeper API Sync
st.sidebar.header("Live Draft Sync")
sleeper_draft_id = st.sidebar.text_input("Sleeper Draft ID", value="1397302773686468608")
debug_mode = st.sidebar.checkbox("Enable API Debug View", value=True)

# Function to fetch live picks from Sleeper API
@st.cache_data(ttl=5)
def fetch_sleeper_picks(draft_id):
    if not draft_id:
        return []
    url = f"https://api.sleeper.app/v1/draft/{draft_id}/picks"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Function to fetch active NFL players dictionary from Sleeper
@st.cache_data
def fetch_sleeper_nfl_players():
    url = "https://api.sleeper.app/v1/players/nfl"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Master Player Pool structured with TFH Tiers and Metrics
master_pool = [
    {"name": "Bijan Robinson", "pos": "RB", "tier": 1, "drb_score": 9.6, "archetype": "Elite Ceiling", "adp": 3},
    {"name": "Jahmyr Gibbs", "pos": "RB", "tier": 1, "drb_score": 9.4, "archetype": "Elite Ceiling", "adp": 4},
    {"name": "Christian McCaffrey", "pos": "RB", "tier": 1, "drb_score": 9.8, "archetype": "Elite Ceiling", "adp": 1},
    {"name": "CeeDee Lamb", "pos": "WR", "tier": 1, "drb_score": 0.0, "archetype": "Target Monster", "adp": 2},
    {"name": "Tyreek Hill", "pos": "WR", "tier": 1, "drb_score": 0.0, "archetype": "Target Monster", "adp": 5},
    {"name": "Puka Nacua", "pos": "WR", "tier": 1, "drb_score": 0.0, "archetype": "Target Monster", "adp": 7},
    {"name": "Ja'Marr Chase", "pos": "WR", "tier": 1, "drb_score": 0.0, "archetype": "Target Monster", "adp": 6},
    {"name": "Saquon Barkley", "pos": "RB", "tier": 2, "drb_score": 8.5, "archetype": "Safe Volume Floor", "adp": 12},
    {"name": "Jonathan Taylor", "pos": "RB", "tier": 2, "drb_score": 8.3, "archetype": "Safe Volume Floor", "adp": 15},
    {"name": "Amon-Ra St. Brown", "pos": "WR", "tier": 2, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 10},
    {"name": "Garrett Wilson", "pos": "WR", "tier": 2, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 14},
    {"name": "Drake London", "pos": "WR", "tier": 2, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 18},
    {"name": "De'Von Achane", "pos": "RB", "tier": 3, "drb_score": 7.8, "archetype": "Explosive Ceiling", "adp": 25},
    {"name": "Josh Jacobs", "pos": "RB", "tier": 3, "drb_score": 7.5, "archetype": "Safe Volume Floor", "adp": 28},
    {"name": "Nico Collins", "pos": "WR", "tier": 3, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 30},
    {"name": "Marvin Harrison Jr.", "pos": "WR", "tier": 3, "drb_score": 0.0, "archetype": "Rookie Upside", "adp": 22},
    {"name": "Rhamondre Stevenson", "pos": "RB", "tier": 4, "drb_score": 5.4, "archetype": "Bust Risk (Dead Zone)", "adp": 62},
    {"name": "D'Andre Swift", "pos": "RB", "tier": 4, "drb_score": 5.2, "archetype": "Bust Risk (Dead Zone)", "adp": 68},
    {"name": "Zamir White", "pos": "RB", "tier": 4, "drb_score": 4.9, "archetype": "Bust Risk (Dead Zone)", "adp": 75},
    {"name": "Christian Kirk", "pos": "WR", "tier": 3, "drb_score": 0.0, "archetype": "PPR Value Target", "adp": 70},
    {"name": "Rashee Rice", "pos": "WR", "tier": 3, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 55},
    {"name": "Chris Godwin", "pos": "WR", "tier": 3, "drb_score": 0.0, "archetype": "PPR Value Target", "adp": 64},
]

# Initialize Session State
if "manual_drafted" not in st.session_state:
    st.session_state.manual_drafted = []

if "current_round" not in st.session_state:
    st.session_state.current_round = 1

# App Header
st.title("🏈 TFH Draft Assistant + Live Sleeper Sync")
st.markdown("Powered by Dynamic Running Back (DRB) metrics, tier-based value matrices, and live Sleeper API integration.")

st.sidebar.markdown("---")
st.session_state.current_round = st.sidebar.slider("Current Draft Round", 1, 15, st.session_state.current_round)

# Fetch and Parse Sleeper API Picks (Strictly filtering for active rostered players)
sleeper_picked_names = []
raw_picks = []
if sleeper_draft_id:
    raw_picks = fetch_sleeper_picks(sleeper_draft_id)
    nfl_players = fetch_sleeper_nfl_players()
    
    for pick in raw_picks:
        p_id = pick.get("player_id")
        if p_id and p_id in nfl_players:
            p_info = nfl_players[p_id]
            # Ensure the player is actively signed to an NFL team roster
            player_team = p_info.get("team")
            if player_team is not None and player_team != "":
                full_name = f"{p_info.get('first_name', '')} {p_info.get('last_name', '')}".strip()
                sleeper_picked_names.append(full_name)

# Debug view output in sidebar
if debug_mode:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 API Debug Inspector")
    st.sidebar.text(f"Raw picks pulled: {len(raw_picks)}")
    st.sidebar.text(f"Active matched picks: {sleeper_picked_names}")

# Filter available player pool
unavailable_players = set(st.session_state.manual_drafted + sleeper_picked_names)
active_pool = [p for p in master_pool if p["name"] not in unavailable_players]

# Main Dashboard Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Round {st.session_state.current_round} Recommendations")
    
    if 5 <= st.session_state.current_round <= 10:
        st.warning("⚠️ **TFH Alert: Mid-Round RB Dead Zone Active.** Prioritize high-upside WR depth.")
    else:
        st.success("✅ **TFH Status:** Optimal draft window for elite ceilings.")

    if active_pool:
        df_pool = pd.DataFrame(active_pool)
        df_pool = df_pool.sort_values(by=["tier", "drb_score"], ascending=[True, False])
        
        st.dataframe(df_pool[["name", "pos", "tier", "archetype", "adp"]], use_container_width=True, hide_index=True)
        
        st.markdown("### Manual Backup Pick")
        available_names = [p["name"] for p in active_pool]
        selected_player_name = st.selectbox("Select player to manually mark as drafted:", available_names)
        
        if st.button("Mark Drafted Locally", type="primary"):
            st.session_state.manual_drafted.append(selected_player_name)
            st.rerun()
    else:
        st.info("No players remaining in the active pool.")

with col2:
    st.subheader("TFH Strategy Matrix")
    st.markdown("""
    * **Elite Ceiling (Tier 1):** Priority targets in rounds 1–2.
    * **Safe Volume Floor:** Reliable touch counts.
    * **Target Monster (WR):** High-target share week-winners.
    * **Bust Risk (Dead Zone):** RBs in rounds 5–10. **Avoid.**
    """)
    
    st.markdown("---")
    if st.button("Reset Local Draft Board"):
        st.session_state.manual_drafted = []
        st.rerun()
