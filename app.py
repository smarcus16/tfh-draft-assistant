import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="TFH Draft Assistant",
    page_icon="🏈",
    layout="wide"
)

# Initialize Session State for Draft Data and Roster
if "player_pool" not in st.session_state:
    st.session_state.player_pool = [
        {"name": "Bijan Robinson", "pos": "RB", "tier": 1, "drb_score": 9.6, "archetype": "Elite Ceiling", "adp": 3},
        {"name": "Jahmyr Gibbs", "pos": "RB", "tier": 1, "drb_score": 9.4, "archetype": "Elite Ceiling", "adp": 4},
        {"name": "Puka Nacua", "pos": "WR", "tier": 1, "drb_score": 0.0, "archetype": "Target Monster", "adp": 7},
        {"name": "CeeDee Lamb", "pos": "WR", "tier": 1, "drb_score": 0.0, "archetype": "Target Monster", "adp": 5},
        {"name": "Mid-Round RB Trap X", "pos": "RB", "tier": 4, "drb_score": 5.1, "archetype": "Bust Risk (Dead Zone)", "adp": 65},
        {"name": "High-Value WR Sleeper Y", "pos": "WR", "tier": 3, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 72},
        {"name": "Anchor RB Z", "pos": "RB", "tier": 2, "drb_score": 8.2, "archetype": "Safe Volume Floor", "adp": 24},
        {"name": "Breakout WR W", "pos": "WR", "tier": 2, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 35},
    ]

if "my_roster" not in st.session_state:
    st.session_state.my_roster = []

if "current_round" not in st.session_state:
    st.session_state.current_round = 1

# App Header
st.title("🏈 The Fantasy Headliners Draft Assistant")
st.markdown("Powered by Dynamic Running Back (DRB) metrics, tier-based value matrices, and mid-round WR conversion filters.")

# Sidebar Controls
st.sidebar.header("Draft Control Center")
st.session_state.current_round = st.sidebar.slider("Current Draft Round", 1, 15, st.session_state.current_round)

scoring_format = st.sidebar.selectbox("Scoring Format", ["Half-PPR", "Full PPR", "Standard"])
league_type = st.sidebar.selectbox("League Type", ["Redraft", "Dynasty / Keeper"])

st.sidebar.markdown("---")
st.sidebar.subheader("My Roster")
if st.session_state.my_roster:
    for idx, player in enumerate(st.session_state.my_roster):
        st.sidebar.text(f"{idx+1}. {player['name']} ({player['pos']})")
else:
    st.sidebar.info("No players drafted yet.")

# Main Dashboard Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Round {st.session_state.current_round} Recommendations")
    
    # TFH Mid-Round Logic Alert
    if 5 <= st.session_state.current_round <= 10:
        st.warning(
            "⚠️ **TFH Alert: Mid-Round RB Dead Zone Active.** "
            "Mid-round running backs carry high bust rates and low top-12 conversion ceilings. "
            "Prioritize high-upside wide receiver depth or elite anchor running backs."
        )
    else:
        st.success("✅ **TFH Status:** Optimal draft window for elite ceilings or high-value foundation pieces.")

    # Filter available players pool dataframe
    if st.session_state.player_pool:
        df_pool = pd.DataFrame(st.session_state.player_pool)
        df_pool = df_pool.sort_values(by=["tier", "drb_score"], ascending=[True, False])
        
        st.dataframe(df_pool[["name", "pos", "tier", "archetype", "adp"]], use_container_width=True, hide_index=True)
        
        st.markdown("### Make a Pick")
        available_names = [p["name"] for p in st.session_state.player_pool]
        selected_player_name = st.selectbox("Select player available on board:", available_names)
        
        if st.button("Draft Player to My Roster", type="primary"):
            for p in st.session_state.player_pool:
                if p["name"] == selected_player_name:
                    st.session_state.player_pool.remove(p)
                    st.session_state.my_roster.append(p)
                    st.success(f"Successfully drafted {p['name']} ({p['pos']})!")
                    st.rerun()
    else:
        st.info("The player pool is currently empty.")

with col2:
    st.subheader("TFH Strategy Matrix")
    st.markdown("""
    * **Elite Ceiling (Tier 1):** Priority targets in rounds 1–2. Unquestioned volume and explosive metrics.
    * **Safe Volume Floor:** Reliable touch counts keeping baseline points secure.
    * **Target Monster (WR):** High-target share receivers driving week-winning upside.
    * **Bust Risk (Dead Zone):** RBs drafted in rounds 5–10 with capped ceilings. **Avoid.**
    """)
    
    st.markdown("---")
    if st.button("Reset Draft Pool"):
        st.session_state.player_pool = [
            {"name": "Bijan Robinson", "pos": "RB", "tier": 1, "drb_score": 9.6, "archetype": "Elite Ceiling", "adp": 3},
            {"name": "Jahmyr Gibbs", "pos": "RB", "tier": 1, "drb_score": 9.4, "archetype": "Elite Ceiling", "adp": 4},
            {"name": "Puka Nacua", "pos": "WR", "tier": 1, "drb_score": 0.0, "archetype": "Target Monster", "adp": 7},
            {"name": "CeeDee Lamb", "pos": "WR", "tier": 1, "drb_score": 0.0, "archetype": "Target Monster", "adp": 5},
            {"name": "Mid-Round RB Trap X", "pos": "RB", "tier": 4, "drb_score": 5.1, "archetype": "Bust Risk (Dead Zone)", "adp": 65},
            {"name": "High-Value WR Sleeper Y", "pos": "WR", "tier": 3, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 72},
            {"name": "Anchor RB Z", "pos": "RB", "tier": 2, "drb_score": 8.2, "archetype": "Safe Volume Floor", "adp": 24},
            {"name": "Breakout WR W", "pos": "WR", "tier": 2, "drb_score": 0.0, "archetype": "High-Upside Conversion", "adp": 35},
        ]
        st.session_state.my_roster = []
        st.session_state.current_round = 1
        st.rerun()
