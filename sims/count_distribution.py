'''
The purpose of this script is to be able to test the distribution and HI-LOW running counts based on different conditions.

The HI-LOW running count is a method used in black jack for counting cards, it keeps a running track of the high and low cards that have been removed from the deck/shoe.

A high count can increase the odds of a player, playing a perfect game by .5 percent for every true count (running count / decks left in the shoe.)

A low count can adversly decrease the odds of a player by the same amount.

This script is meant to be run in the command line and offers a number of arg options. The script tries to take advantage of the performance benifits gained from using async.
'''

import asyncio
from turtle import pen
from unicodedata import decimal
from numpy import floor
import sys
import time 
from json import dumps
import argparse
import os.path

sys.path.append('/home/kye/Documents/projects_/backjack_lw/blackjack/core_game')
from shuffle import ShuffleDeckLw

#script arguments.
parser = argparse.ArgumentParser(description = 'Running count dist. simulation.')
parser.add_argument('-d', '--decks', help='No of decks in a shoe.')
parser.add_argument('-s', '--sims', help='No of shoes run in a sim.')
parser.add_argument('-o', '--output', help='Name of output file.')
parser.add_argument('-p', '--pen', help='Depth of deck penetration.')
args = parser.parse_args()
vargs = vars(args)

#output results file path.
output_filename = 'rcount_dist_results' if not vargs['output'] else vargs['output'].strip()
results_path = f'/home/kye/Documents/projects_/backjack_lw/sims/results/{output_filename}'

def run_count_sims(shuffler, n_sims, pen) -> dict: 
    '''
    perform a running count simulation, this is a black jack card counting strategy used to keep track 
    of the amount of hi-low cards that have left the shoe. 
    Typically extreme counts (high negatives or high positives) are rare, this should be seen in the resulting simulation.

    To perform a simulation pass though an instantiated shuffler and the amount of rounds you want to simulate.

    This fucntion calls another function, it does so to take advantage of async. 
    '''
    return asyncio.run(_build_asyncio_tasks(shuffler, n_sims, pen))

    
async def _build_asyncio_tasks(shuffler, n_sims, pen):
    '''This function build the iterable async task to be executed in parallel.'''
    tasks = []
    for _ in range(n_sims):
        tasks.append( 
                asyncio.create_task(
                                #function _count_shoe_sim actually deals the deck and counts the hand.
                                _count_shoe_sim(shuffler(), shuffler.shoe, pen) 
                                )
                    )

    results =  await asyncio.gather(*tasks)
    final_results = {}
    
    for r in results:
        for key,value in  r.items():
            try:
                final_results[key] += value
            except KeyError:
                final_results[key] = value 
   
    return final_results
    

async def _count_shoe_sim(deck, shoe, pen):
    '''Performs the indivual tasks work of calculating a shoes rc frequency.'''
    tic = time.perf_counter()
    running_count = 0 
    results = {}
    if not pen: pen = .8

    for dealt, c in enumerate(deck):
        
        shoe -= 1 
        if dealt >= (dealt + shoe) * pen:
            toc = time.perf_counter()
            return results
       
        if isinstance(c,int) and c < 7:
            running_count += 1
       
        elif not isinstance(c,int) or c == 10:
            running_count -= 1
      
        decks = (shoe / 52)
        rc =  1 if running_count == 0 else abs(running_count) 
        tc = int(floor(rc / decks ))
        tc = tc*-1 if running_count <0 else tc 
        try:
            results[tc] += 1
        except KeyError:
            results[tc] = 1


#Run the simulation based on passed args.
pen = round(float(vargs['pen']),2) if vargs['pen'] else None
shuffler = ShuffleDeckLw(decks = int(vargs['decks']) )
results = dumps(
            run_count_sims(
                        shuffler = shuffler, 
                        n_sims = int(vargs['sims']),
                        pen = pen
                        )
                )

#Output results to a file, if the file exists append the results. 
if os.path.exists(results_path): 
    m = 'a'
    results = '\n' + results
else:
    m = 'w'
with open(results_path, m) as f:
    f.write(results)
