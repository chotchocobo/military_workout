import streamlit as st
import pandas as pd
import time

# --- Page Configuration ---
st.set_page_config(layout="wide")

st.title("Military Workout Timer and Plan")

# --- New 7-Day Workout Data Structure ---
# This has been updated to follow the user's detailed 7-day plan.
# Each day includes a warm-up, two rounds of the main routine (40s work / 20s rest),
# a finisher, and a cool-down.
workout_plans = {
    "Select a Day": [],
    "Monday (Day 1) - Full Body Strength": [
        {"exercise": "Warm-up (Jumping Jacks)", "duration": 120, "reps": "N/A"},
        {"exercise": "Get Ready", "duration": 10, "reps": "Round 1 Starts"},
        {"exercise": "Push-ups", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Squats", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Plank", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Mountain Climbers", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Burpees", "duration": 40, "reps": "Round 1"},
        {"exercise": "Round Rest", "duration": 30, "reps": "Round 2 Starts"},
        {"exercise": "Push-ups", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Squats", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Plank", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Mountain Climbers", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Burpees", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 30, "reps": "Finisher next"},
        {"exercise": "Finisher: Push-ups", "duration": 60, "reps": "Max Reps"},
        {"exercise": "Cool-down (Stretch)", "duration": 120, "reps": "N/A"},
    ],
    "Tuesday (Day 2) - Core & Stability": [
        {"exercise": "Warm-up (High Knees)", "duration": 120, "reps": "N/A"},
        {"exercise": "Get Ready", "duration": 10, "reps": "Round 1 Starts"},
        {"exercise": "Sit-ups", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Side Plank (Right)", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Flutter Kicks", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Russian Twists", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Plank Shoulder Taps", "duration": 40, "reps": "Round 1"},
        {"exercise": "Round Rest", "duration": 30, "reps": "Round 2 Starts"},
        {"exercise": "Sit-ups", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Side Plank (Left)", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Flutter Kicks", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Russian Twists", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Plank Shoulder Taps", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 30, "reps": "Finisher next"},
        {"exercise": "Finisher: Mountain Climbers", "duration": 60, "reps": "Max Reps"},
        {"exercise": "Cool-down (Stretch)", "duration": 120, "reps": "N/A"},
    ],
    "Wednesday (Day 3) - Cardio & Endurance": [
        {"exercise": "Warm-up (Jumping Jacks)", "duration": 120, "reps": "N/A"},
        {"exercise": "Get Ready", "duration": 10, "reps": "Round 1 Starts"},
        {"exercise": "Jumping Jacks", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "High Knees", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Burpees", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Mountain Climbers", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Squat Jumps", "duration": 40, "reps": "Round 1"},
        {"exercise": "Round Rest", "duration": 30, "reps": "Round 2 Starts"},
        {"exercise": "Jumping Jacks", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "High Knees", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Burpees", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Mountain Climbers", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Squat Jumps", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 30, "reps": "Finisher next"},
        {"exercise": "Finisher: Sprint in Place", "duration": 60, "reps": "Max Effort"},
        {"exercise": "Cool-down (Stretch)", "duration": 120, "reps": "N/A"},
    ],
    "Thursday (Day 4) - Upper Body Power": [
        {"exercise": "Warm-up (Arm Circles)", "duration": 120, "reps": "N/A"},
        {"exercise": "Get Ready", "duration": 10, "reps": "Round 1 Starts"},
        {"exercise": "Push-ups", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Tricep Dips (on chair)", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Pike Push-ups", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Plank Up-Downs", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Burpees", "duration": 40, "reps": "Round 1"},
        {"exercise": "Round Rest", "duration": 30, "reps": "Round 2 Starts"},
        {"exercise": "Push-ups", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Tricep Dips (on chair)", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Pike Push-ups", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Plank Up-Downs", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Burpees", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 30, "reps": "Finisher next"},
        {"exercise": "Finisher: Push-ups", "duration": 60, "reps": "Max Reps"},
        {"exercise": "Cool-down (Stretch)", "duration": 120, "reps": "N/A"},
    ],
    "Friday (Day 5) - Lower Body Strength": [
        {"exercise": "Warm-up (Leg Swings)", "duration": 120, "reps": "N/A"},
        {"exercise": "Get Ready", "duration": 10, "reps": "Round 1 Starts"},
        {"exercise": "Squats", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Lunges", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Wall Sit", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Calf Raises", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Jump Squats", "duration": 40, "reps": "Round 1"},
        {"exercise": "Round Rest", "duration": 30, "reps": "Round 2 Starts"},
        {"exercise": "Squats", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Lunges", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Wall Sit", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Calf Raises", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Jump Squats", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 30, "reps": "Finisher next"},
        {"exercise": "Finisher: Lunges", "duration": 60, "reps": "Max Reps"},
        {"exercise": "Cool-down (Stretch)", "duration": 120, "reps": "N/A"},
    ],
    "Saturday (Day 6) - HIIT Combat Style": [
        {"exercise": "Warm-up (Torso Twists)", "duration": 120, "reps": "N/A"},
        {"exercise": "Get Ready", "duration": 10, "reps": "Round 1 Starts"},
        {"exercise": "Burpees", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Push-ups", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Squat Jumps", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Mountain Climbers", "duration": 40, "reps": "Round 1"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Plank Jacks", "duration": 40, "reps": "Round 1"},
        {"exercise": "Round Rest", "duration": 30, "reps": "Round 2 Starts"},
        {"exercise": "Burpees", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Push-ups", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Squat Jumps", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Mountain Climbers", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 20, "reps": "N/A"},
        {"exercise": "Plank Jacks", "duration": 40, "reps": "Round 2"},
        {"exercise": "Rest", "duration": 30, "reps": "Finisher next"},
        {"exercise": "Finisher: Burpees", "duration": 60, "reps": "Max Reps"},
        {"exercise": "Cool-down (Stretch)", "duration": 120, "reps": "N/A"},
    ],
    "Sunday (Day 7) - Recovery & Mobility": [
        {"exercise": "Cat-Cow Stretch", "duration": 60, "reps": "Focus on breathing"},
        {"exercise": "Rest", "duration": 15, "reps": "N/A"},
        {"exercise": "Hip Bridges", "duration": 60, "reps": "Squeeze glutes"},
        {"exercise": "Rest", "duration": 15, "reps": "N/A"},
        {"exercise": "Side Lunges", "duration": 60, "reps": "30s each side"},
        {"exercise": "Rest", "duration": 15, "reps": "N/A"},
        {"exercise": "Superman Hold", "duration": 60, "reps": "Engage back"},
        {"exercise": "Rest", "duration": 15, "reps": "N/A"},
        {"exercise": "Plank", "duration": 60, "reps": "Hold steady"},
        {"exercise": "Full-Body Stretch", "duration": 120, "reps": "Hold each stretch 30s"},
    ],
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
    df = pd.DataFrame(selected_plan)
    st.dataframe(df, use_container_width=True)


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


