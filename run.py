from nachos.data.Input import TSVLoader
from nachos.constraints import build_constraints
from nachos.similarity_functions import build_similarity_functions as build_sims
from nachos.splitters import build_splitter
import yaml


def main():
    config = yaml.safe_load(open("config.yaml"))
    splitter = build_splitter(config)
    config = yaml.safe_load(open("test/fixtures/connected_test_constraints.yaml"))
    connected_eg = TSVLoader.load("test/fixtures/connected_fraction_constraints.tsv", config)
    split, scores = splitter(connected_eg)
    for idx_s, s in enumerate(split):
        constraint_stats = splitter.constraint_fn.stats(connected_eg, s)
        print(f'Split {idx_s}: {constraint_stats}')
    test_sets = connected_eg.make_overlapping_test_sets(split)
    for idx_s, s in enumerate(test_sets):
        if len(test_sets[s]) > 0:
            constraint_stats = splitter.constraint_fn.stats(connected_eg, test_sets[s])
            print(f'Split {idx_s+2}: {constraint_stats}')
        else:
            print(f'Split {idx_s+2}: length = 0')
    sets = {}
    sets[0] = split[0]
    sets[1] = split[1]
    for i in range(2, len(test_sets)+2):
        sets[i] = test_sets[i-2]
    for i in range(0, len(sets)):
        for j in range(0, len(sets)):
            if i != j and len(sets[i]) > 0 and len(sets[j]) > 0:
                overlap_stats = connected_eg.overlap_stats(sets[i], sets[j])
                print(f'{j} overlap with {i}: {overlap_stats}')


if __name__ == "__main__":
    main()
