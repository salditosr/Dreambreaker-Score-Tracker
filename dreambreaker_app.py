import streamlit as st

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'setup'
if 'team1_score' not in st.session_state:
    st.session_state.team1_score = 0
if 'team2_score' not in st.session_state:
    st.session_state.team2_score = 0
if 'current_player_index' not in st.session_state:
    st.session_state.current_player_index = 0
if 'points_in_current_round' not in st.session_state:
    st.session_state.points_in_current_round = 0
if 'serving_team' not in st.session_state:
    st.session_state.serving_team = 1
if 'target_score' not in st.session_state:
    st.session_state.target_score = 21

def reset_game():
    """Reset all game state"""
    st.session_state.team1_score = 0
    st.session_state.team2_score = 0
    st.session_state.current_player_index = 0
    st.session_state.points_in_current_round = 0
    st.session_state.serving_team = 1
    st.session_state.page = 'setup'

def start_game():
    """Start the game and move to scoring page"""
    st.session_state.page = 'game'
    st.session_state.team1_score = 0
    st.session_state.team2_score = 0
    st.session_state.current_player_index = 0
    st.session_state.points_in_current_round = 0

def add_point(team):
    """Add a point to the specified team and check for player rotation"""
    if team == 1:
        st.session_state.team1_score += 1
    else:
        st.session_state.team2_score += 1
    
    # Team that scores gets the serve
    st.session_state.serving_team = team
    
    st.session_state.points_in_current_round += 1
    
    # Check if we have a winner
    if st.session_state.team1_score >= st.session_state.target_score:
        st.session_state.page = 'winner'
        st.session_state.winning_team = 1
        return
    elif st.session_state.team2_score >= st.session_state.target_score:
        st.session_state.page = 'winner'
        st.session_state.winning_team = 2
        return
    
    # Check if we need to rotate players (every 4 points)
    if st.session_state.points_in_current_round >= 4:
        st.session_state.current_player_index += 1
        st.session_state.points_in_current_round = 0
        
        # Reset to first player if we've cycled through all
        if st.session_state.current_player_index >= 4:
            st.session_state.current_player_index = 0

# Main app
st.set_page_config(page_title="MLP Dreambreaker Calculator", layout="wide")

