import csv


def run_script():
    """ Main Program """

    # get user sample data choice
    user_input = input('Choose Sample Data Size. OPTIONS (1: 3600, 2: 36000, 3: all)')

    options = {'1': 'data_3600.csv', '2': 'data_36000.csv', '3': 'data_all.csv'}

    # Get csv file from the same directory
    data = options.get(user_input)
    result_strings = ['Trades are:']
    profits= []

    data_list = process_data(data)
    iter_data_list_len = len(data_list) - 29 # subtract 30 minutes for the last valid trade period

    start_index = 0
    while start_index <= iter_data_list_len:
        # Get 59 minutes of data starting from start_index
        # dltp = data_list trading period
        dltp = list(data_list[start_index:start_index+60])

        # sell only from after the 29th minute
        # dltp is less than 30 minutes, do not buy anymore
        if len(dltp[30:]) <= 0:
            break

        buy_price_val, curr_index = buy_price(start_index, data_list)

        sell_price_val, end_index = sell_price(dltp, curr_index)

        profit = sell_price_val - buy_price_val

        # only suggest trades that are not negative
        if profit > 0:
            result = 'Open at {} ({}), Close at {} ({}) for profit {:.4f}'\
                .format(curr_index, buy_price_val, end_index, sell_price_val, round(profit, 4))

            result_strings.append(result)
            profits.append(profit)

        start_index = end_index + 1 # plus 1 for the next data

    for result in result_strings:
        print(result)
    
    print('Total trades made: {}'.format(len(result_strings) - 1))
    print('Total profit is {:.4f}'.format(round(sum(profits), 4)))


def sell_price(dltp, curr_index):
    """Determines when to sell with the most profit with in the 59-minute trading period
    But we are only going to process the last 30 mins since we can only sell from that period

    -- Returns selling price, index of the sell price --
    """

    first_iter = True
    end_index = 0
    highest_price = 0.0

    # start loop from the 30th minute  
    for count, item in dltp[30:]:
        curr_price = float(item)
        if first_iter:
            highest_price = curr_price
            end_index = int(count)
            first_iter = False
        else:
            if curr_price > highest_price:
                highest_price = curr_price
                end_index = int(count)

    # enhancement
    # Add algorithm to take note of trends. 
    
    return highest_price, end_index

def process_data(data):
    """Reads data from CSV, returns a list of tuples (time, price)"""

    data_list = []

    with open(data) as file:
        reader = csv.reader(file)
        next(reader) # skip column name

        count = 1
        
        for row in reader:
            data_list.append(tuple(row))

    return data_list

def buy_price(start_index, data_list):
    """Determines when to buy at the start of the market time or after a sell.

    Checks the lowest price from a group of data to set as as buying price.

    --Returns the buy price and current index--
    """
    
    lowest_price = 0.0
    first_iter = True
    curr_index = start_index

    for count, item in data_list[curr_index:]:
        curr_price = float(item)
        if first_iter:
            lowest_price = curr_price
            curr_index = int(count)
            first_iter = False
        else:
            if curr_price < lowest_price:
                lowest_price = curr_price
                curr_index = int(count)

            elif curr_price > lowest_price:
                # enhancement 
                # insert some sort of algo to check if the current price continues to go down
                # if it continues to go down do not set lower_price yet (the buy price)
                break

    # lowest price will be the buy price 
    return lowest_price, curr_index


run_script()