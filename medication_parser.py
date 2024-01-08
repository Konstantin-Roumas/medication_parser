import pandas as pd
import re


def filter_values(input_string):
    pattern = re.compile(r'(\d+(\.\d+)?)\s?(mg|mcg|ml|%)\b')
    matches = pattern.findall(input_string)
    result_list = [(float(match[0]), match[2]) for match in matches]
    return result_list


raw_data = pd.read_csv(
    'Result_1.csv',
    names=['Protocol', 'Medication', 'Medication Strength', 'Amount']
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
maximus_free = list()
for data in brackets_clean:
    if "Maximus" in data:
        maximus_free.append(data.replace("Maximus", ''))
    else:
        maximus_free.append(data)
digit_free = ["".join(filter(lambda x: not x.isdigit() and x != "%" and x != ".", s)) for s in maximus_free]
print(maximus_free)
for data in maximus_free:
    splitted_part = data.split()
    splitted_part = splitted_part[0]
    first_part.append(splitted_part)
res = ''
for data in result_df:
    res += data + '\n'
pattern = re.compile(r'(\d+(\.\d+)?)\s?(mg|mcg|ml|%)\b')
matches = list()
for data in maximus_free:
    matches.append(pattern.findall(data))
with open('result.csv', 'w') as f:
    f.writelines(res)
medication_strength = list()
formatted_data = list()
f = ''
result_list = [filter_values(item) for item in maximus_free]
for l in result_list:
    for t in l:
        for item in t:
            f += str(item)+' '
    formatted_data.append(f)
    f = ''
print(formatted_data)
check = pd.DataFrame()
check['Formatted Data'] = formatted_data
check.to_csv('formatted.csv', index=False)
result_df['Medication'] = first_part
result_df['Medication Strength'] = formatted_data
result_df['Elation Medication Name'] = raw_data['Medication']
result_df.to_csv('res.csv',index=False)
