import msprime
import tskit
import sys
from argparse import ArgumentParser
import json
import stdpopsim
import numpy as np


parser = ArgumentParser("sim_complete")

parser.add_argument("input_ts", help="input incomplete tree sequence")
parser.add_argument("output_ts", help="output tree sequence file")
parser.add_argument(
    "-m", "--model", help="Contiuation model", default="DTWF", choices=["DTWF", "OOA"]
)
parser.add_argument("-p", "--population", help="source population")
parser.add_argument(
    "-N",
    "--population-size",
    help="Effective population size, only for DTWF",
    type=int,
    default=1_000,
)

args = parser.parse_args()
ts = tskit.load(args.input_ts)

# read the recombination map from the provenance
provenance = json.loads(ts.provenance(0).record)
ts_recomb_rate = provenance["parameters"]["recombination_rate"]


if args.model == "DTWF":
    sim = msprime.simulate(
        from_ts=ts,
        model="dtwf",
        Ne=args.population_size,
        recombination_rate=ts_recomb_rate,
    )
elif args.model == "OOA":
    tables = ts.dump_tables()
    # add extra populations
    # 0=YRI, 1=CEU and 2=CHB
    tables.populations.add_row()
    tables.populations.add_row()

    # change the population - set all to CEU
    nodes = tables.nodes
    nodes.set_columns(
        time=nodes.time,
        flags=nodes.flags,
        individual=nodes.individual,
        population=np.repeat(1, len(nodes)).astype(np.int32),
        metadata=nodes.metadata,
        metadata_offset=nodes.metadata_offset,
        # metadata_schema=nodes.metadata_schema,
        # Does this mean that the metadata gets drpped here?
        # Though we are not really using it
    )

    ts = tables.tree_sequence()

    population_configurations, migration_matrix, demographic_events = out_of_africa()

    sim = msprime.simulate(
        from_ts=ts,
        model="dtwf",
        population_configurations=population_configurations,
        demographic_events=demographic_events,
        migration_matrix=migration_matrix,
        recombination_rate=ts_recomb_rate,
    )

sim.dump(args.output_ts)
