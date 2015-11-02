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


if __name__ == '__main__':
    input_file_path = '/home/mlb/res/stock/twse/json/'
    file_list = listdir(input_file_path)
    file_list.sort()
    start_index, end_index, latest_n_days, output_file = process_input(argv[1], argv[2], argv[3], argv[4], file_list)
    data_of_days = []
    ignore_stock_ids = ['id']
    with codecs.open(output_file, 'w') as fw:
        for i in range(latest_n_days):
            data = json.load(codecs.open(input_file_path + file_list[end_index - i], 'r'))
            data_of_days.append(data)
            
        for i in range(latest_n_days, end_index - start_index + latest_n_days + 1):
            data = json.load(codecs.open(input_file_path + file_list[end_index - i], 'r'))
            print(file_list[end_index - i])
            data_of_days.append(data)
            output_data = {}
            for d in range(latest_n_days + 1):
                for key in data_of_days[d]:
                    if d == 0 and key not in ignore_stock_ids:
                        output_data[key] = []
                        try:
                            increase = 0
                            if float(data_of_days[d][key]['close']) > float(data_of_days[d + 1][key]['close']):
                                increase = 1
                            elif float(data_of_days[d][key]['close']) < float(data_of_days[d + 1][key]['close']):
                                increase = -1
                            output_data[key].append(increase)
                        except:
                            continue
                    elif d > 0:
                        if key in output_data:
                            output_data[key].append(data_of_days[d][key]['open'])
                            output_data[key].append(data_of_days[d][key]['close'])
                            output_data[key].append(data_of_days[d][key]['high'])
                            output_data[key].append(data_of_days[d][key]['low'])
                            output_data[key].append(data_of_days[d][key]['volume'])
                            output_data[key].append(data_of_days[d][key]['adj_close'])

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



