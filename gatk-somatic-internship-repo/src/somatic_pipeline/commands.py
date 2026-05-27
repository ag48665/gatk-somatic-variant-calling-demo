from pathlib import Path


def bwa_mem(reference: str, r1: str, r2: str, out_bam: str, threads: int = 4) -> str:
    return f"bwa mem -t {threads} {reference} {r1} {r2} | samtools sort -o {out_bam}"


def minimap2_align(reference: str, r1: str, r2: str, out_bam: str, threads: int = 4) -> str:
    return f"minimap2 -ax sr -t {threads} {reference} {r1} {r2} | samtools sort -o {out_bam}"


def samtools_index(bam: str) -> str:
    return f"samtools index {bam}"


def mutect2(reference: str, tumor_bam: str, normal_bam: str, tumor_name: str, normal_name: str, out_vcf: str) -> str:
    return (
        f"gatk Mutect2 -R {reference} "
        f"-I {tumor_bam} -I {normal_bam} "
        f"-tumor {tumor_name} -normal {normal_name} "
        f"-O {out_vcf}"
    )


def filter_mutect_calls(reference: str, in_vcf: str, out_vcf: str) -> str:
    return f"gatk FilterMutectCalls -R {reference} -V {in_vcf} -O {out_vcf}"


def ensure_output_paths(output_dir: str) -> dict[str, str]:
    out = Path(output_dir)
    return {
        "tumor_bam": str(out / "bam" / "tumor.sorted.bam"),
        "normal_bam": str(out / "bam" / "normal.sorted.bam"),
        "unfiltered_vcf": str(out / "variants" / "somatic.unfiltered.vcf.gz"),
        "filtered_vcf": str(out / "variants" / "somatic.filtered.vcf.gz"),
    }
