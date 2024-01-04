import pandas as pd
import re

raw_data = pd.read_csv(
    '',
    names=['Protocol', 'Medication']
)
result_df = pd.DataFrame()
raw_medication = list()
protocols = list()
for data in raw_data['Protocol']:
    protocols.append(str(data).capitalize())
for data in raw_data['Medication']:
    raw_medication.append(data)
brackets_clean = list()
for brackets in raw_medication:
    brackets_clean.append(re.sub(r'\[.*?\]|\(.*?\)', '', brackets))
building_blocks = list()
for bb in brackets_clean:
    if "w/ SUPPLEMENT" in bb:
        building_blocks.append("True")
    else:
        building_blocks.append("False")
result_df['BuildingBlocks'] = building_blocks
result_df['Protocol'] = protocols
first_part = list()
for data in brackets_clean:
    splitted_part = data.split()
    first_part.append(splitted_part[0])
res = ''
for data in brackets_clean:
    res += data +'\n'

with open('result.csv', 'w') as f:
    f.writelines(res)
result_df['Medication'] = first_part
