import pandas as pd

cols = [2,3,4,5,6,7,8,9,10,'A']
rows = list(range(17,7,-1))

hard_totals = {
                                                2: ['S']*5 + ['H'] + ['D']*2 + ['H']*2,
                                                3: ['S']*5 + ['H'] + ['D']*3 + ['H']*1,
                                                4: ['S']*6 + ['D']*2 + ['H']*2,
                                                5: ['S']*6 + ['D']*2 + ['H']*2,
                                                6: ['S']*6 + ['D']*2 + ['H']*2,
                                                7: ['S']*1 + ['H']*5 + ['D']*2 + ['H']*2,
                                                8: ['S']*1 + ['H']*5 + ['D']*2 + ['H']*2,
                                                9: ['S']*1 + ['H']*5 + ['D']*2 + ['H']*2,
                                                10:['S']*1 + ['H']*5 + ['D']*1 + ['H']*3,
                                               'A':['S']*1 + ['H']*5 + ['D']*1 + ['H']*3
                                        }
                                       

basic_strategy_hard_totals = {c:{r:hard_totals[c][i] for i, r in enumerate(rows)} for c in cols}

