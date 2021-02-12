# Installation

This will walk you through the installation procedure for the development branch
of `msprime` that includes genealogy simulations, and a `conda` setup to install
the environment.

The installation instructions are specific to MUGQIC `abacus` cluster, and may
differ on your system.

# Environment

We use `conda` to install dependencies and manage the environment. If you have
`conda` installed, proceed to the next section.

Alternatively, you can use `virtualenv`, as long as you can install the `gsl`
library dependency. Note that this is not a python dependency, which is why
`conda` is preferred. In addition, the batch scripts assume that a `conda`
environment has been set up.

## Option 1 - `conda` installation

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
[these instructions](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html)
if you have issues.

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

Your shell prompt should now have `(msp-gen)` in it. You can confirm you have the
right `python` executable with `which python` - it should be something like
`~/miniconda2/envs/msp-gen/bin/python`.

## Option 2 - `virtualenv`


### `msprime` dependency installation

`msprime` relies on the `GSL` library for high-performance numerical computation.

#### With `conda`

This library is not present by default on `abacus`, so we use conda:

```shell
conda install gsl
```

#### Other

Of you have access to a system package manager, there is an excellent change `gsl` is available:

```shell
sudo apt install gsl-devel
```

# Python dependencies - `msprime` and `stdpopsim`

The python packages can be installed with `pip`:

```shell
pip install -r requirements.txt
```

Note that we are presently using the `git HEAD` of `msprime`. This will change in the near future.

# Test simulation

Run a test simulation:

```shell
python simulate.py data/balsav.tsv test_sim
```
