# White Elephant Simulator

```bash
python3 run_sim.py
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