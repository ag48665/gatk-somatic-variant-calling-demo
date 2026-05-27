import argparse
import subprocess
import yaml

from .commands import bwa_mem, minimap2_align, samtools_index, mutect2, filter_mutect_calls, ensure_output_paths


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_commands(config: dict) -> list[str]:
    paths = ensure_output_paths(config["output_dir"])
    ref = config["reference"]
    threads = int(config.get("threads", 4))
    aligner = config.get("aligner", "bwa")
    tumor = config["samples"]["tumor"]
    normal = config["samples"]["normal"]
    align = bwa_mem if aligner == "bwa" else minimap2_align
    return [
        f"mkdir -p {config['output_dir']}/bam {config['output_dir']}/variants",
        align(ref, tumor["r1"], tumor["r2"], paths["tumor_bam"], threads),
        samtools_index(paths["tumor_bam"]),
        align(ref, normal["r1"], normal["r2"], paths["normal_bam"], threads),
        samtools_index(paths["normal_bam"]),
        mutect2(ref, paths["tumor_bam"], paths["normal_bam"], tumor["name"], normal["name"], paths["unfiltered_vcf"]),
        filter_mutect_calls(ref, paths["unfiltered_vcf"], paths["filtered_vcf"]),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a tumor-normal somatic variant calling workflow.")
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--config", required=True)
    run_parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = load_config(args.config)
    for command in build_commands(config):
        print(f"[somatic-pipeline] {command}")
        if not args.dry_run:
            subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    main()
