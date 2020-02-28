# import json

# json_list = []
# csv_file = open('7612버스노선.csv', 'r', encoding='utf8')

# for line in csv_file.readlines():
#     bus_id, number, sta_nm, x_coordi, y_coordi, sta_id = line.strip().split(',')
#     data = {
#         'bus_id': bus_id,
#         'number': number,
#         'sta_nm': sta_nm,
#         'coordinates': [float(x_coordi), float(y_coordi)],
#         'sta_id': sta_id,
#     }
#     json_list.append(data)

# csv_file.close()

# json_file = open('json_file.json', 'w', encoding='utf8')
# # 저장된것을 보면 한글이 byte 문자로 깨져서 나오는데 
# # ensure_ascii=False 옵션넣어주면 해결됨
# json.dump(json_list, json_file, ensure_ascii=False)
# json_file.close()

import json
import xlrd
from collections import OrderedDict

wb = xlrd.open_workbook('7611.xlsx')
sh = wb.sheet_by_index(0)

data_list = []

for rownum in range(1, sh.nrows):
    data = OrderedDict()
    row_values = sh.row_values(rownum)
    # 좌표값만 가져와 저장
    data['x_coordi'] = row_values[3]
    data['y_coordi'] = row_values[4]
    # data_list에 좌표값 추가
    data_list.append(data)

# ensure_ascii=False 옵션넣어주면 한글깨짐/바이트출력 문제 해결
# json 형태의 문자열을 보기 좋게 나오게 하려면 dumps에 indent 옵션 추가
j = json.dumps(data_list, ensure_ascii=False, indent=4)

# json파일로 저장
with open('7611.json', 'w+') as f:
    f.write(j)