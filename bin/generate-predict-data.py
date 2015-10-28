from os import listdir
from sys import argv
from datetime import datetime as dt
import datetime
import codecs
import json


def process_input(predict_day_str, pre_days_str, predict_data, predict_stock_list, files):
    #[predict-data(YYYY-MM-DD)] [latest n days] [predict-data] [predict-stock-list]
    while predict_day_str + '.json' not in files:
        date_object = dt.strptime(predict_day_str, '%Y-%m-%d') - datetime.timedelta(days = 1)
        predict_day_str = date_object.strftime('%Y-%m-%d')
    start = files.index(predict_day_str + '.json')

    pre_days = int(pre_days_str)

    return start, pre_days, predict_data, predict_stock_list


if __name__ == '__main__':
    input_file_path = '/home/mlb/res/stock/twse/json/'
    file_list = listdir(input_file_path)
    file_list.sort()
    print("Input parsing")
    start_day_index, latest_n_days, predict_data_file, predict_stock_list_file = process_input(argv[1], argv[2], argv[3], argv[4], file_list)
    
    print("Predict data generating")
    data_of_days = []
    ignore_stock_ids = ['id']
    with codecs.open(predict_data_file, 'w') as fw:
        for i in range(latest_n_days):
            data = json.load(codecs.open(input_file_path + file_list[start_day_index - i], 'r'))
            data_of_days.append(data)
        
        print("Data loading finish")
        predict_data = {}
        stock_list = {}
        feature_list = ['open', 'close', 'high', 'low', 'volume', 'adj_close']
        for data in data_of_days:
            for key in data:
                if key not in ignore_stock_ids:
                    if key not in predict_data:
                        predict_data[key] = []
                        predict_data[key].append(0)
                        stock_list[key] = {}
                        stock_list[key]['open'] = data[key]['open']
                        stock_list[key]['close'] = data[key]['close']
                    for f in feature_list:
                        predict_data[key].append(data[key][f])

        output_stock_list = {}
        index = 0
        for key in sorted(predict_data):
            if len(predict_data[key]) == (6 * latest_n_days + 1) and 'NULL' not in predict_data[key]:
                #fw.write(file_list[end_index - i + latest_n_days] + '\t' + key + '\t' + str(output_data[key][0]))

                output_str = ''
                for f in range(1, len(predict_data[key])):
                    #print(key, f, output_data[key][f])
                    try:
                        output_str = output_str + '\t' + str(f) + ':' + predict_data[key][f]
                    except:
                        output_str = 'error'
                        print(key, f, predict_data[key][f])
                        break

                if output_str != 'error':
                    fw.write(str(predict_data[key][0]) + output_str + '\n')
                    output_stock_list[index] = {}
                    output_stock_list[index]['id'] = key
                    output_stock_list[index]['open'] = stock_list[key]['open']
                    output_stock_list[index]['close'] = stock_list[key]['close']

    with open(predict_stock_list_file, 'w') as fw:
        json.dump(stock_list, fw)
