from itertools import count
from tqdm import tqdm
from numpy import random as rnd
import numpy as np

# SEX: 1 = male, 2 = female
# Individual = ("ID", "father", "mother", "time", "sex")


def simulate_pedigree(n_founders, n_generations,
                      avg_offspring=2,
                      avg_immigrants=2,
                      seed=None,
                      no_progress=True):

    rng = rnd.default_rng(seed)
    current_males, current_females = set(), set()
    next_males, next_females = set(), set()

    ped = []
    id_counter = count(1)

    # assign sex to the founder generation
    for _ in range(n_founders):
        ind_id = next(id_counter)
        male = rng.random() < 0.5
        if male:
            current_males.add(ind_id)
            ped.append((ind_id, 0, 0, n_generations, 1))
        else:
            current_females.add(ind_id)
            ped.append((ind_id, 0, 0, n_generations, 2))

    for t in tqdm(range(n_generations-1, -1, -1), disable=no_progress):
        # pad the arrays if we have uneven sex ratio
        diff = len(current_males) - len(current_females)
        if diff > 0:
            for _ in range(diff):
                ind_id = next(id_counter)
                current_females.add(ind_id)
                ped.append((ind_id, 0, 0, t+1, 2))
        elif diff < 0:
            for _ in range(-diff):
                ind_id = next(id_counter)
                current_males.add(ind_id)
                ped.append((ind_id, 0, 0, t+1, 1))

        # Pick couples
        while len(current_males) and len(current_females):
            # I am assuming that set.pop() returns a random element
            father = current_males.pop()
            mother = current_females.pop()

            n_children = rng.poisson(avg_offspring)

            for ch in range(n_children):
                child_id = next(id_counter)
                child_male = rng.random() < 0.5
                if child_male:
                    next_males.add(child_id)
                    ped.append((child_id, father, mother, t, 1))
                else:
                    next_females.add(child_id)
                    ped.append((child_id, father, mother, t, 2))

        # add extra out-of-family individuals - but not in the present
        if t > 1:
            n_immigrants = rnd.poisson(avg_immigrants)
            for _ in range(n_immigrants):
                ind_id = next(id_counter)
                ind_male = rng.random() < 0.5
                if ind_male:
                    next_males.add(ind_id)
                    ped.append((ind_id, 0, 0, t, 1))
                else:
                    next_females.add(ind_id)
                    ped.append((ind_id, 0, 0, t, 2))

        if not (next_males or next_females):
            raise(RuntimeError('Simulation terminated at time t=' + str(t) +
                               ', (' + str(n_generations-t) +
                               ' generations from founders)'))
        current_males = next_males
        current_females = next_females
        next_males = set()
        next_females = set()

    return np.array(ped)


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("Simulate an extended family genealogy")
    parser.add_argument("founders", type=int,
                        help="Number of founder individuals")
    parser.add_argument("generations", type=int,
                        help="Number of generations to simulate")
    parser.add_argument("--children", "-c", type=float, default=2.0,
                        help="Average number of offspring per family")
    parser.add_argument("--immigrants", "-i", type=float, default=2.0,
                        help="Average number of immigrants per generation")
    parser.add_argument("--seed", "-s", type=int,
                        default=None, help="Random seed")
    parser.add_argument("--no-progress", action="store_true")
    parser.add_argument(
        "--output", "-o", default="genealogy.tsv", help="Output file")
    args = parser.parse_args()

    ped = simulate_pedigree(args.founders, args.generations,
                            avg_offspring=args.children,
                            avg_immigrants=args.immigrants,
                            seed=args.seed,
                            no_progress=args.no_progress)

    np.savetxt(args.output, ped, fmt="%d", delimiter="\t",
               header="individual\tfather\tmother\ttime\tsex")
