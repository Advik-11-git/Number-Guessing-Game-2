import streamlit as st
import random

st.title("🎯 Number Guessing Game")

# --- Session State Setup ---
if "computer_pick" not in st.session_state:
    st.session_state.computer_pick = random.randint(1, 11)

if "player_names" not in st.session_state:
    st.session_state.player_names = []

if "scoreboard" not in st.session_state:
    st.session_state.scoreboard = {}

if "current_player" not in st.session_state:
    st.session_state.current_player = 0

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "game_started" not in st.session_state:
    st.session_state.game_started = False


# --- Step 1: Number of Players ---
if not st.session_state.game_started:
    st.subheader("Game Setup")

    num_players = st.number_input(
        "Enter the Number of Players",
        min_value=1,
        step=1
    )

    # Collect player names
    st.session_state.player_names = []
    for i in range(int(num_players)):
        name = st.text_input(f"Enter name for Player {i+1}", key=f"name_{i}")
        if name:
            st.session_state.player_names.append(name)

    if st.button("Start Game"):
        if len(st.session_state.player_names) == int(num_players):
            st.session_state.game_started = True
            st.rerun()
        else:
            st.warning("Please enter all player names!")


# --- Step 2: Game Play ---
else:
    st.subheader("Game In Progress")

    players = st.session_state.player_names
    cp = st.session_state.computer_pick
    current = st.session_state.current_player

    if current < len(players):
        player_name = players[current]
        st.markdown(f"### {player_name}'s Turn")

        guess = st.number_input(
            "Enter a number (1–11)",
            min_value=1,
            max_value=11,
            step=1,
            key=f"guess_{current}_{st.session_state.attempts}"
        )

        if st.button("Submit Guess"):
            st.session_state.attempts += 1

            if guess == cp:
                st.success("🎉 You Won!")
                st.session_state.scoreboard[player_name] = "Win"
                st.session_state.current_player += 1
                st.session_state.attempts = 0
                st.rerun()

            elif guess > cp:
                st.warning("📈 Your number is bigger than the computer's pick")

            else:
                st.warning("📉 Your number is smaller than the computer's pick")

            # Lose after 3 attempts
            if st.session_state.attempts >= 3:
                st.error("❌ You Lose!")
                st.session_state.scoreboard[player_name] = "Lose"
                st.session_state.current_player += 1
                st.session_state.attempts = 0
                st.rerun()

    else:
        # --- Step 3: Show Scoreboard ---
        st.subheader("🏆 Scoreboard")
        for name, result in st.session_state.scoreboard.items():
            st.write(f"**{name}**: {result}")

        if st.button("Play Again"):
            # Reset everything
            st.session_state.computer_pick = random.randint(1, 11)
            st.session_state.player_names = []
            st.session_state.scoreboard = {}
            st.session_state.current_player = 0
            st.session_state.attempts = 0
            st.session_state.game_started = False
            st.rerun()
