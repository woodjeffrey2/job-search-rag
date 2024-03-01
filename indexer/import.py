# Imports cleaned state skills data from csv files as Weaviate vectors

import pandas as pd
import weaviate
import yaml
import uuid

INPUT_FILE = './indexer/data/experiences.yml'
CLASS_NAME = 'Experience'

client = weaviate.connect_to_local()
client.timeout_config = (3, 200)

def add_experiences(data):
    """ upload professional experience to Weaviate

    :param data: experiences data in panda dataframe object
    :type data: panda dataframe object (2 columns: 'description', 'job')
    """
    with client.batch.dynamic() as batch:
        for index, row in data.iterrows():
            exp = row.to_dict()
            print('Adding experience:', exp)
            batch.add_object(properties=row.to_dict(), collection=CLASS_NAME, uuid=uuid.uuid4())

    message = str(index+1) + ' / ' + str(data.shape[0]) +  ' items imported'
    print(message)


with open(INPUT_FILE, 'r') as file:
    yaml_data = yaml.safe_load(file)
experiences_data = yaml_data.get('experiences', [])
df = pd.DataFrame(experiences_data)

try:
  add_experiences(df, batch_size=99, debug_mode=True)

except Exception as e:
  print('Error: ' + e)

finally:
  client.close()
