# Installation

This will walk you through the installation procedure for the development branch
of `msprime` that includes genealogy simulations, and a `conda` setup to install
the environment.

The installation instructions are specific to MUGQIC `abacus` cluster, and may
differ on your system.

## Environment

We use `conda` to install dependencies and manage the environment. If you have
`conda` installed, proceed to the next section.

### `conda` installation

Since `abacus` uses an older version of `python` by default, we use `miniconda2`
to install the environment:

```shell
# download the conda installer
wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh

# run the installer
sh ./Miniconda2-latest-Linux-x86_64.sh
# make sure to run conda init to set your environment variables

# activate conda by running your login script
source ~/.bashrc
```

You should now see `(base)` in your shell prompt, indicating that you are using
the `base` conda environment. Refer to
[https://conda.io/projects/conda/en/latest/user-guide/install/linux.html](these
instructions) if you have issues.

### Create an isolated `conda` environment

This is a good practice for any project. This allows you to get reproducible
environments across different machines, since all the dependencies are local. If
things go wrong with the installation, you can remove everything and start over.

Create the `msp-gen` environment. The name is important, since it used in the
batch script.

```shell
conda create --name msp-gen python=3
```

If you chose a different name for the environment, make sure to also change it in
the script: `./batch_sim.sh:21`.

Now, activate the environment:

```shell
conda activate msp-gen
```

Your shell prompt should not have `(msp-gen)` in it. You can confirm you have the
right `python` executable with `which python` - it should be something like
`~/miniconda2/envs/msp-gen/bin/python`.


### `msprime` dependency installation

`msprime` relies on the `GSL` library for high-performance numerical computation.
This library is not present by default on `abacus`, so we use conda:

```shell
conda install gsl
```

## `msprime` installation

Clone the development version of `msprime` from github:

```shell
git clone https://github.com/tskit-dev/msprime.git --recurse-submodules msprime_dev
```

Now, descend into the `msprime` directory and compile the code:

```shell
cd msprime_dev
make
```

Now, install `msprime` into your `msp-gen` environment:

```shell
python setup.py install
```

## Test simulation

Run a test simulation:

```shell
python msp_sim_gen.py data/balsav.tsv test_sim
```
