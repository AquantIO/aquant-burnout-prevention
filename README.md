Service Technician Burnout Prevention

This repository contains the code for a system designed to flag technicians who may be experiencing burnout. The system processes and analyzes various work-related metrics to provide insights into potential burnout risks based on correlated factors. It is intended to help managers proactively support their team members by identifying technicians who may need assistance in maintaining a healthy work-life balance.

Overview

The system uses event data to calculate several key metrics related to technician workload, travel, vacation patterns, and symptoms of potential burnout. It produces scores and flags based on these metrics to indicate where a technician may be at risk of burnout. These insights can be used for early intervention, allowing managers to address potential issues before they escalate.

Features

Caseload Analysis: Calculates the average caseload per workday to assess daily workload intensity.
Labor Duration Scoring: Analyzes the average time spent on work activities per day to identify technicians who may be overworked.
Vacation Monitoring: Tracks time since last vacation and the duration of vacations to flag technicians who may need a break.
Travel Time Assessment: Evaluates total and average travel time per day to identify technicians with potentially excessive travel burdens.
Outlier Detection: Identifies irregular work patterns by detecting unusually long or short labor durations.
Negative Events Tracking: Counts and rates negative events (e.g., complaints, errors) to signal performance or morale issues.
Burnout Indices: Combines various metrics into "Cause" and "Symptom" burnout indices to provide an overall assessment of burnout risk.



Usage

Preprocess Event Data: Prepare and clean the input event data using the preprocessing.py module.
Run the Main Script: Execute main.py to load the data, calculate metrics, and generate burnout scores:

python main.py
The script will output results to an Excel file, including sheets for overall burnout scores and recent symptom changes.
Analyze Results: Use the scores and flags generated to identify technicians who may need support.

Key Modules

preprocessing.py: Prepares and cleans event data for analysis.
scoring.py: Scores numerical columns using outlier detection and normalization.
trends.py: Detects sharp changes in work patterns.
symptom_detection.py: Calculates burnout indices based on symptom-related metrics.
cause_detection.py: Computes burnout indices based on workload and other "cause" factors.
freetext_sentiment.py: Analyzes text sentiment to gauge technician morale.
workload.py: Assesses the workload by calculating caseload and labor duration scores.
time_off.py: Evaluates vacation patterns to determine potential burnout risk.

Configuration
Column names must be set in utils/schema_def.py
Required columns are event agent name, event date and event ID. Other columns are optional, and if no match exists for them then related functionality will be skipped.

You can customize various parameters (e.g., thresholds for burnout indices, data input paths, weightings) to tailor the system to your specific needs.


Contributing

If you'd like to contribute to this project, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.

Contact

For any questions or feedback, please contact tommer.vardi@aquant.ai
