from utils.schema_def import ColNames
import numpy as np

from utils.scoring import score_column


def calc_agent_caseload(events_data_in):
    agent_workload = events_data_in[[ColNames.TECH_NAME,ColNames.EVENT_ID,ColNames.EVENT_DATE,ColNames.LABOR_DURATION]].copy()
    agent_workload['agent_start_date'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('min')
    agent_workload['agent_end_date'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('max')
    agent_workload['agent_work_duration'] = (agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('max') - agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('min'))/ (np.timedelta64(1,'D')*30)
    agent_workload['agent_total_workdays'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('nunique')
    agent_workload['agent_events'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_ID].transform('nunique')
    agent_workload['agent_total_labor'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.LABOR_DURATION].transform('sum')
    agent_workload['caseload'] = agent_workload['agent_events']/agent_workload['agent_total_workdays']
    agent_workload = agent_workload[[ColNames.TECH_NAME,'caseload']].drop_duplicates()
    return agent_workload


def calc_agent_labor_duration(events_data_in):
    agent_workload = events_data_in[[ColNames.TECH_NAME,ColNames.EVENT_ID,ColNames.EVENT_DATE,ColNames.LABOR_DURATION]].copy()
    agent_workload['agent_start_date'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('min')
    agent_workload['agent_end_date'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('max')
    agent_workload['agent_work_duration'] = (agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('max') - agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('min'))/ (np.timedelta64(1,'D')*30)
    agent_workload['agent_total_workdays'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_DATE].transform('nunique')
    agent_workload['agent_events'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.EVENT_ID].transform('nunique')
    agent_workload['agent_total_labor'] = agent_workload.groupby(ColNames.TECH_NAME)[ColNames.LABOR_DURATION].transform('sum')
    agent_workload['labor_duration'] = agent_workload['agent_total_labor'] / agent_workload['agent_total_workdays']
    agent_workload = agent_workload[[ColNames.TECH_NAME,'labor_duration']].drop_duplicates()
    return agent_workload


def calc_agent_caseload_score(events_data_in):
    agent_workload = calc_agent_caseload(events_data_in)
    agent_workload_w_score = score_column(agent_workload,'caseload')
    return agent_workload_w_score

def calc_agent_labor_duration_score(events_data_in):
    agent_workload = calc_agent_labor_duration(events_data_in)
    agent_workload_w_score = score_column(agent_workload,'labor_duration')
    return agent_workload_w_score



