import time
import streamlit as st
from datetime import timedelta

st.set_page_config(page_title="Military Workout Timer", page_icon="🪖", layout="wide")

# -------------------------
# Workout definitions by day
# -------------------------
WORKOUTS = {
    "Mon (Day 1) – Full Body Strength": {
        "exercises": ["Push-ups", "Squats", "Plank", "Mountain Climbers", "Burpees"],
        "finisher": "Max Push-ups",
    },
    "Tue (Day 2) – Core & Stability": {
        "exercises": ["Sit-ups / Crunches", "Side Plank (L)", "Side Plank (R)", "Flutter Kicks", "Russian Twists", "Plank Shoulder Taps"],
        "finisher": "Max Mountain Climbers",
    },
    "Wed (Day 3) – Cardio & Endurance": {
        "exercises": ["Jumping Jacks", "High Knees", "Burpees", "Mountain Climbers", "Squat Jumps"],
        "finisher": "Sprint in Place",
    },
    "Thu (Day 4) – Upper Body Power": {
        "exercises": ["Push-ups (Standard/Wide)", "Tricep Dips", "Pike Push-ups", "Plank Up-Downs", "Burpees"],
        "finisher": "Max Push-ups",
    },
    "Fri (Day 5) – Lower Body Strength": {
        "exercises": ["Squats", "Lunges (Alt)", "Wall Sit (Hold)", "Calf Raises", "Jump Squats"],
        "finisher": "Max Lunges",
    },
    "Sat (Day 6) – HIIT Combat": {
        "exercises": ["Burpees", "Push-ups", "Squat Jumps", "Mountain Climbers", "Plank Jacks"],
        "finisher": "Max Burpees",
    },
    "Sun (Day 7) – Recovery & Mobility": {
        "exercises": ["Cat–Cow (Mobility)", "Hip Bridges", "Side Lunges", "Superman Hold", "Plank (Hold)"] ,
        "finisher": "Full-Body Stretch",
    },
}

# -------------------------
# Utilities
# -------------------------

def fmt_time(seconds: int) -> str:
    if seconds < 0:
        seconds = 0
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def build_sequence(day_key: str, work: int, rest: int, rounds: int, warmup: int, finisher: int, include_warmup: bool, include_finisher: bool):
    plan = WORKOUTS[day_key]
    exs = plan["exercises"]
    seq = []
    if include_warmup and warmup > 0:
        seq.append(("Warm-up", warmup))
    for r in range(rounds):
        for i, ex in enumerate(exs):
            seq.append((ex, work))
            # Add rest after each work interval except the very last exercise of the last round
            is_last_block = (r == rounds - 1) and (i == len(exs) - 1)
            if not is_last_block and rest > 0:
                seq.append(("Rest", rest))
    if include_finisher and finisher > 0:
        seq.append((f"Finisher – {plan['finisher']}", finisher))
    return seq


# -------------------------
# Session state init
# -------------------------
if "day" not in st.session_state:
    st.session_state.day = list(WORKOUTS.keys())[0]
if "sequence" not in st.session_state:
    st.session_state.sequence = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "remaining" not in st.session_state:
    st.session_state.remaining = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "last_ts" not in st.session_state:
    st.session_state.last_ts = None


# -------------------------
# Sidebar settings
# -------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Adjust durations if you want a different intensity.")

    st.session_state.day = st.selectbox("Select Day / Plan", list(WORKOUTS.keys()), index=list(WORKOUTS.keys()).index(st.session_state.day))

    colA, colB = st.columns(2)
    with colA:
        work_s = st.number_input("Work (sec)", min_value=10, max_value=120, value=40, step=5)
        rounds = st.number_input("Rounds", min_value=1, max_value=5, value=2, step=1)
        include_warmup = st.checkbox("Include Warm-up", value=True)
    with colB:
        rest_s = st.number_input("Rest (sec)", min_value=5, max_value=120, value=20, step=5)
        finisher_s = st.number_input("Finisher (sec)", min_value=0, max_value=300, value=60, step=5)
        include_finisher = st.checkbox("Include Finisher", value=True)

    warmup_s = st.number_input("Warm-up (sec)", min_value=0, max_value=600, value=120, step=10)

    def reset_plan():
        st.session_state.sequence = build_sequence(
            st.session_state.day,
            work=work_s,
            rest=rest_s,
            rounds=rounds,
            warmup=warmup_s,
            finisher=finisher_s,
            include_warmup=include_warmup,
            include_finisher=include_finisher,
        )
        st.session_state.index = 0
        st.session_state.remaining = st.session_state.sequence[0][1] if st.session_state.sequence else 0
        st.session_state.running = False
        st.session_state.last_ts = None

    if st.button("Build / Reset Plan", use_container_width=True):
        reset_plan()

