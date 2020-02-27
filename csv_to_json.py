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

json_list = []
csv_file = open('7612버스노선.csv', 'r', encoding='utf8')

for line in csv_file.readlines():
    bus_id, number, sta_nm, x_coordi, y_coordi, sta_id = line.strip().split(',')
    data = [
        float(x_coordi), float(y_coordi),
    ]
    json_list.append(data)

csv_file.close()

json_file = open('coordi.json', 'w', encoding='utf8')
# 저장된것을 보면 한글이 byte 문자로 깨져서 나오는데 
# ensure_ascii=False 옵션넣어주면 해결됨
# json 형태의 문자열을 보기 좋게 나오게 하려면 dumps에 indent 옵션 추가
json.dump(json_list, json_file, ensure_ascii=False, indent=4)
json_file.close()
