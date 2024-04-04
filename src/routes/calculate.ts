function americanToDecimalOdds(american_odds: number): number {
    if (american_odds >= 100) {
        return 1 + american_odds / 100
    } else if (american_odds <= -100) {
        return 1 - 100 / american_odds
    }

    throw `Invalid american odds, expected value above 100 or below -100 got ${american_odds}`
}


function hasArbitrage(decimalOdds: number[]): boolean {
    let odds_sum = decimalOdds.map((odd) => 1 / odd).reduce((a, b) => a + b)
    return odds_sum < 1
}


function calculateWeights(decimalOdds): number[] {
    let inv_odds = decimalOdds.map((odd) => 1 / odd)
    let sum_inv_odds = inv_odds.reduce((a, b) => a + b)
    let weights = inv_odds.map((invOdd) => invOdd / sum_inv_odds)
    return weights
}


export function calculateArbitrage(odds: number[]): [boolean, number[], number[]] {
    let decimalOdds = odds.map((odd) => americanToDecimalOdds(odd))
    let isArbitrage = hasArbitrage(decimalOdds)
    let weights = calculateWeights(decimalOdds);

    return [isArbitrage, weights, decimalOdds]
}