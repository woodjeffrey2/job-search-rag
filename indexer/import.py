# Imports cleaned state skills data from csv files as Weaviate vectors

import pandas as pd
import helper
import weaviate
import os
import glob

INPUT_FILES = '/data/skills/*.csv'

client = weaviate.Client("http://localhost:8080")
client.timeout_config = (3, 200)

# empty schema and create new schema
# client.schema.delete_all()
# schema = { add schema here }
#
# client.schema.create(schema)

def add_skills(data, batch_size=512, debug_mode=False):
    """ upload skills to Weaviate

    :param data: skills data in panda dataframe object
    :type data: panda dataframe object (4 columns: 'subject', 'root_skill', 'skill', 'skill_description')
    :param batch_size: number of data objects to put in one batch, defaults to 512
    :type batch_size: int, optional
    :param debug_mode: set to True if you want to display upload errors, defaults to False
    :type debug_mode: bool, optional
    """

    no_items_in_batch = 0

    for index, row in data.iterrows():
        skill_object = {
            "subject": row["subject"],
            "root_skill": row["root_skill"],
            "skill": row["skill"],
            "skill_description": row["skill_description"]
        }

        skill_uuid = helper.generate_uuid('skill', row["skill"])

        client.batch.add_data_object(skill_object, "Skill", skill_uuid)
        no_items_in_batch += 1

        if no_items_in_batch >= batch_size:
            results = client.batch.create_objects()

            if debug_mode:
                for result in results:
                    if result['result'] != {}:
                        helper.log(result['result'])

                message = str(index) + ' / ' + str(data.shape[0]) +  ' items imported'
                helper.log(message)

            no_items_in_batch = 0

    message =  str(data.shape[0]) +  ' items imported'
    helper.log(message)

    results = client.batch.create_objects()
    for result in results:
        if result['result'] != {}:
            helper.log(result['result'])

csv_files = glob.glob(helper.from_root_dir(INPUT_FILES))

for f in csv_files:
    df = pd.read_csv(f)
    add_skills(df.head(4000), batch_size=99, debug_mode=True)
