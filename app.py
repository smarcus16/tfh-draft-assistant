class TFHDraftAssistant:
    def __init__(self):
        # Database mimicking TFH Tier and Metric data structure
        self.player_pool = [
            {"name": " Jahmyr Gibbs", "pos": "RB", "tier": 1, "drb_score": 9.4, "archetype": "Elite Ceiling", "adp": 4},
            {"name": "Bijan Robinson", "pos": "RB", "tier": 1, "drb_score": 9.6, "archetype": "Elite Ceiling", "adp": 3},
            {"name": "Puka Nacua", "pos": "WR", "tier": 1, "drb_score": 0, "archetype": "Target Monster", "adp": 7},
            {"name": "Mid-Round RB Trap X", "pos": "RB", "tier": 4, "drb_score": 5.1, "archetype": "Bust Risk (Dead Zone)", "adp": 65},
            {"name": "High-Value WR Sleeper Y", "pos": "WR", "tier": 3, "drb_score": 0, "archetype": "High-Upside Conversion", "adp": 72},
        ]
        self.drafted_players = []

    def draft_player(self, name):
        for p in self.player_pool:
            if p["name"].lower() == name.lower():
                self.player_pool.remove(p)
                self.drafted_players.append(p)
                print(f"--> Drafted: {p['name']} ({p['pos']})")
                return
        print("Player not found in pool.")

    def get_recommendations(self, current_round):
        print(f"\n--- TFH RECOMMENDATIONS FOR ROUND {current_round} ---")
        
        # Apply Headliners logic: discourage mid-round RB traps in rounds 5-10
        filtered_pool = self.player_pool.copy()
        if 5 <= current_round <= 10:
            print("[TFH Alert]: Mid-round RB window detected. Penalizing low-ceiling RBs. Favoring WR conversion depth.")
            # Sort prioritizing elite WR value or high DRB score if looking at RB
        
        # Sort by tier and score/value
        sorted_recommendations = sorted(filtered_pool, key=lambda x: (x["tier"], -x["drb_score"]))
        
        for rec in sorted_recommendations[:5]:
            print(f"[{rec['pos']}] {rec['name']} | Tier: {rec['tier']} | Archetype: {rec['archetype']} | ADP: {rec['adp']}")

# Example Usage:
assistant = TFHDraftAssistant()
assistant.get_recommendations(current_round=2)