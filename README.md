# `msprime` genealogy simulations

This repository contains the driver scripts for genealogical simulations.
For installation instructions, consult [INSTALL.md](./INSTALL.md).

# `simulate.py`
<a name="simulate"></a>

Main simulation script - simulate genomes of probands on a genealogy, and
output a single tree sequence.

| Argument                | Required | Type      | Default | Description                                                                                                     |
|-------------------------|----------|-----------|---------|-----------------------------------------------------------------------------------------------------------------|
| `genealogy`             | yes      | file      |         | genealogy input table - 3 columns, whitespace-separated. See [genealogy format](#genealogy_format) for details. |
| `output`                | yes      | directory |         | output tree sequence.                                                                                           |
| `--proband-file` / `-p` |          | file      | `None`  | proband IDs, one per line. See [probands](#probands) for details.                                               |
| `--length` / `-l`       |          | int       | `1000`  | length of the genome, in base-pairs                                                                             |
| `--recomb-rate` / `-r`  |          | float     | `0`     | recombination rate, per base pair-pair per generation                                                           |

# `complete_simulation_demography.py`
<a name="complete_simulation_demography"></a>

Continue a simulation of a tree sequence until a common ancestor with a
demographic history. This is usually used on the output of
[`simulate.py`](#simulate).

We are using the `stdpopsim` library to specify the demographic models. See the
[catalogue](https://stdpopsim.readthedocs.io/en/latest/catalog.html#sec_catalog_HomSap)
for more.

You can run `python complete_simulation_demography.py --help` to see the available options, including the models.

| Argument                | Required | Type               | Default            | Description                                                     |
|-------------------------|----------|--------------------|--------------------|-----------------------------------------------------------------|
| `input_ts`              | yes      | tree sequence file |                    | An input tree sequence file to initialize the simulation        |
| `output_ts`             | yes      | tree sequence file |                    | Name of the output file                                         |
| `--model` / `-m`        |          | string             | `OutOfAfrica_2T12` | The name of the demographic model from the `stdpopsim` library. |
| `--population` / `-p`   |          | string             | `EUR`              | The label of the population to simulate.                        |
| `--no-citations` / `-q` |          | flag               |                    | Suppress the citation output                                    |


# `complete_simulation_wf.py`
<a name="complete_simulation_wf"></a>

Continue a simulation of a tree sequence until a common ancestor with a
Wright-Fisher model of constant population size. This is usually used on the output of
[`simulate.py`](#simulate).

| Argument                   | Required | Type               | Default | Description                                                |
|----------------------------|----------|--------------------|---------|------------------------------------------------------------|
| `input_ts`                 | yes      | tree sequence file |         | An input tree sequence file to initialize the simulation   |
| `output_ts`                | yes      | tree sequence file |         | Name of the output file                                    |
| `--population-size` / `-N` |          | int                | `10000` | The effective population of the Wright-Fisher model to use |

# `mutate_tree_sequence.py`
<a name="mutate_tree_sequence"></a>

Use this script to overlay mutations on a tree sequence.

| Argument                 | Required | Type               | Default | Description                                          |
|--------------------------|----------|--------------------|---------|------------------------------------------------------|
| `input_ts`               | yes      | tree sequence file |         | An input tree sequence file to overlay the mutations |
| `output_ts`              | yes      | tree sequence file |         | Name of the output file                              |
| `--mutation-rate` / `-u` |          | float              | `1e-8`  | Mutation rate (forward only)                         |

# `convert_to_bcf.py`
<a name="convert_to_bcf"></a>

Use this to convert a mutated tree sequence into a BCF/VCF file. There are
additional options to remove alleles below a frequency threshold and to
randomly subsample individuals.

Note that `bcftools` installation is required to run this script.

| Argument                     | Required | Type               | Default | Description                                                            |
|------------------------------|----------|--------------------|---------|------------------------------------------------------------------------|
| `input_ts`                   | yes      | tree sequence file |         | An input tree sequence                                                 |
| `output`                     | yes      | bcf or vcf file    |         | Name of the output file                                                |
| `--n_subsample` / `-s`       |          | int                | all     | Randomly select some of the individuals from the tree sequence         |
| `--af_cutoff` / `-f`         |          | float              | 0       | Remove any variants that have in-sample frequency below this threshold |
| `--remove_singletons` / `-r` |          | flag               |         | Remove all the singletons from the output                              |
| `--use_vcf` / `-vcf`         |          | flag               |         | Use uncompressed output (`bcftool -O v` option)                        |
| `--verbose` / `-v`           |          | flag               |         | Show `bcftools` commands that are used                                 |


## Genealogy format
<a name="genealogy_format"></a>

Genealogy is formatted as a table with at least 3 columns:

- `individual` - unique ID of an individual
- `father` - ID of the father
- `mother` - ID of the mother

The only requirements is for the IDs to be unique. See
[balsac.tsv](./data/balsac.tsv) or [simple.tsv](./data/simple.tsv) for examples.

Simulated genealogies can also be created with [`create_genealogy.py`](#create_genealogy) script.

## Probands
<a name="probands"></a>

By default, the simulation is initiated for all the individuals that do not have
children. If you have a specific list of proband IDs, pass them in
`--proband-file` argument.

The proband file have one individual ID per line.

# `create_genealogy.py`
<a name="create_genealogy"></a>

A script to simulate genealogical relationships.

| Argument              | Required | Type  | Default         | Description                                                                                                      |
|-----------------------|----------|-------|-----------------|------------------------------------------------------------------------------------------------------------------|
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

An array job for simulating a chromosome over a genealogy. The script sets up
the environment ([INSTALL.md](INSTALL.md)) and invokes [`simulate.py`](#simulate).

# TODO

- [ ] document the functions in the `batch_sim` scripts
- [ ] provide input to `batch_sim` as input arguments
