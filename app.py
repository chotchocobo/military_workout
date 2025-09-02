import streamlit as st
import pandas as pd
import time

# Set page configuration for a better layout
st.set_page_config(layout="wide")

st.title("Military Workout Timer and Plan")

# Define workout plans as a dictionary
workout_plans = {
    "Push up": [
        {"exercise": "Push up", "duration": 120, "reps": "max"},
    ],
    "Sit up": [
        {"exercise": "Sit up", "duration": 120, "reps": "max"},
    ],
    "Running": [
        {"exercise": "Running", "duration": 720, "reps": "2 km"},
    ],
    "Full Body Workout": [
        {"exercise": "Jumping Jacks", "duration": 60, "reps": "N/A"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Push ups", "duration": 60, "reps": "max"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Sit ups", "duration": 60, "reps": "max"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Squats", "duration": 60, "reps": "max"},
    ]
}

# --- Session State Initialization ---
# Initialize session state variables if they don't exist to prevent errors on first run
if "running" not in st.session_state:
    st.session_state.running = False
if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = []
if "current_exercise_index" not in st.session_state:
    st.session_state.current_exercise_index = 0
if "timer" not in st.session_state:
    st.session_state.timer = 0

# --- Functions to control workout state ---
def start_workout(plan):
    """Starts the workout timer and sets up the session state."""
    st.session_state.running = True
    st.session_state.workout_plan = plan
    st.session_state.current_exercise_index = 0
    # Ensure the plan has at least one exercise before accessing index 0
    if plan:
        st.session_state.timer = plan[0]["duration"]

def stop_workout():
    """Stops the workout timer."""
    st.session_state.running = False

def reset_workout():
    """Resets the entire workout state."""
    st.session_state.running = False
    st.session_state.workout_plan = []
    st.session_state.current_exercise_index = 0
    st.session_state.timer = 0


# --- UI Layout ---
# Dropdown to select a workout plan
plan_selection = st.selectbox("Choose your workout plan:", list(workout_plans.keys()))

selected_plan = workout_plans[plan_selection]

# Display the details of the selected plan in a dataframe
st.write("### Workout Details")
df = pd.DataFrame(selected_plan)
st.dataframe(df, use_container_width=True)

# Create columns for control buttons
col1, col2, col3 = st.columns(3)

with col1:
    # Show "Start" button only if the workout is not running
    if not st.session_state.running:
        if st.button("Start", use_container_width=True, type="primary"):
            start_workout(selected_plan)
            # Rerun the script to start the timer display
            st.rerun()

with col2:
    # Show "Stop" button only if the workout is running
    if st.session_state.running:
        if st.button("Stop", use_container_width=True):
            stop_workout()
            # Rerun the script to hide the timer and update button states
            st.rerun()

with col3:
    # "Reset" button is always available
    if st.button("Reset", use_container_width=True):
        reset_workout()
        # Rerun to reflect the reset state in the UI
        st.rerun()


# --- Timer and Exercise Display Logic ---
# This block runs only when the 'running' state is True
if st.session_state.running:
    # Defensive check to prevent IndexError if the workout plan is somehow empty or finished
    if st.session_state.current_exercise_index >= len(st.session_state.workout_plan):
        stop_workout()
        st.warning("Workout finished or plan is empty.")
        st.rerun()
    else:
        current_exercise = st.session_state.workout_plan[st.session_state.current_exercise_index]
        exercise_name = current_exercise["exercise"]
        reps = current_exercise["reps"]

        st.markdown(f"## Current Exercise: **{exercise_name}**")
        st.markdown(f"### Reps: **{reps}**")

        # Timer display using a progress bar and a metric
        progress_bar = st.progress(0.0)
        timer_placeholder = st.empty()

        total_duration = current_exercise["duration"]
        remaining_time = st.session_state.timer
        
        # Calculate progress, avoiding division by zero
        progress = (total_duration - remaining_time) / total_duration if total_duration > 0 else 1.0
        
        # Ensure progress is between 0.0 and 1.0
        progress = max(0.0, min(1.0, progress))

        progress_bar.progress(progress)
        
        # Format time as MM:SS
        minutes, seconds = divmod(remaining_time, 60)
        timer_placeholder.metric("Time Remaining", f"{minutes:02d}:{seconds:02d}")

        # --- Core timer logic ---
        # Pause execution for 1 second. This makes the timer update every second.
        time.sleep(1)

        if st.session_state.timer > 0:
            st.session_state.timer -= 1
        else:
            # Timer for the current exercise is up, move to the next one
            st.session_state.current_exercise_index += 1
            # Check if the workout is completely finished
            if st.session_state.current_exercise_index >= len(st.session_state.workout_plan):
                stop_workout()
                st.balloons() # Fun celebration!
            else:
                # Set the timer for the next exercise in the plan
                next_exercise = st.session_state.workout_plan[st.session_state.current_exercise_index]
                st.session_state.timer = next_exercise["duration"]
        
        # Rerun the script to update the UI with the new timer value
        # We check 'running' again in case the workout was stopped in this iteration
        if st.session_state.running:
            st.rerun()
