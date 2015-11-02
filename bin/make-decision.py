import codecs
from sys import argv
import json
import operator


def read_predict_result(in_file):
    result = {}
    with codecs.open(argv[1], 'r') as fr:
        index = 0
        header = []
        for row in fr:
            cols = row.strip().split(' ')
            if index == 0:
                header.append(cols[0])
                for c in range(1, len(cols)):
                    result[cols[c]] = {}
                    header.append(cols[c])
                index += 1
            else:
                result[cols[0]][index] = {}
                for c in range(1, len(cols)):
                    result[cols[0]][index][header[c]] = float(cols[c])
                index += 1
    return result


def choose_stocks(result_info):
    stocks = {}
    actions = {'1':'buy', '-1':'short'}
    for act in actions:
        max_p = 0
        chosen_stock = {}
        for stock_id in result_info[act]:
            chosen_stock[stock_id] = result_info[act][stock_id][act]
        if len(chosen_stock) > 0 :
            sorted_stocks = sorted(chosen_stock.items(), key=operator.itemgetter(1), reverse=True)
            stocks[actions[act]] = [sorted_stocks[i][0] for i in range(len(sorted_stocks))]

    return stocks


def make_decision(stocks, predict_stock_list, highest_price, lowest_price):
    decision_table = []
    # load predict-stock-list
    stock_list = json.load(codecs.open(predict_stock_list, 'r'))

    # code, life, type, weight, open_price, close_high_price, close_low_price
    for act in stocks:
        index = 0
        for id in stocks[act]:
            if index  > 2:
                break
            base_price = float(stock_list[str(id)]['close'])
            if base_price <= highest_price and base_price >= lowest_price:
                decision ={}
                decision['"type"'] = '"' + act + '"'
                decision['"code"'] = '"' + stock_list[str(id)]['id'] + '"'
                decision['"weight"'] = str(1)
                decision['"life"'] = str(1)

                if act == 'buy':
                    decision['"open_price"'] = base_price * 0.91
                    decision['"close_high_price"'] = '%.2f'%(decision['"open_price"'] * 1.01)
                    decision['"close_low_price"'] = '%.2f'%(decision['"open_price"'] * 0.99)
                    decision['"open_price"'] = '%.2f'%(decision['"open_price"'])
                elif act == 'short':
                    decision['"open_price"'] = base_price * 0.91
                    decision['"close_high_price"'] = '%.2f'%(decision['"open_price"'] * 1.01)
                    decision['"close_low_price"'] = '%.2f'%(decision['"open_price"'] * 0.99)
                    decision['"open_price"'] = '%.2f'%(decision['"open_price"'])

                decision_table.append(decision)
                index += 1

    return decision_table


def write_decision(decision_table, out_file):
    with codecs.open(out_file, 'w') as fw:
        features = ['"code"', '"type"', '"weight"', '"life"', '"open_price"', '"close_high_price"', '"close_low_price"']
        output_str = []
        for decision in decision_table:
            decision_str = '\t{\n'
            info = []
            for f in features:
                #print(decision[f])
                info.append('\t\t' + f + ': ' + decision[f])
            decision_str = decision_str + (',\n').join(info) + '\n\t}'
            output_str.append(decision_str)
        fw.write('[\n' + (',\n').join(output_str) + '\n]')

if __name__ == '__main__':
    # read predict result
    predict_result = read_predict_result(argv[1])

    # choose stock from the predict result
    bought_stocks = choose_stocks(predict_result)

    # make decision: life, type, weight, open_price, close_high_price, close_low_price
    output_decision = make_decision(bought_stocks, argv[2], 300, 10)

    # output chosen stocks
    write_decision(output_decision, argv[3])
