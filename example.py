import msprime
import tskit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# An example script to simulate over a genealogy and count the number of
# coalescent events

ped = msprime.Pedigree.read_txt("data/balsac.tsv")
rep = 100
probands = ped.get_proband_indices()
ped.set_samples(num_samples=len(probands))

t = int(max(ped.time))
    
replicates = msprime.simulate(len(probands),
                              pedigree=ped,
                              length=1_000_000,
                              recombination_rate=0,
                              model='wf_ped',
                              end_time=t,
                              num_replicates=rep)

coal_times = []
for ts in replicates:
    tb = ts.dump_tables()
    # filter out stop nodes and sample nodes
    mask = ~((tb.nodes.individual == -1) | (tb.nodes.flags == tskit.NODE_IS_SAMPLE))
    coal_times.extend(tb.nodes.time[mask])

counts, bins = np.histogram(coal_times, range(1, t+1))
means = counts / rep
stdev = np.sqrt((counts - means) / (rep - 1))

mpl.style.use('seaborn')
fig, ax = plt.subplots()
ax.bar(bins[:-1], means)
ax.errorbar(bins[:-1], means, stdev, ls="", color="gray")
# ax.set_ylim(0,7)
ax.set(xlabel="Generation",
       ylabel="Effective N times some arbitrary constant",
       title=f"Simulating over publically available BALSAC data, n={rep}")
fig.savefig("example.png", dpi=300)
