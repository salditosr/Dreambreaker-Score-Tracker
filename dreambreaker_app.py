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
    st.markdown("<h1 style='font-size: 1.5rem; margin: 0.3rem 0; line-height: 1.2;'>🏓 MLP Dreambreaker Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 0.3rem 0;'>", unsafe_allow_html=True)
    
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
    st.markdown("<h3 style='font-size: 1rem; margin: 0.3rem 0;'>⚙️ Game Settings</h3>", unsafe_allow_html=True)
    settings_col1, settings_col2 = st.columns(2)
    with settings_col1:
        # Make score input tiny - 20% width
        _, score_input, _ = st.columns([0.6, 0.2, 0.2])
        with score_input:
            target_score = st.number_input("", min_value=1, max_value=100, value=25, step=1)
        st.markdown("<p style='text-align: center; font-size: 0.7em; margin: -15px 0 5px 0; line-height: 1;'>Score to Play To</p>", unsafe_allow_html=True)
    with settings_col2:
        serving_first = st.selectbox("Who Serves First?", ["Select...", "Home", "Away"])
    
    st.markdown("<hr style='margin: 0.3rem 0;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h2 style='font-size: 1.3rem; margin: 0.3rem 0;'>Home Team</h2>", unsafe_allow_html=True)
        # NO subheader, just inputs
        _, input_col, _ = st.columns([0.25, 0.5, 0.25])
        with input_col:
            team1_player1 = st.text_input("", key="t1p1", placeholder="Player 1")
            team1_player2 = st.text_input("", key="t1p2", placeholder="Player 2")
            team1_player3 = st.text_input("", key="t1p3", placeholder="Player 3")
            team1_player4 = st.text_input("", key="t1p4", placeholder="Player 4")
    
    with col2:
        st.markdown("<h2 style='font-size: 1.3rem; margin: 0.3rem 0;'>Away Team</h2>", unsafe_allow_html=True)
        # NO subheader, just inputs
        _, input_col, _ = st.columns([0.25, 0.5, 0.25])
        with input_col:
            team2_player1 = st.text_input("", key="t2p1", placeholder="Player 1")
            team2_player2 = st.text_input("", key="t2p2", placeholder="Player 2")
            team2_player3 = st.text_input("", key="t2p3", placeholder="Player 3")
            team2_player4 = st.text_input("", key="t2p4", placeholder="Player 4")
    
    st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
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
    # Game Page - Ultra condensed layout
    col_title, col_reset = st.columns([3, 1])
    with col_title:
        st.markdown("<h3 style='margin: 0; font-size: 1rem; line-height: 1;'>🏓 MLP Dreambreaker</h3>", unsafe_allow_html=True)
    with col_reset:
        if st.button("🔄", use_container_width=True):
            reset_game()
            st.rerun()
    
    # Home and Away headers with scores - ultra condensed
    score_col1, vs_col, score_col2 = st.columns([3, 0.5, 3])
    
    current_idx = st.session_state.current_player_index
    
    # Player change indicator color
    player_bg_color = ["#1E3A8A", "#15803D", "#9333EA", "#DC2626"][current_idx]
    
    with score_col1:
        st.markdown(f"<div style='text-align: center; line-height: 1;'><h2 style='margin: 0; font-size: 1.8rem;'>{st.session_state.stored_team1_name}</h2></div>", unsafe_allow_html=True)
        
        if st.session_state.serving_team == 1:
            side = "R" if st.session_state.team1_score % 2 == 0 else "L"
            st.markdown(f"<div style='text-align: center; color: #FF4B4B; font-size: 1.3em; margin: 0; line-height: 1;'>🔴 SERVE ({side})</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='text-align: center; margin: 0; font-size: 4rem; line-height: 1;'>{st.session_state.team1_score}</h1>", unsafe_allow_html=True)
    
    with vs_col:
        st.markdown("<div style='text-align: center; margin-top: 25px;'><h2 style='font-size: 1.8rem; line-height: 1;'>VS</h2></div>", unsafe_allow_html=True)
    
    with score_col2:
        st.markdown(f"<div style='text-align: center; line-height: 1;'><h2 style='margin: 0; font-size: 1.8rem;'>{st.session_state.stored_team2_name}</h2></div>", unsafe_allow_html=True)
        
        if st.session_state.serving_team == 2:
            side = "R" if st.session_state.team2_score % 2 == 0 else "L"
            st.markdown(f"<div style='text-align: center; color: #FF4B4B; font-size: 1.3em; margin: 0; line-height: 1;'>🔴 SERVE ({side})</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='text-align: center; margin: 0; font-size: 4rem; line-height: 1;'>{st.session_state.team2_score}</h1>", unsafe_allow_html=True)
    
    # Player names - minimal spacing
    player_col1, player_col2 = st.columns(2)
    
    with player_col1:
        st.markdown(f"<div style='text-align: center; font-size: 2.4em; font-weight: bold; margin: 2px 0; padding: 8px; background-color: {player_bg_color}; border-radius: 10px; color: white; line-height: 1.1;'>{st.session_state.team1_players[current_idx]}</div>", unsafe_allow_html=True)
    
    with player_col2:
        st.markdown(f"<div style='text-align: center; font-size: 2.4em; font-weight: bold; margin: 2px 0; padding: 8px; background-color: {player_bg_color}; border-radius: 10px; color: white; line-height: 1.1;'>{st.session_state.team2_players[current_idx]}</div>", unsafe_allow_html=True)
    
    # Score buttons - ABSOLUTELY NO GAPS
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
            st.markdown(f"<small>{status} {round_color} R{i+1}: {st.session_state.team1_players[i]} vs {st.session_state.team2_players[i]}</small>", unsafe_allow_html=True)

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
    
    /* Larger input text on all screens */
    input {
        font-size: 32px !important;
        padding: 1rem !important;
    }
    
    input[type="number"] {
        font-size: 32px !important;
    }
    
    /* Make labels and text smaller on mobile */
    @media only screen and (max-width: 768px) {
        /* Reduce all text/label spacing on setup page */
        label {
            margin-bottom: 0.2rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Compact radio buttons */
        .stRadio {
            margin-top: 0 !important;
            margin-bottom: 0.3rem !important;
        }
        
        .stRadio > div {
            gap: 0.2rem !important;
        }
        
        /* Compact number input */
        .stNumberInput {
            margin-bottom: 0.3rem !important;
        }
        
        /* Reduce header spacing */
        h1, h2, h3 {
            margin-top: 0.3rem !important;
            margin-bottom: 0.3rem !important;
        }
        
        /* Reduce subheader spacing */
        .stMarkdown h2, .stMarkdown h3 {
            margin-top: 0.2rem !important;
            margin-bottom: 0.2rem !important;
        }
    }
    
    /* Reduce default Streamlit spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Force columns to stay side-by-side on mobile */
    @media only screen and (max-width: 768px) {
        /* CRITICAL: Force buttons to have NO gaps */
        [data-testid="column"] {
            width: 50% !important;
            flex: 1 1 50% !important;
            min-width: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* NO gaps between columns */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            gap: 0 !important;
        }
        
        /* Force buttons to take full width with no margins */
        .stButton {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
        }
        
        .stButton>button {
            margin: 0 !important;
            border-radius: 0.5rem !important;
        }
        
        /* Remove ALL padding from container */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Main content area - minimal padding */
        .main .block-container {
            padding-top: 0.1rem !important;
            padding-bottom: 0.1rem !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Reduce ALL element spacing on setup page */
        .element-container {
            margin-bottom: 0 !important;
            margin-top: 0 !important;
        }
        
        /* Compact form elements */
        .stTextInput, .stNumberInput {
            margin-bottom: 0.3rem !important;
            margin-top: 0 !important;
        }
        
        /* Reduce radio button spacing */
        .stRadio {
            margin: 0.2rem 0 !important;
        }
        
        .stRadio label {
            margin: 0.1rem 0 !important;
            padding: 0.2rem 0 !important;
        }
        
        /* Make dividers thinner */
        hr {
            margin: 0.3rem 0 !important;
            height: 1px !important;
        }
        
        /* Adjust headings for mobile - make smaller */
        h1 {
            font-size: 2.5rem !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }
        h2 {
            font-size: 1.2rem !important;
            margin: 0.2rem 0 !important;
            line-height: 1.1 !important;
            padding: 0 !important;
        }
        h3 {
            font-size: 0.8rem !important;
            margin: 0.2rem 0 !important;
            padding: 0 !important;
        }
        
        /* Make subheaders tiny */
        .stMarkdown h2 {
            font-size: 1rem !important;
            margin: 0.1rem 0 !important;
        }
        
        .stMarkdown h3 {
            font-size: 0.85rem !important;
            margin: 0.1rem 0 !important;
        }
        
        /* Mobile buttons */
        .stButton>button {
            height: 3.1em !important;
            font-size: 0.9em !important;
            padding: 0.3em 0.2em !important;
        }
        
        /* Remove spacing */
        .element-container {
            margin-bottom: 0 !important;
        }
        
        /* Keep larger input fields */
        input {
            font-size: 28px !important;
            padding: 0.8rem !important;
        }
        
        input[type="number"] {
            font-size: 28px !important;
        }
        
        /* No spacing on dividers */
        hr {
            margin: 0.1rem 0 !important;
        }
        
        /* Compact expander */
        .streamlit-expanderHeader {
            font-size: 0.7rem !important;
            padding: 0.15rem !important;
        }
        
        .streamlit-expanderContent {
            padding: 0.15rem !important;
            font-size: 0.65rem !important;
        }
        
        /* Smaller player names on mobile */
        div[style*="font-size: 2.4em"] {
            font-size: 1.3em !important;
            padding: 5px !important;
            margin: 1px 0 !important;
        }
        
        /* Tiny serve indicator */
        div[style*="font-size: 1.3em"] {
            font-size: 0.75em !important;
        }
        
        /* Smaller scores */
        h1[style*="font-size: 4rem"] {
            font-size: 2.2rem !important;
        }
        
        /* Smaller team names */
        h2[style*="font-size: 1.8rem"] {
            font-size: 1.1rem !important;
        }
        
        /* Reduce all spacing divs */
        div[style*="height: 18px"] {
            height: 12px !important;
        }
        
        div[style*="height: 25px"] {
            height: 12px !important;
        }
        
        /* Force VS column to be minimal */
        div[style*="margin-top: 25px"] {
            margin-top: 18px !important;
        }
    }
    
    /* Very small phones */
    @media only screen and (max-width: 480px) {
        h1[style*="font-size: 4rem"] {
            font-size: 1.8rem !important;
        }
        
        h2[style*="font-size: 1.8rem"] {
            font-size: 0.95rem !important;
        }
        
        .stButton>button {
            font-size: 0.75em !important;
            height: 2.75em !important;
            padding: 0.2em 0.1em !important;
        }
        
        div[style*="font-size: 2.4em"] {
            font-size: 1.1em !important;
            padding: 4px !important;
            margin: 1px 0 !important;
        }
        
        input {
            font-size: 24px !important;
        }
    }
</style>
""", unsafe_allow_html=True)
