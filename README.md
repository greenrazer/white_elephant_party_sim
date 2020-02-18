# White Elephant Party Paper

## Paper

Read it [here](paper.md)! :)

## Figures

Feel free to use any figures in the figures folder, just credit me.

## Data

The raw data counts for the complete analysis is in `raw.data.json` in the format 
`data[<number of participants>][<number of steals>]` this will return a dict of the `counts` which is the `participant x value of gift` array, and `total` which is a number representing the total amount of outcomes for each participant. To get the percentages divide each entry in `counts` by `total`.

## White Elephant Complete Analysis Script

```bash
python3 src/run_analysis.py
usage: run_analysis.py [-h] [-n NUMBER_OF_PARTICIPANTS] [-m MAX_STEALS]
                       [-s GRAPH_FILE] [-a ANIMATION_FILE]

Run white elephant analysis.

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER_OF_PARTICIPANTS, --number_of_participants NUMBER_OF_PARTICIPANTS
                        Number of participants in simulated white elephant
                        party.
  -m MAX_STEALS, --max_steals MAX_STEALS
                        Maximum steals per present.
  -s GRAPH_FILE, --graph_file GRAPH_FILE
                        Save graph file.
  -a ANIMATION_FILE, --animation_file ANIMATION_FILE
                        Save rotation animation of graph.
```
This will evaluate the whole tree and output com

## White Elephant Simulator Script

```bash
python3 src/run_sim.py
usage: run_sim.py [-h] [-n NUMBER_OF_PARTICIPANTS] [-m MAX_STEALS] [-r RUNS]
                  [-d OUTPUT_DIR]

Run white elephant simuation.

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER_OF_PARTICIPANTS, --number_of_participants NUMBER_OF_PARTICIPANTS
                        Number of participants in simulated white elephant
                        party.
  -m MAX_STEALS, --max_steals MAX_STEALS
                        Maximum steals per present.
  -r RUNS, --runs RUNS  Amount of times to run simulation.
  -d OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output directory to put figures.
```
this will run 1000 white elephant simulations with 100 participants and 2 max steals. 
It will then save two figures in the "--output_dir". 
One with the average raw value of the gifts vs. the position number.
One with the average relative value of the gifts vs. the position number.