import sys
import math

# 10^12
UPPER_LIMIT = 1000000000000


# given a budget, current cost of each stock, and ideal percentage investment of that stock (compare to total budget)
# return a vector of number of shares of each stock to buy that is the closest to the ideal percentage

# e.g.
#
# budget
# current price of stocks
# percentages of total budget
#
# 5000.00
# 117.23 132.13 41.11 32.11 13.12
# .25 .20 .20 .20 .15


def init():
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

    return [budget, stock_cost, stock_percent, expected_cost]


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
