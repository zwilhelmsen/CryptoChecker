
"""
CryptoChecker
Zachary Wilhelmsen 03/24/18
This application utilizes cryptocompare web service api to check current prices of desired crypto-currecies.

"""
import urllib.request, json, shelve

def main():
    print('start')

    while True:
        print('What do you want to do? enter help for list of commands.')
        action = input('> ').lower()

        if action in actions.keys():
            exit = actions[action]()
            if exit:
                break
    print('end')

def Exit():
    return True


def Price():
    singleurl = ["https://min-api.cryptocompare.com/data/price?fsym=","&tsyms=USD"]
    multurl = ["https://min-api.cryptocompare.com/data/pricemulti?fsyms=","&tsyms=USD"]
    print("Choose a currency to check from the list.\
    Choose multiple with the format: symbol,symbol,symbol")
    chosen = input("> ").upper()
    symbols = chosen.split(',')
    if len(symbols) > 1:
        with urllib.request.urlopen(multurl[0]+chosen+multurl[1]) as URL:
            data = URL.read().decode('utf-8')
            price = json.loads(data)
            if 'Response' not in price.keys():
                for each in price:
                    print("The price of 1 %s is %s" % (each,price[each]['USD']))
            else:
                print(price['Message'])
    elif len(symbols) == 1:
        with urllib.request.urlopen(singleurl[0]+chosen+singleurl[1]) as URL:
            data = URL.read().decode('utf-8')
            price = json.loads(data)
            if 'Response' not in price.keys():
                print("The price of 1 %s is %s " % (chosen,price['USD']))
            else:
                print(price['Message'])
    return False


def Symbol():
    with shelve.open('list') as coinList:
        # for each in coinList:
            # print(each,coinList[each])
        print('Which coin would you like to check the symbol for?')
        name = input('> ').upper()
        if name.upper() in coinList.keys():
            print('Name = %s, Symbol = %s' % (name,coinList[name]))

        else:
            print('No coin with that name. Refresh list if you are sure.')

    return False


def Help():
    commands = ''
    count = 0
    for each in actions.keys():
        if count > 0:
            commands += ', '
        commands += each.capitalize()
        count += 1
    print(commands)
    return False


def Refresh():
    print("> Starting refresh of list data.")
    print("> Reaching out to server.")
    with urllib.request.urlopen("https://min-api.cryptocompare.com/data/all/coinlist") as URL:
        print("> Contacted server.")
        print("> Sorting Data.")
        data = json.loads(URL.read())
        # print(data.keys())
        coins = shelve.open('list')
        # print(data['Data']['42']['Name'])
        for each in data['Data']:
            if data['Data'][each]:
                    # print(data['Data'][each]['Name'])
                    coins[data['Data'][each]['Name']] = data['Data'][each]['Symbol']
        print('Finished updating list')
    return False



actions = {
        'price'   :   Price,
        'symbol'   :   Symbol,
        'refresh'   :   Refresh,
        'help'   :   Help,
        'exit'   :   Exit,

}

main()