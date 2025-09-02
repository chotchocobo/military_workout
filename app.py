import streamlit as st
import time

# ---------------- Workout Plan ----------------
WORKOUT_PLAN = {
    "Day 1 - Full Body": [
        ("Jumping Jacks", 30),
        ("Push-ups", 30),
        ("Bodyweight Squats", 30),
        ("Plank", 30),
        ("Burpees", 30),
    ],
    "Day 2 - Core & Cardio": [
        ("High Knees", 30),
        ("Mountain Climbers", 30),
        ("Bicycle Crunches", 30),
        ("Russian Twists", 30),
        ("Leg Raises", 30),
    ],
    "Day 3 - Strength": [
        ("Lunges", 30),
        ("Push-ups", 30),
        ("Glute Bridges", 30),
        ("Tricep Dips", 30),
        ("Wall Sit", 30),
    ],
    "Day 4 - Cardio Blast": [
        ("Jump Rope (no rope)", 30),
        ("Burpees", 30),
        ("High Knees", 30),
        ("Squat Jumps", 30),
        ("Plank Jacks", 30),
    ],
    "Day 5 - Mixed": [
        ("Push-ups", 30),
        ("Sit-ups", 30),
        ("Squats", 30),
        ("Burpees", 30),
        ("Mountain Climbers", 30),
    ],
    "Day 6 - Core Focus": [
        ("Plank", 30),
        ("Side Plank (Left)", 30),
        ("Side Plank (Right)", 30),
        ("Flutter Kicks", 30),
        ("Bicycle Crunches", 30),
    ],
    "Day 7 - Active Recovery": [
        ("Stretching", 60),
        ("Yoga Poses", 60),
        ("Breathing Exercise", 60),
    ],
}

# ---------------- State Init ----------------
if "running" not in st.session_state:
    st.session_state.running = False
if "paused" not in st.session_state:
    st.session_state.paused = False
if "remaining" not in st.session_state:
    st.session_state.remaining = 0
if "exercise_index" not in st.session_state:
    st.session_state.exercise_index = 0

# ---------------- UI ----------------
st.title("🏋 Military Style Workout Timer")

day = st.selectbox("Select Workout Day", list(WORKOUT_PLAN.keys()))
exercises = WORKOUT_PLAN[day]

current_exercise = exercises[st.session_state.exercise_index]
next_exercise = exercises[st.session_state.exercise_index + 1] if st.session_state.exercise_index + 1 < len(exercises) else ("Done!", 0)

# Display exercises
st.markdown(f"### Current: **{current_exercise[0]}** ({current_exercise[1]} sec)")
st.markdown(f"➡️ Next: **{next_exercise[0]}**")

# ---------------- Controls ----------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Start"):
        st.session_state.running = True
        st.session_state.paused = False
        st.session_state.remaining = current_exercise[1]
with col2:
    if st.button("Pause"):
        st.session_state.paused = True
with col3:
    if st.button("Resume"):
        st.session_state.paused = False
with col4:
    if st.button("Reset"):
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.remaining = current_exercise[1]
        st.session_state.exercise_index = 0

# ---------------- Timer ----------------
timer_placeholder = st.empty()
sound_placeholder = st.empty()

if st.session_state.running and not st.session_state.paused:
    while st.session_state.remaining > 0 and st.session_state.running:
        mins, secs = divmod(st.session_state.remaining, 60)
        timer_placeholder.markdown(
            f"<h1 style='text-align:center;font-size:120px;'>{mins:02d}:{secs:02d}</h1>",
            unsafe_allow_html=True,
        )
        time.sleep(1)
        st.session_state.remaining -= 1
        st.experimental_rerun()

    # When timer ends -> beep & move to next exercise
    if st.session_state.remaining == 0 and st.session_state.running:
        sound_placeholder.audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg")
        st.session_state.exercise_index += 1
        if st.session_state.exercise_index < len(exercises):
            st.session_state.remaining = exercises[st.session_state.exercise_index][1]
        else:
            st.session_state.running = False
            st.success("Workout Complete! 🎉")
