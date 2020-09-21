# `msprime` genealogy simulations

This repository contains the driver scripts for genealogical simulations.
For installation instructions, consult [INSTALL.md](./INSTALL.md).

# `msp_sim_gen.py`
<a name="msp_sim_gen"></a>

Main simulation script - simulate genomes of probands on a genealogy, outputting
tree sequences for each replicate.

| Argument                | Required | Type      | Default | Description                                                                                                     |
| --------                | -------- | ----      | ------- | -----------                                                                                                     |
| `genealogy`             | yes      | file      |         | genealogy input table - 3 columns, whitespace-separated. See [genealogy format](#genealogy_format) for details. |
| `output`                | yes      | directory |         | output path.                                                                                                    |
| `--prefix` / `-a`       |          | string    | `""`    | prefix to append to output file. Used in batch jobs.                                                            |
| `--proband-file` / `-p` |          | file      | `None`  | proband IDs, one per line. See [probands](#probands) for details.                                               |
| `--length` / `-l`       |          | int       | `1000`  | length of the genome, in base-pairs                                                                             |
| `--recomb-rate` / `-r`  |          | float     | `0`     | recombination rate, per base pair-pair per generation                                                           |
| `--replicates` / `-n`   |          | int       | `1`     | number of simulation replicates. For running on a cluster, use an array job instead.                            |
| `--no-provenance`       |          | flag      |         | do not record run-specific metadata. Temporary workaround.                                                      |

## Genealogy format
<a name="genealogy_format"></a>

Genealogy is formatted as a table with at least 3 columns:

- `individual` - unique ID of an individual
- `father` - ID of the father
- `mother` - ID of the mother

The only requirements is for the IDs to be unique. See
[balsac.tsv](./data/balsac.tsv) for an example.

Genealogies can also be simulated with [`sim_gen.py`](#sim_gen) script.

## Probands
<a name="probands"></a>

By default, the simulation is initiated for all the individuals that do not have
children. If you have a specific list of proband IDs, pass them in
`--proband-file` argument.

The proband file have one individual ID per line.

# `sim_gen.py`
<a name="sim_gen"></a>

A script to simulate genealogical relationships.

| Argument              | Required | Type  | Default         | Description                                                                                                      |
| --------              | -------- | ----  | -------         | -----------                                                                                                      |
| `founders`            | yes      | int   |                 | number of found individuals in the founder population. Extra individuals will be added to have complete couples. |
| `generations`         | yes      | int   |                 | depth of the genealogy.                                                                                          |
| `--children` / `-c`   |          | float | `2.0`           | average number of children per couple. Mean for a Poisson distribution.                                          |
| `--immigrants` / `-i` |          | float | `2.0`           | average number of new arrivals per generation. Mean for a Poisson distribution.                                  |
| `--seed` / `-s`       |          | int   |                 | seed for the random number generator                                                                             |
| `--no-progress`       |          | flag  |                 | do not display a progress bar                                                                                    |
| `--output` / `-o`     |          | file  | `genealogy.tsv` | output file                                                                                                      |

Note that if the average number of children per generation is insufficient, and
the population dies out, the simulation will stop early, and may not have the
desired number of generations.

# `batch_sim.sh`
<a name="batch_sim"></a>

An array job for simulating replicate chromosomes over a genealogy. The script
sets up the environment ([INSTALL.md](INSTALL.md)) and invokes
[`msp_gen_sim.py`](#msp_gen_sim).

# TODO

[ ] document the functions in the `batch_sim` scripts
[ ] provide input to `batch_sim` as input arguments