if st.session_state.page == 'setup':
    # Setup Page
    st.title("🏓 MLP Dreambreaker Calculator")
    st.markdown("---")
    
    # Add JavaScript for Enter key navigation
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const inputs = document.querySelectorAll('input[type="text"], input[type="number"]');
        inputs.forEach((input, index) => {
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (index < inputs.length - 1) {
                        inputs[index + 1].focus();
                    }
                }
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Game Settings
    st.subheader("⚙️ Game Settings")
    settings_col1, settings_col2 = st.columns(2)
    with settings_col1:
        target_score = st.number_input("Score to Play To", min_value=1, max_value=100, value=21, step=1)
    with settings_col2:
        serving_first = st.radio("Who Serves First?", ["Select...", "Home", "Away"], horizontal=False)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Home Team")
        st.subheader("Players")
        team1_player1 = st.text_input("Player 1", key="t1p1", placeholder="Enter player name")
        team1_player2 = st.text_input("Player 2", key="t1p2", placeholder="Enter player name")
        team1_player3 = st.text_input("Player 3", key="t1p3", placeholder="Enter player name")
        team1_player4 = st.text_input("Player 4", key="t1p4", placeholder="Enter player name")
    
    with col2:
        st.header("Away Team")
        st.subheader("Players")
        team2_player1 = st.text_input("Player 1", key="t2p1", placeholder="Enter player name")
        team2_player2 = st.text_input("Player 2", key="t2p2", placeholder="Enter player name")
        team2_player3 = st.text_input("Player 3", key="t2p3", placeholder="Enter player name")
        team2_player4 = st.text_input("Player 4", key="t2p4", placeholder="Enter player name")
    
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("🚀 START", use_container_width=True, type="primary"):
            # Validate all fields are filled
            if not all([team1_player1, team1_player2, team1_player3, team1_player4,
                       team2_player1, team2_player2, team2_player3, team2_player4]):
                st.error("⚠️ Please fill in all player names before starting!")
            elif serving_first == "Select...":
                st.error("⚠️ Please select who serves first!")
            else:
                # Store team info in session state
                st.session_state.stored_team1_name = "Home"
                st.session_state.stored_team2_name = "Away"
                st.session_state.team1_players = [team1_player1, team1_player2, team1_player3, team1_player4]
                st.session_state.team2_players = [team2_player1, team2_player2, team2_player3, team2_player4]
                st.session_state.target_score = target_score
                st.session_state.serving_team = 1 if serving_first == "Home" else 2
                start_game()
                st.rerun()

elif st.session_state.page == 'game':
    # Game Page - Side-by-side layout with columns
    col_title, col_reset = st.columns([3, 1])
    with col_title:
        st.markdown("<h3 style='margin: 0; font-size: 1rem;'>🏓 MLP Dreambreaker</h3>", unsafe_allow_html=True)
    with col_reset:
        if st.button("🔄", use_container_width=True):
            reset_game()
            st.rerun()
    
    # Home and Away headers with scores - side by side
    score_col1, vs_col, score_col2 = st.columns([2, 1, 2])
    
    current_idx = st.session_state.current_player_index
    
    with score_col1:
        # Home team
        st.markdown(f"<div style='text-align: center;'><h2 style='margin: 0; font-size: 0.9rem;'>{st.session_state.stored_team1_name}</h2></div>", unsafe_allow_html=True)
        
        # Serving indicator for Home
        if st.session_state.serving_team == 1:
            side = "R" if st.session_state.team1_score % 2 == 0 else "L"
            st.markdown(f"<div style='text-align: center; color: #FF4B4B; font-size: 0.65em; margin: 3px 0;'>🔴 SERVE ({side})</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Score
        st.markdown(f"<h1 style='text-align: center; margin: 5px 0; font-size: 2rem;'>{st.session_state.team1_score}</h1>", unsafe_allow_html=True)
    
    with vs_col:
        st.markdown("<div style='text-align: center; margin-top: 25px;'><h2 style='font-size: 0.9rem;'>VS</h2></div>", unsafe_allow_html=True)
    
    with score_col2:
        # Away team
        st.markdown(f"<div style='text-align: center;'><h2 style='margin: 0; font-size: 0.9rem;'>{st.session_state.stored_team2_name}</h2></div>", unsafe_allow_html=True)
        
        # Serving indicator for Away
        if st.session_state.serving_team == 2:
            side = "R" if st.session_state.team2_score % 2 == 0 else "L"
            st.markdown(f"<div style='text-align: center; color: #FF4B4B; font-size: 0.65em; margin: 3px 0;'>🔴 SERVE ({side})</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Score
        st.markdown(f"<h1 style='text-align: center; margin: 5px 0; font-size: 2rem;'>{st.session_state.team2_score}</h1>", unsafe_allow_html=True)
    
    # Player names - side by side
    player_col1, player_col2 = st.columns(2)
    
    with player_col1:
        st.markdown(f"<div style='text-align: center; font-size: 1.2em; font-weight: bold; margin: 8px 0;'>{st.session_state.team1_players[current_idx]}</div>", unsafe_allow_html=True)
    
    with player_col2:
        st.markdown(f"<div style='text-align: center; font-size: 1.2em; font-weight: bold; margin: 8px 0;'>{st.session_state.team2_players[current_idx]}</div>", unsafe_allow_html=True)
    
    # Score buttons - narrower with better spacing
    btn_col_left, btn_col1, spacer, btn_col2, btn_col_right = st.columns([0.05, 0.425, 0.05, 0.425, 0.05])
    
    with btn_col1:
        if st.button(f"➕ {st.session_state.stored_team1_name}", 
                     use_container_width=True, 
                     type="primary",
                     key="team1_btn"):
            add_point(1)
            st.rerun()
    
    with btn_col2:
        if st.button(f"➕ {st.session_state.stored_team2_name}", 
                     use_container_width=True, 
                     type="primary",
                     key="team2_btn"):
            add_point(2)
            st.rerun()
    
    # Player rotation schedule - compact at bottom
    with st.expander("📋 Schedule"):
        for i in range(4):
            status = "🟢" if i == current_idx else "⚪"
            st.markdown(f"<small>{status} R{i+1}: {st.session_state.team1_players[i]} vs {st.session_state.team2_players[i]}</small>", unsafe_allow_html=True)

elif st.session_state.page == 'winner':
    # Winner Page
    st.balloons()
    
    winning_team_name = (st.session_state.stored_team1_name if st.session_state.winning_team == 1 
                         else st.session_state.stored_team2_name)
    winning_score = (st.session_state.team1_score if st.session_state.winning_team == 1 
                    else st.session_state.team2_score)
    losing_score = (st.session_state.team2_score if st.session_state.winning_team == 1 
                   else st.session_state.team1_score)
    
    st.markdown("<h1 style='text-align: center;'>🎉 CONGRATULATIONS! 🎉</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{winning_team_name} WINS!</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Final Score: {winning_score} - {losing_score}</h3>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Display all players from winning team
    st.markdown("### 🏆 Winning Team Players:")
    winning_players = (st.session_state.team1_players if st.session_state.winning_team == 1 
                      else st.session_state.team2_players)
    for player in winning_players:
        st.markdown(f"- **{player}**")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # New game button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Start New Game", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()


# Add custom CSS for better styling
st.markdown("""
<style>
    .stButton>button {
        height: 3.3em;
        font-size: 1.2em;
        font-weight: bold;
    }
    h2 {
        font-weight: bold;
    }
    
    /* Reduce default Streamlit spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Force columns to stay side-by-side on mobile */
    @media only screen and (max-width: 768px) {
        /* Prevent columns from stacking */
        [data-testid="column"] {
            width: 50% !important;
            flex: 1 1 50% !important;
            min-width: 0 !important;
            padding: 0.1rem !important;
        }
        
        /* Ensure row stays horizontal */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            gap: 0.2rem !important;
        }
        
        /* Reduce padding and margins */
        .block-container {
            padding-top: 0.3rem;
            padding-bottom: 0.3rem;
            padding-left: 0.3rem;
            padding-right: 0.3rem;
        }
        
        /* Compact headings - much smaller */
        h1 {
            font-size: 2rem !important;
            margin: 0.1rem 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
        }
        h2 {
            font-size: 0.95rem !important;
            margin: 0.1rem 0 !important;
            line-height: 1.1 !important;
        }
        h3 {
            font-size: 0.85rem !important;
            margin: 0.1rem 0 !important;
        }
        
        /* Make buttons more compact */
        .stButton>button {
            height: 3.1em !important;
            font-size: 0.85em !important;
            padding: 0.3em 0.3em !important;
            margin: 0 !important;
        }
        
        /* Remove excess spacing between elements */
        .element-container {
            margin-bottom: 0.1rem !important;
        }
        
        /* Smaller input fields */
        input {
            font-size: 14px !important;
            padding: 0.4rem !important;
        }
        
        /* Remove horizontal rules spacing */
        hr {
            margin: 0.2rem 0 !important;
        }
        
        /* Compact expander */
        .streamlit-expanderHeader {
            font-size: 0.75rem !important;
            padding: 0.2rem !important;
        }
        
        .streamlit-expanderContent {
            padding: 0.2rem !important;
            font-size: 0.7rem !important;
        }
        
        /* Much smaller player names on portrait */
        div[style*="font-size: 2em"] {
            font-size: 1.1em !important;
            margin: 8px 0 !important;
        }
        
        /* Smaller serve indicator */
        div[style*="font-size: 0.9em"] {
            font-size: 0.7em !important;
        }
        
        /* Compact the VS column */
        div[style*="margin-top: 60px"] {
            margin-top: 30px !important;
        }
    }
    
    /* Very small phones - even more compact */
    @media only screen and (max-width: 480px) {
        h1 {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 0.85rem !important;
        }
        
        .stButton>button {
            font-size: 0.75em !important;
            height: 2.75em !important;
            padding: 0.2em 0.2em !important;
        }
        
        div[style*="font-size: 2em"] {
            font-size: 1em !important;
        }
    }
</style>
""", unsafe_allow_html=True)
