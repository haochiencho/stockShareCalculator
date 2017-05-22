//
//  main.cpp
//  Training
//
//  Created by Brian Cho on 4/14/17.
//  Copyright © 2017 Cho. All rights reserved.
//

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <math.h>
#include <algorithm>
#include <list>
#include <stack>
#include <queue>
#include <cmath>

using namespace std;

double costFunction(double budget, vector<double> & expectedCosts, vector<int> & currentShares, vector<double> & stockCosts);


// given a budget, current cost of each stock, and ideal percentage investment of that stock (compare to total budget)
// return a vector of number of shares of each stock to buy that is the closest to the ideal percentage

/*
 
budget
number of stocks
costs
percentages
 
e.g.

5000.00
5
117.23 132.13 41.11 32.11 13.12
.25 .20 .20 .20 .25
 
 */


int main() {
  double budget;
  cin >> budget;
  
  int n;
  cin >> n;
  
  vector<double> stockCosts(n);
  vector<double> stockPercent(n);
  vector<double> expectedCosts(n);
  
  for(int i = 0; i < n; i++) {
    cin >> stockCosts[i];
  }
  
  for(int i = 0; i < n; i++) {
    cin >> stockPercent[i];
    expectedCosts[i] = budget * stockPercent[i];
  }
  
  vector<int> shares(n, 0);

  for(int i = 0; i < n; i++) {
    while((shares[i] + 1) * stockCosts[i] <= expectedCosts[i]) {
      shares[i]++;
    }
  }
  
  int index = 0;
  
  while(index != -1) {
    index = -1;
    double minCost = INT_MAX;
    
    for(int i = 0; i < n; i++) {
      shares[i]++;
      double curCost = costFunction(budget, expectedCosts, shares, stockCosts);
      if(curCost < minCost) {
        minCost = curCost;
        index = i;
      }
      shares[i]--;
    }
    
    if(index != -1)
      shares[index]++;
  }
  
  double totalInvestment = 0;
  for(int i = 0; i < n; i++) {
    cout << shares[i] << " ";
    totalInvestment += shares[i] * stockCosts[i];
  }

  cout << endl << "Budget: " << budget;
  cout << endl << "Investment: " << totalInvestment << endl;
  
}

double costFunction(double budget, vector<double> & expectedCosts, vector<int> & currentShares, vector<double> & stockCosts) {
  double totalCost = 0;
  
  int n = stockCosts.size();
  for(int i = 0; i < n; i++) {
    totalCost += currentShares[i] * stockCosts[i];
  }
  
  if(budget < totalCost) {
    return INT_MAX;
  } else {
    totalCost = budget - totalCost;
    
    for(int i = 0; i < n; i++) {
      totalCost += abs(expectedCosts[i] - currentShares[i] * stockCosts[i]);
    }
  }
  
  return totalCost;
}
