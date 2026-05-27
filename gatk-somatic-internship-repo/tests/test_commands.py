from somatic_pipeline.commands import bwa_mem, mutect2, filter_mutect_calls


def test_bwa_command_contains_expected_tools():
    cmd = bwa_mem("ref.fa", "a_R1.fq.gz", "a_R2.fq.gz", "a.bam", 8)
    assert "bwa mem" in cmd
    assert "samtools sort" in cmd
    assert "-t 8" in cmd


def test_mutect2_command_contains_tumor_normal_names():
    cmd = mutect2("ref.fa", "tumor.bam", "normal.bam", "TUMOR", "NORMAL", "out.vcf.gz")
    assert "gatk Mutect2" in cmd
    assert "-tumor TUMOR" in cmd
    assert "-normal NORMAL" in cmd


def test_filter_mutect_calls_command():
    cmd = filter_mutect_calls("ref.fa", "in.vcf.gz", "out.vcf.gz")
    assert cmd == "gatk FilterMutectCalls -R ref.fa -V in.vcf.gz -O out.vcf.gz"
