import msprime
import tskit
from argparse import ArgumentParser
import json
import stdpopsim
import numpy as np


hom_sap = stdpopsim.get_species('HomSap')
model_ids = [model.id for model in hom_sap.demographic_models]

parser = ArgumentParser("complete_simulation_demography")

parser.add_argument("input_ts", help="input incomplete tree sequence")
parser.add_argument("output_ts", help="output tree sequence file")
parser.add_argument(
    "-m", "--model", help="Contiuation model",
    default="OutOfAfrica_2T12", choices=model_ids
)
parser.add_argument("-p", "--population", default='EUR',
                    help="source population")

args = parser.parse_args()
ts = tskit.load(args.input_ts)

model = hom_sap.get_demographic_model(args.model)
pop_ids = [pop.id for pop in model.populations]
if args.population not in pop_ids:
    message = f'''{parser.prog}: error: argument -p/--population: invalid choice: {args.population} (choose from {pop_ids})\n'''
    parser.exit(1, message)

# read the recombination map from the provenance
provenance = json.loads(str(ts.provenance(0).record))
ts_recomb_rate = provenance["parameters"]["recombination_rate"]

tables = ts.dump_tables()
# Add extra populations
for _ in range(model.num_populations - 1):
    tables.populations.add_row()

pop_ids = [pop.id for pop in model.populations]
our_id = pop_ids.index(args.population)

# change the population - set all to CEU
nodes = tables.nodes
nodes.set_columns(
    time=nodes.time,
    flags=nodes.flags,
    individual=nodes.individual,
    population=np.repeat(our_id, len(nodes)).astype(np.int32),
    metadata=nodes.metadata,
    metadata_offset=nodes.metadata_offset,
    # metadata_schema=nodes.metadata_schema,
    # Does this mean that the metadata gets drpped here?
    # Though we are not really using it
)

ts = tables.tree_sequence()

sim = msprime.simulate(
    from_ts=ts,
    model="hudson",
    population_configurations=model.population_configurations,
    demographic_events=model.demographic_events,
    migration_matrix=model.migration_matrix,
    recombination_rate=ts_recomb_rate,
    # TODO Make the replicate interface consistent across scripts
    num_replicates=1
)

next(sim).dump(args.output_ts)
