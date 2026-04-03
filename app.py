import numpy as np
import streamlit as st

st.set_page_config(page_title="Student Score Analyzer", layout="centered")

st.title("📊 Student Score Analyzer")

# -------------------------------
# Generate Scores
# -------------------------------
st.header("🎲 Generate Scores")

n = st.number_input("Number of Students", min_value=1, value=10)

if st.button("Generate Scores"):
    names = np.array([f"Student {i+1}" for i in range(int(n))])
    scores = np.random.randint(0, 101, size=int(n))
    table = np.column_stack((names, scores))

    st.session_state["data"] = table

# Display data
if "data" in st.session_state:
    st.subheader("📋 Student Scores")
    st.dataframe(st.session_state["data"], use_container_width=True)


# -------------------------------
# Full Analysis
# -------------------------------
st.header("📈 Full Analysis")

def score_statistics(data):
    scores = data[:, 1].astype(float)
    return np.mean(scores), np.max(scores), np.min(scores), np.sum(scores)

def pass_fail_analysis(data):
    scores = data[:, 1].astype(float)
    return np.sum(scores >= 40), np.sum(scores < 40)

def top_students(data):
    names = data[:, 0]
    scores = data[:, 1].astype(float)

    sorted_idx = np.argsort(scores)[::-1][:3]
    return names[sorted_idx], scores[sorted_idx]

if st.button("Run Analysis"):
    if "data" not in st.session_state:
        st.error("Generate scores first!")
    else:
        data = st.session_state["data"]

        avg, highest, lowest, total = score_statistics(data)
        passed, failed = pass_fail_analysis(data)
        top_names, top_scores = top_students(data)

        st.subheader("📊 Results")

        st.write(f"**Average Score:** {avg:.2f}")
        st.write(f"**Highest Score:** {highest}")
        st.write(f"**Lowest Score:** {lowest}")
        st.write(f"**Total Score:** {total}")
        st.write(f"**Passed Students:** {passed}")
        st.write(f"**Failed Students:** {failed}")

        st.write("### 🏆 Top 3 Students")
        for i in range(3):
            st.write(f"{i+1}. {top_names[i]} - {top_scores[i]}")


# -------------------------------
# Filter Scores
# -------------------------------
st.header("🔍 Filter High Scores")

threshold = st.number_input("Threshold", value=75)

if st.button("Filter Scores"):
    if "data" not in st.session_state:
        st.error("Generate scores first!")
    else:
        data = st.session_state["data"]
        scores = data[:, 1].astype(float)

        mask = scores > float(threshold)
        filtered = np.column_stack((data[:, 0][mask], scores[mask]))

        st.subheader("📋 Filtered Results")
        st.dataframe(filtered, use_container_width=True)
