.PHONY: all prep

all: prep fig/af_compare.png

prep:
	mkdir -p test fig

Ne=10000
length=100000
mu=1e-8
rho=1.5e-8

test/test.ts: data/balsac.tsv simulate.py
	python simulate.py -l ${length} -r ${rho} $< $@

test/test_wf.ts: test/test.ts complete_simulation_wf.py
	python complete_simulation_wf.py -N ${Ne} $< $@

test/test_ooa.ts: test/test.ts complete_simulation_demography.py
	python complete_simulation_demography.py $< $@

test/test_%_mu.ts: test/test_%.ts mutate_tree_sequence.py
	python mutate_tree_sequence.py -u ${mu} $< $@

fig/af_compare.png: test/test_wf_mu.ts test/test_ooa_mu.ts af_compare.py
	python af_compare.py $(filter %.ts,$^) $@

test/test_%_mu.bcf: test/test_%_mu.ts convert_to_bcf.py
	python convert_to_bcf.py $< $@

clean:
	rm -rf test fig
