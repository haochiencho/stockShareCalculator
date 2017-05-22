import sys
import math

# 10^12
UPPER_LIMIT = 1000000000000


# given a budget, current cost of each stock, and ideal percentage investment of that stock (compare to total budget)
# return a vector of number of shares of each stock to buy that is the closest to the ideal percentage

# e.g.
#
# budget
# number of stocks
# percentages
#
# 5000.00
# 117.23 132.13 41.11 32.11 13.12
# .25 .20 .20 .20 .25


def cost_function(budget, expected_cost, current_shares, stock_cost):
    totalCost = 0.0

    n = len(stock_cost)

    for i in range(n):
        totalCost += current_shares[i] * stock_cost[i]

    if budget < totalCost:
        return UPPER_LIMIT
    else:
        totalCost = budget - totalCost

        for i in range(n):
            totalCost += math.fabs(expected_cost[i] - current_shares[i] * stock_cost[i])

    return totalCost


def main():
    budget = 0.0
    stock_cost = []
    stock_percent = []
    expected_cost = []

    line = sys.stdin.readline()
    for el in line.split():
        budget = float(el)

    line = sys.stdin.readline()
    for el in line.split():
        stock_cost.append(float(el))

    line = sys.stdin.readline()
    for el in line.split():
        stock_percent.append(float(el))
        expected_cost.append(budget * float(el))

    n = len(stock_percent)
    shares = [0] * n

    for i in range(n):
        while (shares[i] + 1) *  stock_cost[i] <= expected_cost[i]:
            shares[i] += 1

    curCost = 0.0
    index = 0

    while index != -1:
        index = -1
        curCost = UPPER_LIMIT

        for i in range(n):
            shares[i] += 1
            if cost_function(budget, expected_cost, shares, stock_cost) < curCost:
                index = i
            shares[i] -= 1

        if index != -1:
            shares[index] += 1

    totalInvestment = 0.0
    for i in range(n):
        print(str(shares[i]) + " ")
        totalInvestment += shares[i] * stock_cost[i]

    print("Budget: " + str(budget))
    print("Investment: " + str(totalInvestment))


if __name__ == "__main__":
    main()