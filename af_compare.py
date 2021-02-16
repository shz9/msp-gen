import matplotlib.pyplot as plt
import tskit
import sys
import math

wf = tskit.load(sys.argv[1])
ooa = tskit.load(sys.argv[2])

fig, ax = plt.subplots(ncols=1)

afs_wf = wf.allele_frequency_spectrum(
    polarised=False, mode="site", span_normalise=False
)[1 : math.ceil(wf.num_samples / 2)]

afs_ooa = ooa.allele_frequency_spectrum(
    polarised=False, mode="site", span_normalise=False
)[1 : math.ceil(ooa.num_samples / 2)]

plot_args = dict(marker=".", ls="")
ax.plot(afs_wf, label="WF", **plot_args)
ax.plot(afs_ooa, label="OOA", **plot_args)
ax.legend()

ax.set_title("Folded AFS of out-of-Africa vs constant size Wright-Fisher continuation")

fig.savefig(sys.argv[3])
