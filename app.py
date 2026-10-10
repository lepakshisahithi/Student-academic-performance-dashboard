import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Student Academic Performance Dashboard",
    page_icon="🎓",
    layout="wide",
)

DATA_PATH = "StudentsPerformance.csv"
SCORE_COLUMNS = ["math score", "reading score", "writing score"]
SCORE_LABELS = {
    "math score": "Math",
    "reading score": "Reading",
    "writing score": "Writing",
}

@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    # Clean column names just in case the CSV has extra spaces.
    data.columns = [column.strip() for column in data.columns]
    for col in SCORE_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=SCORE_COLUMNS)
    return data

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"Could not find `{DATA_PATH}`. Keep StudentsPerformance.csv in the same "
        "folder as app.py, then run the app again."
    )
    st.stop()

st.title("🎓 Student Academic Performance Dashboard")
st.write(
    "Explore student exam scores and compare performance by gender, parental "
    "education, lunch type, test preparation, and race/ethnicity."
)

# All sidebar controls are applied to one shared filtered dataframe.
st.sidebar.header("🔎 Dashboard Filters")
st.sidebar.caption("Change any filter to update every chart and KPI.")

def multiselect_filter(label, column):
    options = sorted(df[column].dropna().unique().tolist())
    return st.sidebar.multiselect(label, options, default=options)

gender_options = multiselect_filter("Gender", "gender")
group_options = multiselect_filter("Race / ethnicity", "race/ethnicity")
parent_edu_options = multiselect_filter(
    "Parental level of education", "parental level of education"
)
lunch_options = multiselect_filter("Lunch type", "lunch")
prep_options = multiselect_filter("Test preparation course", "test preparation course")

score_min = int(df[SCORE_COLUMNS].min().min())
score_max = int(df[SCORE_COLUMNS].max().max())
score_range = st.sidebar.slider(
    "Score range (applies to all subjects)",
    min_value=score_min,
    max_value=score_max,
    value=(score_min, score_max),
)

filtered = df[
    df["gender"].isin(gender_options)
    & df["race/ethnicity"].isin(group_options)
    & df["parental level of education"].isin(parent_edu_options)
    & df["lunch"].isin(lunch_options)
    & df["test preparation course"].isin(prep_options)
].copy()

# Keep students whose scores for all three subjects fall inside the chosen range.
for score_col in SCORE_COLUMNS:
    filtered = filtered[filtered[score_col].between(score_range[0], score_range[1])]

if filtered.empty:
    st.warning("No students match these filters. Adjust the sidebar selections.")
    st.stop()

filtered["average score"] = filtered[SCORE_COLUMNS].mean(axis=1).round(2)
filtered["overall result"] = filtered["average score"].apply(
    lambda score: "Pass (50+)" if score >= 50 else "Below 50"
)

# KPI cards
k1, k2, k3, k4 = st.columns(4)
k1.metric("Students in selection", f"{len(filtered):,}")
k2.metric("Average overall score", f"{filtered['average score'].mean():.2f} / 100")
k3.metric("Highest average score", f"{filtered['average score'].max():.2f} / 100")
k4.metric("Average math score", f"{filtered['math score'].mean():.2f} / 100")

st.divider()

# Every visualization below uses `filtered`, so the sidebar filters affect all charts.
left, right = st.columns(2)

with left:
    st.subheader("1. Average score by subject")
    subject_means = filtered[SCORE_COLUMNS].mean().rename(index=SCORE_LABELS).reset_index()
    subject_means.columns = ["Subject", "Average score"]
    fig = px.bar(
        subject_means,
        x="Subject",
        y="Average score",
        color="Subject",
        text_auto=".2f",
        title="Average marks across subjects",
        range_y=[0, 100],
    )
    fig.update_layout(showlegend=False, yaxis_title="Average score (0–100)")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("2. Score distribution")
    selected_subject = st.selectbox(
        "Choose subject for the distribution chart",
        SCORE_COLUMNS,
        format_func=lambda value: SCORE_LABELS[value],
        key="distribution_subject",
    )
    fig = px.histogram(
        filtered,
        x=selected_subject,
        nbins=20,
        title=f"{SCORE_LABELS[selected_subject]} score distribution",
        labels={selected_subject: "Score"},
        color_discrete_sequence=["#4C78A8"],
    )
    fig.update_layout(yaxis_title="Number of students", xaxis_title="Score")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("3. Average scores by test preparation")
    prep_summary = (
        filtered.groupby("test preparation course", as_index=False)[SCORE_COLUMNS]
        .mean()
        .melt(
            id_vars="test preparation course",
            value_vars=SCORE_COLUMNS,
            var_name="Subject",
            value_name="Average score",
        )
    )
    prep_summary["Subject"] = prep_summary["Subject"].map(SCORE_LABELS)
    fig = px.bar(
        prep_summary,
        x="test preparation course",
        y="Average score",
        color="Subject",
        barmode="group",
        title="Subject averages by preparation status",
        range_y=[0, 100],
        labels={
            "test preparation course": "Test preparation",
            "Average score": "Average score (0–100)",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("4. Scores by parental education")
    education_summary = (
        filtered.groupby("parental level of education", as_index=False)[SCORE_COLUMNS]
        .mean()
        .melt(
            id_vars="parental level of education",
            value_vars=SCORE_COLUMNS,
            var_name="Subject",
            value_name="Average score",
        )
    )
    education_summary["Subject"] = education_summary["Subject"].map(SCORE_LABELS)
    fig = px.bar(
        education_summary,
        x="parental level of education",
        y="Average score",
        color="Subject",
        barmode="group",
        title="Average marks by parental education",
        range_y=[0, 100],
        labels={
            "parental level of education": "Parental education",
            "Average score": "Average score (0–100)",
        },
    )
    fig.update_layout(xaxis_tickangle=-25)
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("5. Relationship between subject scores")
    fig = px.scatter(
        filtered,
        x="math score",
        y="reading score",
        color="gender",
        size="writing score",
        hover_data=["race/ethnicity", "test preparation course"],
        title="Math vs reading scores (bubble size = writing score)",
        labels={"math score": "Math score", "reading score": "Reading score"},
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("6. Correlation between scores")
    corr = filtered[SCORE_COLUMNS].rename(columns=SCORE_LABELS).corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Subject score correlation heatmap",
        aspect="auto",
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered student records")
st.caption("This table also reflects the current sidebar filters.")
display_columns = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
    "math score",
    "reading score",
    "writing score",
    "average score",
    "overall result",
]
st.dataframe(
    filtered[display_columns].reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
)

csv_data = filtered[display_columns].to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download filtered data as CSV",
    data=csv_data,
    file_name="filtered_student_performance.csv",
    mime="text/csv",
)

with st.expander("About this project"):
    st.write(
        "This dashboard uses the Students Performance in Exams dataset. "
        "It explores math, reading, and writing scores. The filters in the "
        "sidebar are shared across all charts, summary metrics, and the table. "
        "The 50-point label is a simple project-defined threshold, not an "
        "official grading rule."
    )
