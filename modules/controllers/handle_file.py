import json


def read_file_c(file):
    temp = []
    with open(file) as json_file:
        data = json.load(json_file)
        temp = data['data']
    return temp


def write_file_c(file, datas):
    temp = {"data": []}
    for data in datas:
        temp['data'].append(data)
    ff = temp
    # print(type(ff))
    with open(file, 'w') as file_:
        file_.write(json.dumps(ff))

    # print()
    # print(json.dump('{ "data" : 1  , "d" : 2}'))
