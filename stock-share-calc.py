#!/usr/bin/python

import sys
import math
from googlefinance import getQuotes

# 10^12
UPPER_LIMIT = 1000000000000

LAST_TRADE_STR = "LastTradePrice" # from googlefinance API

class Stock:
    def __init__(self, stock_ticker, stock_price, stock_percent, budget):
        self.ticker = stock_ticker
        self.price = stock_price
        self.percent = stock_percent/100
        self.expected_investment = budget * self.percent

class InvestmentInfo:
    def __init__(self):
        print("*** Please enter your budget in USD. ***")
        val = sys.stdin.readline().strip('\n')

        self.budget = round(float(val), 2)
        self.stocks = []

        percent_left = 100
        while percent_left != 0:
            print("*** Please enter a ticker symbol. ***")
            stock_ticker = sys.stdin.readline().strip('\n')

            stock_price = round(float(getQuotes(stock_ticker)[0][LAST_TRADE_STR]), 2)
            print("The current price of " + stock_ticker + " is: $" + str(stock_price))
            print("*** Enter a percentage of the investment to allocate to this stock. Percent left: " + str(percent_left) + "% ***")

            stock_percent = round(float(sys.stdin.readline()), 2)
            while stock_percent > percent_left:
                print("*** Invalid percentage. Please enter a percentage less than or equal to " + str(percent_left) + "% for this stock. ***")
                stock_percent = round(float(sys.stdin.readline()), 2)

            percent_left = round(percent_left - stock_percent, 2)
            self.stocks.append(Stock(stock_ticker, stock_price, stock_percent, self.budget))

        print("---------------------------------------")


def cost_function(investment_info, current_shares):
    total_cost = 0.0
    n = len(investment_info.stocks)

    for i in range(n):
        total_cost += current_shares[i] * investment_info.stocks[i].price

    if investment_info.budget < total_cost:
        return UPPER_LIMIT
    else:
        total_cost = investment_info.budget - total_cost
        for i in range(n):
            stock = investment_info.stocks[i]
            total_cost += math.fabs(stock.expected_investment - current_shares[i] * stock.price)

    return total_cost

def compute_ideal_breakdown(investment_info):
    n = len(investment_info.stocks)
    shares = [0] * n
    for i in range(n):
        stock = investment_info.stocks[i]
        while (shares[i] + 1) * stock.price <= stock.expected_investment:
            shares[i] += 1

    index = 0
    while index != -1:
        index = -1
        min_cost = UPPER_LIMIT

        for i in range(n):
            shares[i] += 1
            curr_cost = cost_function(investment_info, shares)
            if curr_cost < min_cost:
                min_cost = curr_cost
                index = i

            shares[i] -= 1

        if index != -1:
            shares[index] += 1

    return shares

def main():
    investment_info = InvestmentInfo()
    shares = compute_ideal_breakdown(investment_info)

    final_investment = 0.0
    print("*** INVESTMENT BREAKDOWN ***")

    for i in range(len(shares)):
        stock = investment_info.stocks[i]
        print(stock.ticker + " --- " + str(shares[i]) + (" share" if shares[i] == 1 else " shares"))
        final_investment += shares[i] * stock.price

    print("Budget: $" + str(investment_info.budget))
    print("Investment: $" + str(final_investment))
    print("---------------------------------------")

if __name__ == "__main__":
    main()