# Auto-build plan on first load
if not st.session_state.sequence:
    with st.spinner("Preparing your plan..."):
        with st.sidebar:
            st.caption("Tip: You can change settings and press 'Build / Reset Plan'.")
        # Use current sidebar values
        st.session_state.sequence = build_sequence(
            st.session_state.day,
            work=work_s,
            rest=rest_s,
            rounds=rounds,
            warmup=warmup_s,
            finisher=finisher_s,
            include_warmup=include_warmup,
            include_finisher=include_finisher,
        )
        st.session_state.index = 0
        st.session_state.remaining = st.session_state.sequence[0][1]
        st.session_state.running = False
        st.session_state.last_ts = None

# -------------------------
# Header
# -------------------------
st.markdown("""
<style>
.big-timer {font-size: 10rem; font-weight: 800; text-align:center; line-height: 1;}
.phase {font-size: 2rem; text-align:center; margin-top: -10px;}
.note {text-align:center; color: #666;}
.card {padding: 1rem; border-radius: 1rem; border: 1px solid #eee; background: #fafafa;}
</style>
""", unsafe_allow_html=True)

st.title("🪖 Military Workout Timer (15 min)")
st.caption("Large timer with pause/resume, shows current & next exercise. Use the sidebar to pick a day and adjust durations.")

# -------------------------
# Main layout
# -------------------------
left, mid, right = st.columns([1, 2, 1])

# Current and next items
current_label = st.session_state.sequence[st.session_state.index][0] if st.session_state.sequence else ""
next_label = st.session_state.sequence[st.session_state.index + 1][0] if st.session_state.sequence and st.session_state.index + 1 < len(st.session_state.sequence) else "—"

with left:
    st.subheader("Current")
    st.markdown(f"<div class='card'><b>{current_label}</b></div>", unsafe_allow_html=True)

with right:
    st.subheader("Next")
    st.markdown(f"<div class='card'>{next_label}</div>", unsafe_allow_html=True)

with mid:
    # Timer display
    st.markdown(f"<div class='big-timer'>{fmt_time(st.session_state.remaining)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='phase'>{current_label}</div>", unsafe_allow_html=True)

    # Controls
    c1, c2, c3, c4 = st.columns(4)

    if c1.button("▶️ Start / Resume", use_container_width=True):
        st.session_state.running = True
        st.session_state.last_ts = time.monotonic()

    if c2.button("⏸️ Pause", use_container_width=True):
        st.session_state.running = False
        st.session_state.last_ts = None

    if c3.button("⏭️ Skip", use_container_width=True):
        # Skip to next interval
        if st.session_state.index + 1 < len(st.session_state.sequence):
            st.session_state.index += 1
            st.session_state.remaining = st.session_state.sequence[st.session_state.index][1]
            st.session_state.last_ts = time.monotonic() if st.session_state.running else None
        else:
            st.session_state.running = False
            st.session_state.remaining = 0

    if c4.button("🔄 Reset", use_container_width=True):
        # Rebuild sequence with current settings
        reset_plan()

# -------------------------
# Timer engine (frame-by-frame)
# -------------------------
if st.session_state.running and st.session_state.last_ts is not None:
    now = time.monotonic()
    elapsed = now - st.session_state.last_ts
    if elapsed >= 0.2:  # update about 5 times/second for smoothness
        st.session_state.remaining -= elapsed
        st.session_state.last_ts = now
        if st.session_state.remaining <= 0:
            # Advance to next block
            if st.session_state.index + 1 < len(st.session_state.sequence):
                st.session_state.index += 1
                st.session_state.remaining = st.session_state.sequence[st.session_state.index][1]
            else:
                # Done!
                st.session_state.running = False
                st.session_state.remaining = 0
        st.experimental_rerun()

# -------------------------
# Workout plan display
# -------------------------
st.markdown("---")
st.subheader(f"Plan for {st.session_state.day}")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("**Exercises (per round):**")
    for i, ex in enumerate(WORKOUTS[st.session_state.day]["exercises"], start=1):
        st.write(f"{i}. {ex}")
with col2:
    st.write("**Intervals:**")
    st.write(f"Work: {work_s}s")
    st.write(f"Rest: {rest_s}s")
    st.write(f"Rounds: {rounds}")
    if include_warmup and warmup_s:
        st.write(f"Warm-up: {warmup_s}s")
    if include_finisher and finisher_s:
        st.write(f"Finisher: {finisher_s}s – {WORKOUTS[st.session_state.day]['finisher']}")

# Sequence preview table
st.write("")
st.write("**Full Sequence Preview:**")
preview = [
    {"#": i+1, "Phase": label, "Duration": str(timedelta(seconds=secs))[:-3]}
    for i, (label, secs) in enumerate(st.session_state.sequence)
]
st.dataframe(preview, use_container_width=True, hide_index=True)

st.info("Tip: Keep your phone awake while running the timer. You can change day or durations from the sidebar.")
