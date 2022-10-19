import unittest
import subprocess
import json
import time
import os

class CountDistributionTest(unittest.TestCase):

    def test_one_deck_one_sim_total_count(self):
        decks = 1
        sims = 1 
        pen = 1
        output = 'todostc_results'
        filepath = f'sims/results/{output}'

        self._remove_file(filepath = filepath)
        #run sim script.
        bashcommand = f'python sims/count_distribution.py \
                        -d {decks} \
                        -s {sims} \
                        -o {output}\
                        -p {pen}'
        subprocess.Popen(bashcommand.split())
        
        #allow time for the file to be created before trying to load it.
        time.sleep(1)

        dist = self._load_json_file(filepath = filepath)    
        self._remove_file(filepath = filepath)
        
        self.assertEqual(52, sum(dist.values()))

    def _remove_file(self, filepath):
        #remove test output file if it exists.
        if os.path.exists(filepath):
            os.remove(filepath)

    def _load_json_file(self, filepath) -> dict: 
        with open(filepath) as fh:
            results = json.load(fh)
            return results        

if __name__ =='__main__':
    unittest.main()