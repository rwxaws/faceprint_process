import pandas as pd
import datetime as dt

import config.headers as headers


def extract_excuses(
    vacation_duty_df: pd.DataFrame,
    earlylate_absent_df: pd.DataFrame,
    provided_date: str
):

    required_date = dt.datetime.strptime(provided_date, '%Y-%m-%d').date()

    vacation_matched_date = vacation_duty_df['vacation_from'].dt.date == required_date
    hourly_matched_date = vacation_duty_df['date'].dt.date == required_date
    vacation_duty_df = vacation_duty_df[vacation_matched_date | hourly_matched_date]

    merged_df = pd.merge(earlylate_absent_df, vacation_duty_df, on='emp_voter_num', how='left', indicator=True, suffixes=('', '_x'))

    has_excuse = merged_df[merged_df['_merge'] == 'both']
    no_excuse = merged_df[merged_df['_merge'] == 'left_only']

    # drop columns that have merge or _x
    no_excuse = no_excuse.drop(columns=[col for col in no_excuse.columns if col.endswith('_x')])
    has_excuse = has_excuse.drop(columns=[col for col in has_excuse.columns if col.endswith('_x')])

    no_excuse = no_excuse.loc[:, headers.PROCESSINGHEADERS.earlylate_absent_header]
    no_excuse['date'] = no_excuse['date'].dt.date
    no_excuse['entry_timestamp'] = no_excuse['entry_timestamp'].dt.time
    no_excuse['leave_timestamp'] = no_excuse['leave_timestamp'].dt.time

    has_excuse = has_excuse.loc[:, headers.PROCESSINGHEADERS.has_excuse_header]
    has_excuse['date'] = has_excuse['date'].dt.date
    has_excuse['entry_timestamp'] = has_excuse['entry_timestamp'].dt.time
    has_excuse['leave_timestamp'] = has_excuse['leave_timestamp'].dt.time

    return has_excuse, no_excuse
