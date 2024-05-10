## Blackjack Statistics
A program that runs many simulations of a blackjack game, and outputs relevant statistics. Also includes a GUI to make operating the program more user-friendly.

## Dependencies
To install all required dependencies for this project, run
``` pip install pygame ```
in the folder containing the repository.

## More information
This project is a GUI simulation of a game of blackjack. The game has 3 options: basic strategy, advanced strategy, and advanced strategy with card counting.<br>

Basic strategy: The player holds when their hand is greater than or equal to 17, hits otherwise.<br>
Advanced Strategy: The player's decisions are based off the following probability table (credit: Wikipedia.com)<br><br>
<img width="383" alt="probability-table" src="https://github.com/rebeccaborissova/blackjack-statistics/assets/147621579/aa35a971-bf62-4a03-b910-08276a2dab0d">
<br><br>
Card Counting: The Hi-Low strategy is used to count the cards. High cards, with a value of 17 or greater, are considered "high cards", while cards that are 6 or lower are considered "low cards". When a "low card" goes out, you increase the count by 1, and when a high card goes out, you decrease the count by 1. This "running count" is then used to determine whether the player should bet high or low. <br>
 
<h3>Some statistics calculated using the simulator:</h3>
Chance of player win given the first card and strategy used:<br><br>

<img width = "400" alt="basic-strat-win" src="https://github.com/rebeccaborissova/blackjack-statistics/assets/147621579/842538a3-d698-4714-9779-7c15041b44fd">
<img width = "420" alt = "advanced-strat-win" src="https://github.com/rebeccaborissova/blackjack-statistics/assets/147621579/8681f736-3658-46b0-a38a-df0ce3a8a886">
<br><br>

Final balances based on the strategy used:<br><br>
<img width = "400" alt="basic-strat-balances" src="https://github.com/rebeccaborissova/blackjack-statistics/assets/147621579/1949fbcb-e6a2-4043-91d7-31ca1278a194">
<img width = "400" alt="advanced-strat-balances" src="https://github.com/rebeccaborissova/blackjack-statistics/assets/147621579/103e5df8-6a1b-4b89-a4ea-9141b981ad72">

