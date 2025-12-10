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
if 'score_history' not in st.session_state:
    st.session_state.score_history = []

def reset_game():
    """Reset all game state"""
    st.session_state.team1_score = 0
    st.session_state.team2_score = 0
    st.session_state.current_player_index = 0
    st.session_state.points_in_current_round = 0
    st.session_state.serving_team = 1
    st.session_state.page = 'setup'
    st.session_state.score_history = []

def start_game():
    """Start the game and move to scoring page"""
    st.session_state.page = 'game'
    st.session_state.team1_score = 0
    st.session_state.team2_score = 0
    st.session_state.current_player_index = 0
    st.session_state.points_in_current_round = 0
    st.session_state.score_history = []

def undo_last_point():
    """Undo the last point scored"""
    # Always ensure we stay on game page
    st.session_state.page = 'game'
    
    if len(st.session_state.score_history) > 0:
        last_state = st.session_state.score_history.pop()
        st.session_state.team1_score = last_state['team1_score']
        st.session_state.team2_score = last_state['team2_score']
        st.session_state.current_player_index = last_state['current_player_index']
        st.session_state.points_in_current_round = last_state['points_in_current_round']
        st.session_state.serving_team = last_state['serving_team']

def add_point(team):
    """Add a point to the specified team and check for player rotation"""
    # Save current state to history before making changes
    st.session_state.score_history.append({
        'team1_score': st.session_state.team1_score,
        'team2_score': st.session_state.team2_score,
        'current_player_index': st.session_state.current_player_index,
        'points_in_current_round': st.session_state.points_in_current_round,
        'serving_team': st.session_state.serving_team
    })
    
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
    # Add padding at top to avoid banner
    st.write("")
    st.write("")
    
    # Setup Page
    st.title("🏓 MLP Dreambreaker Calculator")
    st.divider()
    
    # Game Settings
    st.subheader("⚙️ Game Settings")
    settings_col1, settings_col2 = st.columns(2)
    with settings_col1:
        target_score = st.number_input("Score to Play To", min_value=1, max_value=100, value=25, step=1)
    with settings_col2:
        serving_first = st.selectbox("Who Serves First?", ["Select...", "Home", "Away"])
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Home Team")
        team1_player1 = st.text_input("Player 1", key="t1p1")
        team1_player2 = st.text_input("Player 2", key="t1p2")
        team1_player3 = st.text_input("Player 3", key="t1p3")
        team1_player4 = st.text_input("Player 4", key="t1p4")
    
    with col2:
        st.subheader("Away Team")
        team2_player1 = st.text_input("Player 1", key="t2p1")
        team2_player2 = st.text_input("Player 2", key="t2p2")
        team2_player3 = st.text_input("Player 3", key="t2p3")
        team2_player4 = st.text_input("Player 4", key="t2p4")
    
    st.divider()
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
    # Safety check - if required data doesn't exist, go back to setup
    if ('stored_team1_name' not in st.session_state or 
        'stored_team2_name' not in st.session_state or
        'team1_players' not in st.session_state or
        'team2_players' not in st.session_state):
        st.session_state.page = 'setup'
        st.rerun()
    
    # Add padding at top to avoid banner
    st.write("")
    st.write("")
    
    # Game Page
    st.subheader("🏓 MLP Dreambreaker")
    
    # Home and Away scores
    score_col1, vs_col, score_col2 = st.columns([3, 0.5, 3])
    
    current_idx = st.session_state.current_player_index
    
    # Player change indicator color
    player_bg_color = ["#1E3A8A", "#15803D", "#9333EA", "#DC2626"][current_idx]
    
    with score_col1:
        st.subheader(st.session_state.stored_team1_name)
        
        if st.session_state.serving_team == 1:
            side = "R" if st.session_state.team1_score % 2 == 0 else "L"
            st.write(f"🔴 SERVE ({side})")
        
        st.title(f"{st.session_state.team1_score}")
    
    with vs_col:
        st.subheader("VS")
    
    with score_col2:
        st.subheader(st.session_state.stored_team2_name)
        
        if st.session_state.serving_team == 2:
            side = "R" if st.session_state.team2_score % 2 == 0 else "L"
            st.write(f"🔴 SERVE ({side})")
        
        st.title(f"{st.session_state.team2_score}")
    
    # Current players
    player_col1, player_col2 = st.columns(2)
    
    with player_col1:
        st.info(f"**{st.session_state.team1_players[current_idx]}**")
    
    with player_col2:
        st.info(f"**{st.session_state.team2_players[current_idx]}**")
    
    # Score buttons
    btn_col1, btn_col2 = st.columns(2)
    
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
    
    # Player rotation schedule
    with st.expander("📋 Schedule"):
        for i in range(4):
            status = "🟢" if i == current_idx else "⚪"
            round_color = ["🔵", "🟢", "🟣", "🔴"][i]
            st.write(f"{status} {round_color} R{i+1}: {st.session_state.team1_players[i]} vs {st.session_state.team2_players[i]}")
    
    # Bottom buttons - Undo and Reset
    st.divider()
    col_undo, col_reset = st.columns(2)
    with col_undo:
        if st.button("↩️ Undo Last Point", use_container_width=True, disabled=len(st.session_state.score_history) == 0, key="undo_btn"):
            undo_last_point()
            st.rerun()
    with col_reset:
        if st.button("🔄 Reset Game", use_container_width=True, key="reset_btn"):
            reset_game()
            st.rerun()

elif st.session_state.page == 'winner':
    # Add padding at top to avoid banner
    st.write("")
    st.write("")
    
    # Winner Page
    st.balloons()
    
    winning_team_name = (st.session_state.stored_team1_name if st.session_state.winning_team == 1 
                         else st.session_state.stored_team2_name)
    winning_score = (st.session_state.team1_score if st.session_state.winning_team == 1 
                    else st.session_state.team2_score)
    losing_score = (st.session_state.team2_score if st.session_state.winning_team == 1 
                   else st.session_state.team1_score)
    
    st.title("🎉 CONGRATULATIONS! 🎉")
    st.header(f"{winning_team_name} WINS!")
    st.subheader(f"Final Score: {winning_score} - {losing_score}")
    
    # Display all players from winning team
    st.write("### 🏆 Winning Team Players:")
    winning_players = (st.session_state.team1_players if st.session_state.winning_team == 1 
                      else st.session_state.team2_players)
    for player in winning_players:
        st.write(f"- **{player}**")
    
    # New game and undo buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("↩️ Undo Last Point", use_container_width=True, disabled=len(st.session_state.score_history) == 0):
            undo_last_point()
            st.rerun()
    with col2:
        if st.button("🔄 Start New Game", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()

