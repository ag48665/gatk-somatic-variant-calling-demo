# Tumor–Normal Somatic Variant Calling Pipeline

![Python tests](https://github.com/ag48665/gatk-somatic-variant-calling-demo/actions/workflows/tests.yml/badge.svg)

![Python tests](https://github.com/ag48665/gatk-somatic-variant-calling-demo/actions/workflows/tests.yml/badge.svg)

This repository demonstrates practical skills in:

- Python pipeline orchestration
- BWA and minimap2 read alignment
- samtools BAM sorting and indexing
- GATK Mutect2 tumor-normal somatic variant calling
- VCF filtering and summarization
- optional C++ utility for fast VCF filtering

## Why this project

Somatic variant calling is a common workflow in cancer genomics. This project shows how paired tumor-normal sequencing data can be aligned, processed, and analyzed to produce filtered candidate SNVs and indels.

It is designed as a small but realistic example of the type of work performed in genomics teams at universities, hospitals, biotech companies, and research institutes.

## Public-data angle

The workflow is compatible with public educational datasets from U.S.-based genomics resources such as:

- Broad Institute / GATK public tutorial data
- NIH / NCBI Sequence Read Archive data
- NCI Genomic Data Commons reference workflows

No controlled-access human data are included in this repository.

## Pipeline overview

```text
FASTQ tumor/normal
      |
      v
BWA or minimap2 alignment
      |
      v
samtools sort + index
      |
      v
GATK Mutect2
      |
      v
GATK FilterMutectCalls
      |
      v
filtered somatic VCF + summary table
```

## Quick start

```bash
conda env create -f environment.yml
conda activate somatic-variant-pipeline

python -m somatic_pipeline.cli run \
  --config config/example_config.yaml
```

The default config is a template. Replace the example paths with your FASTQ/reference files.

## Example commands produced by the pipeline

```bash
bwa mem -t 4 reference.fa tumor_R1.fastq.gz tumor_R2.fastq.gz | samtools sort -o tumor.bam
samtools index tumor.bam

gatk Mutect2 \
  -R reference.fa \
  -I tumor.bam \
  -I normal.bam \
  -tumor TUMOR \
  -normal NORMAL \
  -O unfiltered.vcf.gz

gatk FilterMutectCalls \
  -R reference.fa \
  -V unfiltered.vcf.gz \
  -O filtered.vcf.gz
```

## Repository structure

```text
src/somatic_pipeline/      Python CLI and workflow code
scripts/                   helper scripts
cpp/                       optional C++ VCF filter
workflows/                 runnable bash workflow templates
config/                    example YAML config
examples/                  sample manifest
tests/                     command-generation tests
docs/                      project notes and diagram
```

## Notes

This repository is for educational and portfolio use. It is not a clinical diagnostic workflow.
