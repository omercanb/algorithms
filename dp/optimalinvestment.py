
def optimal_return(num_investments, num_years, f1, f2, returns, starting_money):
    dp = [[0 for _ in range(num_investments)] for _ in range(num_years)]
    for investment in range(num_investments):
        dp[0][investment] = returns[0][investment] * starting_money
    for year in range(1, num_years):
        for curr_investment in range(num_investments):
            best_curr_investment_value = 0
            for prev_investment in range(num_investments):
                fee = f1 if curr_investment == prev_investment else f2
                possible_val = (dp[year - 1][prev_investment] - fee) * returns[year][curr_investment]
                if possible_val > best_curr_investment_value:
                    best_curr_investment_value = possible_val
            dp[year][curr_investment] = best_curr_investment_value
    return max(dp[num_investments - 1])
