from os import listdir
from sys import argv
from datetime import datetime as dt
import datetime
import codecs 
import json


def process_input(start_date_str, end_date_str, pre_days_str, output_file, files):
    print(start_date_str, end_date_str, pre_days_str)
    while start_date_str + '.json' not in files:
        date_object = dt.strptime(start_date_str, '%Y-%m-%d') + datetime.timedelta(days = 1)
        start_date_str = date_object.strftime('%Y-%m-%d')
    start = files.index(start_date_str + '.json')

    while end_date_str + '.json' not in files:
        date_object = dt.strptime(end_date_str, '%Y-%m-%d') - datetime.timedelta(days = 1)
        end_date_str = date_object.strftime('%Y-%m-%d')
    end = files.index(end_date_str + '.json')
    pre_days = int(pre_days_str)

    return start, end, pre_days, output_file


def load_data(start, end, last_days, file_list):
    # load data from end date to start date - last days
    stock_info= {}
    ignore_stock_ids = ['id']
    features = ['open', 'close', 'high', 'low', 'volume', 'adj_close']
    for i in range(end_index - start_index + last_days + 1):
        data = json.load(codecs.open(input_file_path + file_list[end_index - i], 'r'))
        for stock_id in data:
            if stock_id not in stock_info and stock_id not in ignore_stock_ids:
                stock_info[stock_id] = {}
            stock_info[stock_id][i] = {}
            for f in features:
                if data[stock_id][f] != 'NULL':
                    try:
                        stock_info[stock_id][i][f] = float(data[stock_id][f])
                    except:
                        ignore_stock_ids.append(stock_id)
                else:
                    ignore_stock_ids.append(stock_id)

    for stock_id in ignore_stock_ids:
        if stock_id in stock_info:
            del stock_info[stock_id]

    return stock_info


def cal_RSI(data):
    output_RSI = {}
    for key, data_of_days in data.items():
        delta = []
        for i in range(1, len(data_of_days) - 1):
            delta.append(data_of_days[i]['close'] - data_of_days[i + 1]['close'])

        RSI_5 = []
        RSI_10 = []
        for i in range(delta):
            if i + 4 < len(delta):
                up = 0
                down = 0
                for j in range(5):
                    if delta[i + j] > 0:
                        up += delta[i + j]
                    elif delta[i + j] < 0:
                        down += delta[i + j]
                RSI_5.append(up * 100.0 / (up + down))

        for i in range(delta):
            if i + 9 < len(delta):
                up = 0
                down = 0
                for j in range(10):
                    if delta[i + j] > 0:
                        up += delta[i + j]
                    elif delta[i + j] < 0:
                        down += delta[i + j]
                RSI_10.append(up * 100.0 / (up + down))

        output_RSI[key] = []
        for i in range(RSI_10):
            output_RSI[key].append(RSI_10[i])    
            output_RSI[key].append(RSI_5[i])

    return output_RSI


if __name__ == '__main__':
    input_file_path = '/home/mlb/res/stock/twse/json/'
    file_list = listdir(input_file_path)
    file_list.sort()
    start_index, end_index, last_n_days, output_file = process_input(argv[1], argv[2], argv[3], argv[4], file_list)
    data_of_days = []
    output_data = {}
    with codecs.open(output_file, 'w') as fw:
        all_info = load_data(start_index, end_index, last_n_days, file_list)
        stock_RSI = cal_RSI(all_info)

        for key in sorted(output_data):    
            if len(output_data[key]) == (6 * latest_n_days + 1) and 'NULL' not in output_data[key]: 
                #fw.write(file_list[end_index - i + latest_n_days] + '\t' + key + '\t' + str(output_data[key][0]))
                output_str = ''
                for f in range(1, len(output_data[key])):
                    #print(key, f, output_data[key][f])
                    try:
                        output_str = output_str + '\t' + str(f) + ':' + output_data[key][f]
                    except:
                        output_str = 'none'
                        print(file_list[end_index - i], key, f, output_data[key][f])
                        break
                if output_str != 'none':
                    fw.write(str(output_data[key][0]))
                    fw.write(output_str + '\n')

            data_of_days.pop(0)



