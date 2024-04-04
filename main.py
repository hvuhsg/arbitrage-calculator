def american_to_decimal_odds(american_odds):
    if american_odds >= 100:
        return 1+american_odds/100
    elif american_odds <= -100:
        return 1-100/american_odds
    else:
        raise ValueError(f"Invalid american odds, expected value above 100 or below -100 got {american_odds}")

def has_arbitrage(decimal_odds):
    odds_sum = sum([1/odd for odd in decimal_odds])
    return odds_sum < 1

def calc_weights(decimal_odds):
    inv_odds = [1/odd for odd in decimal_odds]
    sum_inv_odds = sum(inv_odds)
    weights = [inv_odd / sum_inv_odds for inv_odd in inv_odds]
    return weights

event1_odds = +200
event2_odds = +180
event3_odds = -280
stake = 100

odds = [event1_odds, event2_odds, event3_odds]
decimal_odds = [american_to_decimal_odds(odd) for odd in odds]
weights = calc_weights(decimal_odds)
make = round(stake*weights[0]*decimal_odds[0], 2)

if has_arbitrage(decimal_odds):
    print("Aribtrage found!")
    print(f"If you bet {stake}$ you are expected to make {abs(stake - make)}$")
else:
    print("Aribtrage not found!")
    print(f"If you bet {stake}$ you are expected to lose {abs(stake - make)}$")