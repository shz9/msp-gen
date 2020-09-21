#!/bin/env bash

#COMMENT_PBS -l qos=short

#PBS -l walltime=10:00:00
#PBS -l nodes=1:ppn=1,pmem=2gb
#PBS -N gen_msp
#PBS -t 1-10

source activate msp-gen
cd msp-gen

CHR=248956422
REC=1e-8
GEN=cached/genealogy.tsv
OUT=example_sim

python msp_sim_gen.py $GEN $OUT -r $REC -l $CHR -a ${PBS_ARRAYID} --no-provenance
