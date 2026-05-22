# Can Care Be Automated?

**Live Dashboard:** https://robot-caregiver-dashboard-pt6kzpzyeczxsxbuzq4vd9.streamlit.app/

This project is a Streamlit data dashboard about how American adults imagined robot caregivers. It treats public opinion not as a simple yes or no answer, but as a movement between readiness, realism, enthusiasm, family responsibility, social consequences, reasons for acceptance and refusal, and human oversight.

## Project Overview

The central question of this dashboard is:

**Can care be automated without losing the human factor?**

The dashboard argues that robot caregivers are not judged only as machines. They are also judged as possible substitutes for human care, family responsibility, emotional presence, independence, isolation, and human oversight.

## Dashboard Structure

The dashboard is organized as a six chapter data story.

1. **Readiness**  
   Shows whether the public can imagine robot care as familiar, realistic, enthusiastic, and personally usable.

2. **Pathway**  
   Uses a Sankey diagram to show how perceived realism connects to enthusiasm and willingness to use robot caregivers.

3. **Context**  
   Uses a heatmap to compare attitudes across different levels of caregiving responsibility.

4. **Consequences**  
   Uses a promise and anxiety map to compare expected benefits and concerns.

5. **Reasons**  
   Uses a treemap to compare written reasons for acceptance and refusal.

6. **Oversight**  
   Uses a ternary triangle to show whether camera monitoring by a human operator makes robot care feel better, neutral, or worse.

## Data

The project uses survey data about American adults' views on robot caregivers. The repository includes raw data files and processed CSV files used by the dashboard.

Processed data files are stored in:

data/processed/

Key processed files include:

caregiver_respondent_clean.csv  
care_responsibility_heatmap.csv  
reason_bubble_summary.csv  
readiness_summary.csv  
consequence_summary.csv  
oversight_summary.csv  

Raw data files are stored in:

data/raw/

## How to Run

Install the required packages:

pip install -r requirements.txt

Run the Streamlit dashboard:

streamlit run app.py

## Repository Structure

robot-caregiver-dashboard/
├── app.py
├── clean_data.py
├── inspect_data.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/
│   └── processed/
└── writeup/

## Design Notes

The dashboard uses a dark visual theme with semantic colors.

Blue is used for realism, information, and interaction guidance.  
Yellow is used for emotional transition and ambivalent states.  
Red is used for worry, refusal, anxiety, and value tension.  
Green is used for willingness, promise, and positive adoption signals.

The goal is to make the dashboard feel like a data story rather than a set of disconnected charts.

## Statement on Collaboration

This was an individual project. I used ChatGPT as a support tool for debugging Streamlit layout issues, refining dashboard wording, checking whether the visualizations matched the assignment requirements, and improving the visual organization of the dashboard. The data selection, dashboard concept, chart choices, interpretation, and final editing decisions were my own.

## Author

Yue Jin  
DIGS 30004 Final Dashboard
