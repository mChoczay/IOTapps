import csv
import json




def read_csv1(source):
    with open(source) as csvfile:
        reader=list(csv.reader(csvfile))
        data = reader[1:]

    return data


def read_csv(source):
    newlist = []
    data = read_csv1(source)
    for datas in data:
        count = 0 
        for i in datas:
            if count == 1:
                newlist.append(i)
            count+=1
    return newlist

# def read_csv2(source):
#     newlist = []
#     data = read_csv1(source)
#     for datas in data:
#         count = 0 
#         for i in datas:
#             if count == 1:
#                 newlist.append(i)
#             count+=1
#     return newlist