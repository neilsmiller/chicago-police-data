#!usr/bin/env python3
#
# Author(s):    Roman Rivera

'''assign-unique-ids script for p046360_TRR-2016-aug/trr-statuses'''

import pandas as pd
import __main__

from assign_unique_ids_functions import assign_unique_ids, aggregate_data
import setup


def get_setup():
    ''' encapsulates args.
        calls setup.do_setup() which returns constants and logger
        constants contains args and a few often-useful bits in it
        including constants.write_yamlvar()
        logger is used to write logging messages
    '''
    script_path = __main__.__file__
    args = {
        'input_file': 'input/trr-statuses.csv.gz',
        'output_file': 'output/trr-statuses.csv.gz',
        'output_demo_file': 'output/trr-statuses_demographics.csv.gz',
        'id_cols': [
            "first_name", "last_name", "middle_initial", "suffix_name",
            "first_name_NS", "last_name_NS", "middle_initial2",
            "appointed_date", "gender", "race"
            ],
        'current_cols': ['star'],
        'time_col': 'status_date',
        'id': 'trr-statuses_ID'
        }

    assert (args['input_file'].startswith('input/') and
            args['input_file'].endswith('.csv.gz')),\
        "input_file is malformed: {}".format(args['input_file'])
    assert (args['output_file'].startswith('output/') and
            args['output_file'].endswith('.csv.gz')),\
        "output_file is malformed: {}".format(args['output_file'])

    return setup.do_setup(script_path, args)


cons, log = get_setup()

df = pd.read_csv(cons.input_file)

df, uid_report = assign_unique_ids(df, cons.id, cons.id_cols)
log.info(uid_report)
df.to_csv(cons.output_file, **cons.csv_opts)

agg_df = aggregate_data(df, cons.id, cons.id_cols,
                        current_cols=cons.current_cols,
                        time_col=cons.time_col)
agg_df.to_csv(cons.output_demo_file, **cons.csv_opts)