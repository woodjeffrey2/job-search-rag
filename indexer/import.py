# Imports cleaned state skills data from csv files as Weaviate vectors

import pandas as pd
import weaviate
import yaml
import uuid

INPUT_FILE = "./indexer/data/experiences.yml"
COLLECTION_NAME = "Experience"

client = weaviate.connect_to_local()
client.timeout_config = (3, 200)


def add_experiences(data):
    """upload professional experience to Weaviate

    :param data: experiences data in panda dataframe object
    :type data: panda dataframe object (2 columns: 'description', 'job')
    """
    with client.batch.dynamic() as batch:
        for index, row in data.iterrows():
            exp = row.to_dict()
            print("Adding experience:", exp)

            exp_uuid = str(
                uuid.uuid5(uuid.NAMESPACE_DNS, row["job"] + str(row["exp_id"]))
            )
            batch.add_object(
                properties=exp,
                collection=COLLECTION_NAME,
                uuid=exp_uuid,
            )

        if batch.number_errors > 0:
            print(f"Errors: {batch.number_errors}")
            print("Failed Objects: ", batch.failed_objects)

    message = str(index + 1) + " / " + str(data.shape[0]) + " items imported"
    print(message)


with open(INPUT_FILE, "r") as file:
    yaml_data = yaml.safe_load(file)
experiences_data = yaml_data.get("experiences", [])
exps = pd.DataFrame(experiences_data)

try:
    add_experiences(exps)

finally:
    client.close()
