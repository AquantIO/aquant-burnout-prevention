import pandas as pd

from causes.cause_detection import calculate_burnout_index_causes
from causes.time_off import calc_vacation_score
from causes.travel_time import calc_agent_travel_time_score, calc_agent_travel_time
from causes.workload import calc_agent_caseload_score
from symptoms.outlier_labor_duration import find_outlier_labor_durations
from symptoms.symptom_detection import calculate_burnout_index_symptoms
from utils.function_inputs import DetectSharpChangesWFuncInput
from utils.preprocessing import prepare_events_data
from utils.schema_def import ColNames
from utils.trends import detect_sharp_changes_with_function

#enter your file path
working_dir = "/Your/Path/Here"
import_filename = "input_filename.csv"
export_filename = "output_filename.xlsx"
filepath_input = f'{working_dir}/{import_filename}'
filepath_output = f'{working_dir}/{export_filename}'
#load data
events_data = pd.read_csv(filepath_input)#+'/'+import_filename)
#column mapping

events_data = prepare_events_data(events_data)

cause_score = calculate_burnout_index_causes(events_data)
symptom_score = calculate_burnout_index_symptoms(events_data)
burnout_score = pd.merge(cause_score, symptom_score, on=ColNames.TECH_NAME, how='outer')
burnout_score['burnout_index'] = burnout_score[['burnout_index_causes', 'burnout_index_symptoms']].mean(axis=1)
burnout_score = burnout_score.sort_values('burnout_index', ascending=False)





sharp_chang_input = DetectSharpChangesWFuncInput(df=events_data, func=calculate_burnout_index_symptoms, eval_col='burnout_index_symptoms', output_type='detailed')
recent_symptom_changes = detect_sharp_changes_with_function(sharp_chang_input)
recent_symptom_changes = recent_symptom_changes.sort_values('rel_difference', ascending=False)

# Create an ExcelWriter object and specify the file name
with pd.ExcelWriter(filepath_output) as writer:
    burnout_score.to_excel(writer, sheet_name='overall burnout scoring', index=False)
    recent_symptom_changes.to_excel(writer, sheet_name='recent symptom changes', index=False)
