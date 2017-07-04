#!/usr/bin/python

import sys
import math
from googlefinance import getQuotes

# 10^12
UPPER_LIMIT = 1000000000000

LAST_TRADE_STR = "LastTradePrice"

def init():
    print("Please enter your budget in USD.")
    val = sys.stdin.readline().strip('\n')
    budget = round(float(val), 2)

    stock_cost = []
    stock_percentages = []
    expected_cost = []

    percent_left = 100
    while percent_left != 0:
        print("Please enter the ticker symbol of one of the stocks in this investment.")
        stock_ticker = sys.stdin.readline().strip('\n')

        stock_price = getQuotes(stock_ticker)[0][LAST_TRADE_STR]
        print("The current price of " + stock_ticker + " is: " + stock_price)
        print("Enter a percentage of the investment to allocate to this stock. Percent left: " + str(percent_left))

        stock_percent = round(float(sys.stdin.readline()), 2)
        while stock_percent > percent_left:
            print("Invalid percentage. Please enter a percentage less than or equal to " + str(percent_left) + " for this stock.")
            stock_percent = round(float(sys.stdin.readline()), 2)

        percent_left = round(percent_left - stock_percent, 2)
        stock_cost.append(float(stock_price))
        stock_percentages.append(stock_percent/100)
        expected_cost.append(budget * stock_percent/100)

    print("---------------------------------------")
    return [budget, stock_cost, stock_percentages, expected_cost]


def cost_function(budget, expected_cost, current_shares, stock_cost):
    total_cost = 0.0

    n = len(stock_cost)

    for i in range(n):
        total_cost += current_shares[i] * stock_cost[i]

    if budget < total_cost:
        return UPPER_LIMIT
    else:
        total_cost = budget - total_cost

        for i in range(n):
            total_cost += math.fabs(expected_cost[i] - current_shares[i] * stock_cost[i])

    return total_cost


def main():
    inputs = init()

    budget = inputs[0]
    stock_cost = inputs[1]
    stock_percent = inputs[2]
    expected_cost = inputs[3]

    n = len(stock_percent)
    shares = [0] * n

    for i in range(n):
        while (shares[i] + 1) * stock_cost[i] <= expected_cost[i]:
            shares[i] += 1

    index = 0

    while index != -1:
        index = -1
        min_cost = UPPER_LIMIT

        for i in range(n):
            shares[i] += 1
            cur_cost = cost_function(budget, expected_cost, shares, stock_cost)
            if cur_cost < min_cost:
                min_cost = cur_cost
                index = i
            shares[i] -= 1

        if index != -1:
            shares[index] += 1

    total_investment = 0.0
    for i in range(n):
        print(str(shares[i]) + " ")
        total_investment += shares[i] * stock_cost[i]

    print("Budget: " + str(budget))
    print("Investment: " + str(total_investment))


if __name__ == "__main__":
    main()
