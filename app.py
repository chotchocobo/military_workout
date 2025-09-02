import streamlit as st
# import pandas as pd # Temporarily removed for debugging
import time

# --- Page Configuration ---
st.set_page_config(layout="wide")

st.title("Military Workout Timer and Plan")

# --- Workout Data Structure ---
# Organized by day for the new dropdown feature
workout_plans = {
    "Select a Day": [],
    "Monday - Full Body Strength": [
        {"exercise": "Warm-up (Jumping Jacks)", "duration": 120, "reps": "N/A"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Push ups", "duration": 60, "reps": "3 sets, max reps"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Bodyweight Squats", "duration": 60, "reps": "3 sets, max reps"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Plank", "duration": 60, "reps": "3 sets"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Sit ups", "duration": 60, "reps": "3 sets, max reps"},
        {"exercise": "Cool-down (Stretch)", "duration": 120, "reps": "N/A"},
    ],
    "Wednesday - Cardio & Core": [
        {"exercise": "Warm-up (High Knees)", "duration": 120, "reps": "N/A"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Running", "duration": 900, "reps": "2.5 km"},
        {"exercise": "Rest", "duration": 60, "reps": "N/A"},
        {"exercise": "Crunches", "duration": 60, "reps": "3 sets, max reps"},
        {"exercise": "Rest", "duration": 30, "reps": "N/A"},
        {"exercise": "Leg Raises", "duration": 60, "reps": "3 sets, max reps"},
        {"exercise": "Cool-down (Stretch)", "duration": 120, "reps": "N/A"},
    ],
    "Friday - Endurance Challenge": [
        {"exercise": "Push up", "duration": 120, "reps": "Max reps in 2 mins"},
        {"exercise": "Rest", "duration": 60, "reps": "N/A"},
        {"exercise": "Sit up", "duration": 120, "reps": "Max reps in 2 mins"},
        {"exercise": "Rest", "duration": 60, "reps": "N/A"},
        {"exercise": "Running", "duration": 720, "reps": "2 km timed run"},
    ]
}

# --- Session State Initialization ---
if "is_started" not in st.session_state:
    st.session_state.is_started = False
if "is_paused" not in st.session_state:
    st.session_state.is_paused = False
if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = []
if "current_exercise_index" not in st.session_state:
    st.session_state.current_exercise_index = 0
if "timer" not in st.session_state:
    st.session_state.timer = 0
if "selected_day" not in st.session_state:
    st.session_state.selected_day = "Select a Day"

# --- Control Functions ---
def start_workout(plan):
    """Initializes the workout state."""
    if plan:
        st.session_state.is_started = True
        st.session_state.is_paused = False
        st.session_state.workout_plan = plan
        st.session_state.current_exercise_index = 0
        st.session_state.timer = plan[0]["duration"]

def pause_workout():
    """Pauses the timer."""
    st.session_state.is_paused = True

def resume_workout():
    """Resumes the timer."""
    st.session_state.is_paused = False

def reset_workout():
    """Resets the entire workout state."""
    st.session_state.is_started = False
    st.session_state.is_paused = False
    st.session_state.workout_plan = []
    st.session_state.current_exercise_index = 0
    st.session_state.timer = 0
    # We keep selected_day so the user doesn't have to choose it again

# --- UI Layout ---

# Top section for workout selection
st.selectbox(
    "Choose your workout plan for the day:",
    list(workout_plans.keys()),
    key="selected_day",
    on_change=reset_workout # Reset if user picks a new plan
)

selected_plan = workout_plans[st.session_state.selected_day]

# Display workout details only if a plan is selected
if st.session_state.selected_day != "Select a Day":
    st.write("### Workout Details")
    # --- TEMPORARY DISPLAY - REPLACED PANDAS DATAFRAME ---
    with st.container(border=True):
        for item in selected_plan:
            st.text(f"- {item['exercise']} ({item['duration']}s) | Reps: {item['reps']}")
    # --------------------------------------------------------


# --- Main Timer and Control Display ---
if not st.session_state.is_started:
    # Show start button if workout hasn't started and a plan is chosen
    if st.session_state.selected_day != "Select a Day":
        if st.button("Start Workout", use_container_width=True, type="primary"):
            start_workout(selected_plan)
            st.rerun()
else:
    # --- Timer Countdown and Display Logic ---
    current_exercise = st.session_state.workout_plan[st.session_state.current_exercise_index]
    remaining_time = st.session_state.timer

    # Format time as MM:SS for display
    minutes, seconds = divmod(remaining_time, 60)

    # LARGE TIMER in the middle of the page
    st.markdown(f"""
    <div style="font-size: 160px; text-align: center; font-weight: bold; color: #4CAF50;">
        {minutes:02d}:{seconds:02d}
    </div>
    """, unsafe_allow_html=True)

    # --- Current and Next Workout Display ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Current Workout")
        st.info(f"**Exercise:** {current_exercise['exercise']}\n\n**Reps:** {current_exercise['reps']}")

    with col2:
        st.markdown("### Next Workout")
        next_index = st.session_state.current_exercise_index + 1
        if next_index < len(st.session_state.workout_plan):
            next_exercise = st.session_state.workout_plan[next_index]
            st.warning(f"**Exercise:** {next_exercise['exercise']}\n\n**Reps:** {next_exercise['reps']}")
        else:
            st.success("Last exercise! You're almost there!")


    # --- Control Buttons (Pause/Resume/Reset) ---
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if not st.session_state.is_paused:
            if st.button("Pause", use_container_width=True):
                pause_workout()
                st.rerun()
        else:
            if st.button("Resume", use_container_width=True, type="primary"):
                resume_workout()
                st.rerun()
    with btn_col2:
        if st.button("Reset", use_container_width=True):
            reset_workout()
            st.rerun()

    # --- Core Timer Logic ---
    if not st.session_state.is_paused:
        time.sleep(1) # Pause execution for 1 second

        if st.session_state.timer > 0:
            st.session_state.timer -= 1
        else:
            # Timer is up, move to the next exercise
            st.session_state.current_exercise_index += 1
            if st.session_state.current_exercise_index >= len(st.session_state.workout_plan):
                st.balloons()
                st.success("Workout Complete! Great job!")
                reset_workout() # Reset state but keep message
            else:
                # Set the timer for the next exercise
                next_ex = st.session_state.workout_plan[st.session_state.current_exercise_index]
                st.session_state.timer = next_ex["duration"]

        st.rerun()

