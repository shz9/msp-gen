import os
import argparse
import subprocess
import numpy as np
import pandas as pd
import tempfile

import tskit


class Runner:
    def __init__(self, args):
        self.test = args.test
        self.verbose = args.verbose or args.test

    def run(self, cmd):
        prefix = "Running:"
        if self.test:
            prefix = "Testing:"

        if self.verbose:
            print(prefix, cmd)

        if not self.test:
            subprocess.run(cmd, shell=True, check=True)


def ts_to_bcf_single(
    ts_file,
    out_file,
    runner,
    af_cutoff=0,
    keep_sample=None,
    remove_singletons=False,
    use_vcf=False,
):

    ts = tskit.load(ts_file)
    if ts.num_individuals == 0:
        bcf_cmd = "tskit vcf --ploidy 2 {} | bcftools view -O b > {}".format(
            ts_file, out_file
        )
        runner.run(bcf_cmd)
    else:
        # remove sites based on allele frequency cutoff
        sample_nodes = ts.samples()

        if (af_cutoff != 0) or remove_singletons:
            sites_to_delete = []
            for tree in ts.trees():
                for mutation in tree.mutations():
                    # should this be count-1 since the node itself is included?
                    count = tree.num_samples(mutation.node)
                    # note that this is non-polarized frequency ( > 50% possible)
                    if (count / len(sample_nodes)) < af_cutoff:
                        sites_to_delete.append(mutation.site)
                    if remove_singletons and count == 1:
                        sites_to_delete.append(mutation.site)

            # bulk-remove sites
            tables = ts.dump_tables()
            tables.delete_sites(sites_to_delete, record_provenance=False)
            ts = tables.tree_sequence()

        # Obtain a list of the individuals and their nodes:
        node_table = []
        individual_table = []

        for ind in ts.individuals():
            if len(ind.nodes) == 2:
                node_table.extend([{'Node': ind.nodes[i], 'Individual': ind.id} for i in range(2)])
                individual_table.append({'Individual': ind.id, 'IndividualName': ind.metadata["individual_name"]})

        # Construct a dataframe of the nodes:
        node_df = pd.DataFrame(node_table)
        # Construct a dataframe of individuals:
        individual_df = pd.DataFrame(individual_table)

        # Merge with the sampled nodes list:
        merged_df = node_df.merge(pd.DataFrame({'Node': sample_nodes}))
        
        # Count how many times an individual ID occurs in the merged table:
        ind_counts = merged_df['Individual'].value_counts()

        # Keep only individuals that occur twice (i.e. are diploid):
        sample_individuals = list(ind_counts[ind_counts == 2].index)

        final_list = individual_df.merge(pd.DataFrame({'Individual': sample_individuals}))
        final_list['IndividualName'] = final_list['IndividualName'].astype(str)

        if keep_sample is not None:
            final_list = final_list.merge(keep_sample)
        
        sample_names = list(final_list['IndividualName'].values)
        sample_ids = list(final_list['Individual'].values)

        read_fd, write_fd = os.pipe()
        write_pipe = os.fdopen(write_fd, "w")
        with open(out_file, "w") as f:
            output_format = "v" if use_vcf else "b"
            proc = subprocess.Popen(
                ["bcftools", "view", "-O", output_format], stdin=read_fd, stdout=f
            )
            ts.write_vcf(
                write_pipe, individuals=sample_ids, individual_names=sample_names
            )
            write_pipe.close()
            os.close(read_fd)
            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError("bcftools failed with status:", proc.returncode)


def bcf_convert_chrom(bcf_file, chrom_num, runner, use_vcf):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("1\t" + str(chrom_num) + "\n")
        output_format = "v" if use_vcf else "b"
        convert_chrom_cmd = (
            "bcftools annotate --rename-chrs {} {} | "
            "bcftools view -O {} > tmp && mv tmp {} && "
            "rm {}"
        ).format(f.name, bcf_file, output_format, bcf_file, f.name)
        runner.run(convert_chrom_cmd)


def concat_bcf(bcf_files, out_file, runner, use_vcf):
    output_format = "v" if use_vcf else "b"
    concat_chrom_cmd = "bcftools concat -o {} -O {} --threads 2"

    for f in bcf_files:
        concat_chrom_cmd += " " + f

    concat_chrom_cmd = concat_chrom_cmd.format(out_file, output_format)

    runner.run(concat_chrom_cmd)


def main(args):
    out_file = os.path.expanduser(args.out_file)
    runner = Runner(args)

    if args.keep_file is None:
        keep = None
    else:
        try:
            keep = pd.read_csv(args.keep_file, header=None, names=['IndividualName'])
            keep['IndividualName'] = keep['IndividualName'].astype(str)
        except Exception as e:
            print("Failed to read the sample filter file!")
            raise e

    tmp_bcf_files = []
    with tempfile.TemporaryDirectory() as tmpdirname:
        for i, tsf in enumerate(args.ts_file):
            chrom_num = i + 1
            tmp_bcf_file = os.path.join(tmpdirname, ".tmp" + str(i) + ".bcf")
            tmp_bcf_files.append(tmp_bcf_file)

            ts_to_bcf_single(
                tsf,
                tmp_bcf_file,
                runner,
                af_cutoff=args.af_cutoff,
                keep_sample=keep,
                remove_singletons=args.remove_singletons,
                use_vcf=args.use_vcf,
            )
            bcf_convert_chrom(tmp_bcf_file, chrom_num, runner, args.use_vcf)

        concat_bcf(tmp_bcf_files, out_file, runner, args.use_vcf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ts_file", nargs="*")
    parser.add_argument("out_file")
    parser.add_argument(
        "--keep-file",
        type=str,
        default=None,
        dest='keep_file',
        help="A file of individual IDs (with no header) to output to the BCF file.",
    )
    parser.add_argument(
        "-f",
        "--af_cutoff",
        type=float,
        default=0,
        help="Drop sites below this allele frequency cutoff. Default - 0",
    )
    parser.add_argument(
        "-r",
        "--remove-singletons",
        action="store_true",
        help="Drop sites with a single mutation",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-vcf", "--use-vcf", action="store_true")

    parser.add_argument("-T", "--test", action="store_true")

    args = parser.parse_args()

    main(args)
