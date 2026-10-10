# Student Academic Performance Analysis Dashboard

An interactive data visualization mini project built with **Python, Streamlit, Pandas, and Plotly**.

## Features

- Sidebar filters for gender, race/ethnicity, parental education, lunch type, test preparation, and score range.
- All sidebar filters update the KPIs, every chart, and the student records table.
- KPI cards for number of students and average/highest scores.
- Bar charts, histogram, scatter plot, and correlation heatmap.
- Download the currently filtered student records as a CSV file.

## Dataset

The included file is `StudentsPerformance.csv`, based on the Kaggle **Students Performance in Exams** dataset.

Original Kaggle page: https://www.kaggle.com/datasets/spscientist/students-performance-in-exams

Dataset columns include gender, race/ethnicity, parental level of education, lunch, test preparation course, math score, reading score, and writing score.

## Run locally

1. Install Python 3.9 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install the packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

6. Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.

## Deploy on Streamlit Community Cloud

1. Push `app.py`, `StudentsPerformance.csv`, and `requirements.txt` to a GitHub repository.
2. Sign in to Streamlit Community Cloud: https://share.streamlit.io/
3. Select **Create app** and choose your GitHub repository.
4. Set the main file path to `app.py`.
5. Deploy the app.

Keep `StudentsPerformance.csv` in the same folder as `app.py`.

## Repository structure

```text
student-academic-performance-dashboard/
├── app.py
├── StudentsPerformance.csv
├── requirements.txt
└── README.md
``#DASHBOARD LINK:
https://student-academic-performance-dashboard-k2zfcptdtggl67jm7hdvqr.streamlit.app/

## Notes

- Filters are shared: each selected sidebar filter is applied to all visualizations and the table.
- The score-range filter keeps records where all three subject scores fall inside the selected range.
- The “Pass (50+)” label is a simple illustrative threshold for this project, not an official grading rule.
