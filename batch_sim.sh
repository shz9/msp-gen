#!/bin/env bash

## Batch directives

#PBS -l walltime=10:00:00
#PBS -l nodes=1:ppn=1,pmem=2gb
#PBS -N gen_msp
#PBS -t 1-10
#PBS -o gen_msp_log/${PBS_JOBID}
#PBS -e gen_msp_log/${PBS_JOBID}

# on Abacus, uncomment the line below for small simulations (under 1k individuals
# with low recombination rate). This will put the job into high proority queue.
# COMMENT_PBS -l qos=short

## Environment setup

# activate the conda environment
source activate msp-gen
# set working directory
cd msp-gen
# prepare output dir
mkdir -p gen_msp_log

## Simulation paramters

# chrsomosome length, in basepairs
CHR=248956422
# reconmbination rate, per base pair per generation
REC=1e-8
# input genealogy file
GEN=cached/genealogy.tsv
# output directory for tree sequences
OUT=example_sim

## Simulate!
python msp_sim_gen.py $GEN $OUT -r $REC -l $CHR -a ${PBS_ARRAYID} --no-provenance

# NB: --no-provenance flag is a temporary work-around. By default, proband info
#     is stored in the tree sequence, which can be a waste of space
