import msprime
import tskit
import numpy as np
import sys
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime


def status(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


parser = ArgumentParser("simulate.py")
parser.add_argument("genealogy", help="Genealogy file")
parser.add_argument("output_ts", type=Path, help="Output tree sequence file")
parser.add_argument("--proband-file", "-p", default=None, help="List of probands")
parser.add_argument(
    "--length", "-l", default=1000, type=int, help="Length of chromosome in base-pairs"
)
parser.add_argument(
    "--recomb-rate",
    "-r",
    default=0,
    type=float,
    help="Recombination rate per base-pair per generation",
)

args = parser.parse_args()

clock_start = datetime.now()
status(f"Started at {clock_start}")

status("Reading pedigree file...")
ped = msprime.Pedigree.read_txt(args.genealogy)
status(f"Read pedigree with {ped.num_individuals} individuals...")

if args.proband_file:
    status(f"Using proband file {args.proband_file}...")
    proband_ID = np.loadtxt(args.proband_file, dtype=int)
    sample_size = len(proband_ID)
    ped.set_samples(sample_IDs=proband_ID, probands_only=True)
else:
    status("Finding probands...")
    proband_idx = ped.get_proband_indices()
    sample_size = len(proband_idx)
    ped.set_samples(num_samples=sample_size)
status(f"Using {sample_size} probands...")

t = int(max(ped.time))

sim = msprime.simulate(
    sample_size,
    pedigree=ped,
    model="wf_ped",
    end_time=t,
    length=args.length,
    recombination_rate=args.recomb_rate,
    num_replicates=1,
)

status("Converting tables...")

# record individual id metadata
tables = next(sim).dump_tables()

individual_metadata_schema = tskit.MetadataSchema(
    {
        "codec": "json",
        "type": "object",
        "properties": {
            # Name of the individual in the pedigree file
            "individual_name": {"type": "integer"},
            "is_sample": {"type": "boolean"},
        },
        "required": ["individual_name", "is_sample"],
    }
)
meta_individuals = tskit.IndividualTable()

meta_individuals.metadata_schema = individual_metadata_schema
for i, ind in enumerate(tables.individuals):
    ind_name = int(ped.individual[i]) if i < ped.num_individuals else -1
    is_sample = bool(ped.is_sample[i]) if i < ped.num_individuals else False
    meta_individuals.add_row(
        metadata={"individual_name": ind_name, "is_sample": is_sample},
    )

tables.individuals.set_columns(
    flags=tables.individuals.flags,
    location=tables.individuals.location,
    location_offset=tables.individuals.location_offset,
    metadata=meta_individuals.ll_table.metadata,
    metadata_offset=meta_individuals.ll_table.metadata_offset,
)

tables.individuals.metadata_schema = individual_metadata_schema
tables.tree_sequence().dump(args.output_ts)

clock_stop = datetime.now()
status(f"Done at {clock_stop}")
status(f"Took {clock_stop - clock_start}")
