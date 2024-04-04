<script lang="ts">
	import Trash from 'lucide-svelte/icons/trash-2';

	import * as Card from '$lib/components/ui/card';
	import * as Table from '$lib/components/ui/table/index.js';
	import { Button } from '$lib/components/ui/button';
	import { Label } from '$lib/components/ui/label';
	import { Input } from '$lib/components/ui/input';

	import { calculateArbitrage } from './calculate';

	let bets = [];
	let odds: number[] = [];
	let stakeStr: string;
	let stake: number;
	$: stake = parseFloat(stakeStr);
	$: if (hasArbitrage != 'null') {
		calculate(odds, stake);
	}

	let canCalculate: boolean = false;
	$: canCalculate = stake && stake > 0 && odds.length >= 2 && validOdds(odds);
	let hasArbitrage: 'true' | 'false' | 'null' = 'null';
	let make: number;

	function validOdds(odds): boolean {
		if (odds.length < 2) {
			return false;
		}
		return (
			odds.map((odd) => (odd >= 100 || odd <= -100 ? 1 : 0)).reduce((a, b) => (a & b ? 1 : 0)) == 1
		);
	}

	function oddUpdated(event: Event, index: number) {
		let input = event.target as HTMLInputElement;
		let value = input.valueAsNumber;

		if (isNaN(value)) {
			value = 0;
		}

		odds[index] = value;
		odds = odds;
	}

	function onBetAdded(event: Event) {
		let input = event.target as HTMLInputElement;
		let value = input.valueAsNumber;
		input.value = '';
		odds = [...odds, value];
	}

	function removeOdd(index: number) {
		odds = odds.filter((_, i) => i != index);
	}

	function calculate(betOdds: number[], stake: number) {
		let [isArbitrage, weights, decimalOdds] = calculateArbitrage(betOdds);
		hasArbitrage = isArbitrage ? 'true' : 'false';
		make = stake * weights[0] * decimalOdds[0];
		bets = weights.map((w, index) => {
			return {
				odds: betOdds[index],
				stake: stake * w,
				payout: stake * w * decimalOdds[index]
			};
		});
	}
</script>

<main class="flex flex-col items-center justify-center">
	<!-- Input -->
	<section class="flex w-full h-full items-center justify-center p-4">
		<Card.Root class="max-w-[430px] w-full">
			<Card.Header>
				<Card.Title>Arbitrage Calculator</Card.Title>
				<Card.Description>Calculate arbitrage on bets</Card.Description>
			</Card.Header>
			<Card.Content>
				<div class="flex flex-col gap-1 space-y-2">
					<h4 class="text-sm font-medium">Enter Odds</h4>
					{#each odds as odd, i}
						<div class="flex items-center gap-2">
							<Input type="number" value={odd} on:change={(e) => oddUpdated(e, i)} />
							<Button variant="outline" on:click={() => removeOdd(i)}>
								<Trash class="h-4 w-4" />
							</Button>
						</div>
					{/each}
					<Input type="number" placeholder="Enter new odds" on:change={onBetAdded} />
				</div>
			</Card.Content>
			<Card.Footer class="flex w-full flex-col gap-1 space-y-2">
				<div class="w-full space-y-2">
					<Label for="stake">Stake</Label>
					<Input
						id="stake"
						type="number"
						placeholder="How much are you staking?"
						bind:value={stakeStr}
					/>
				</div>
				<Button
					class="w-full {hasArbitrage == 'true' ? 'bg-emerald-600' : ''} {hasArbitrage == 'false'
						? 'bg-red-700'
						: ''}"
					disabled={!canCalculate}
					on:click={() => calculate(odds, stake)}
				>
					{#if hasArbitrage == 'true'}
						Arbitrage found!
					{:else if hasArbitrage == 'false'}
						Arbitrage not found!
					{:else}
						Calculate
					{/if}
				</Button>
			</Card.Footer>
		</Card.Root>
	</section>

	<!-- Result -->
	<section class="w-full h-full p-4">
		{#if hasArbitrage != 'null'}
			<div class="flex flex-col md:flex-row gap-4">
				<div class="flex-[3]">
					<Card.Root class="h-full">
						<Card.Header>
							<p class="font-bold">Arbitrage results</p>
						</Card.Header>
						<Card.Content>
							<Table.Root>
								<Table.Caption>A list of your bets and how much to bet on each one.</Table.Caption>
								<Table.Header>
									<Table.Row>
										<Table.Head class="w-[100px]">Bet</Table.Head>
										<Table.Head>Odds</Table.Head>
										<Table.Head>Stake</Table.Head>
										<Table.Head>Payout</Table.Head>
									</Table.Row>
								</Table.Header>
								<Table.Body>
									{#each bets as bet, i (i)}
										<Table.Row>
											<Table.Cell class="font-medium">#{i}</Table.Cell>
											<Table.Cell>{bet.odds}</Table.Cell>
											<Table.Cell>{bet.stake.toFixed(2)}$</Table.Cell>
											<Table.Cell>{bet.payout.toFixed(2)}$</Table.Cell>
										</Table.Row>
									{/each}
								</Table.Body>
							</Table.Root>
						</Card.Content>
					</Card.Root>
				</div>
				<div class="flex-[2] flex flex-col gap-4">
					<Card.Root>
						<Card.Header>
							<p>You Bet</p>
						</Card.Header>
						<Card.Content>
							<p class="text-3xl">
								{stake.toFixed(2)}$
							</p>
						</Card.Content>
					</Card.Root>
					<Card.Root>
						<Card.Header>
							<p>You Get</p>
						</Card.Header>
						<Card.Content>
							<p class="text-3xl">
								{make.toFixed(2)}$
							</p>
						</Card.Content>
					</Card.Root>
					<Card.Root>
						<Card.Header>
							<p>ROI %</p>
						</Card.Header>
						<Card.Content>
							<p class="text-3xl">
								{((100 / stake) * (make - stake)).toFixed(2)}%
							</p>
						</Card.Content>
					</Card.Root>
				</div>
			</div>
		{/if}
	</section>
</main>
