# FASTQ Analysis Pipeline

A simplified bioinformatics pipeline that processes FASTQ files and generates comprehensive analysis including quality control, trimming, alignment, and variant calling with **VCF output**.

## Pipeline Stages

The pipeline processes your FASTQ files through 4 main stages:

### 1. **FastQC** - Quality Control
- Analyzes read quality and composition
- Outputs: HTML quality report

### 2. **Trimming** - Adapter & Quality Trimming  
- Removes adapter sequences and low-quality bases
- Outputs: Trimmed FASTQ file

### 3. **Alignment** - Sequence Mapping
- Aligns reads to reference genome
- Outputs: SAM and BAM files

### 4. **Variant Calling** - Variant Detection ⭐
- Identifies genetic variations (SNPs, indels)
- Outputs: **VCF (Variant Call Format) file**

## Output Files

For each uploaded FASTQ file, you get:

| File | Description |
|------|-------------|
| `*_fastqc.html` | Quality control report |
| `*_trimmed.fastq.gz` | Trimmed sequence data |
| `*_trimmed_aligned.sam` | Sequence alignment (text format) |
| `*_trimmed_aligned.bam` | Sequence alignment (binary format) |
| `*_trimmed_aligned_variants.vcf` | **Detected genetic variants** |

## Usage

### Web Interface
1. Visit http://localhost:5000
2. Upload your FASTQ file (.fastq.gz or .fq.gz)
3. Wait for processing to complete
4. Download all results including the VCF file

### API Endpoints

**Upload file:**
```bash
curl -X POST -F "file=@sample.fastq.gz" http://localhost:5000/upload
```

**Check status:**
```bash
curl http://localhost:5000/status/{task_id}
```

**Download results:**
```bash
curl http://localhost:5000/results/{task_id}
```

**Download individual file:**
```bash
curl http://localhost:5000/download/{task_id}/{filename}
```

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

Or with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Recent Changes

✅ **Simplified pipeline** - Removed unnecessary stages (post-QC, BAM stats, annotation, integration, report)
✅ **VCF generation fixed** - Variant files now properly included in results
✅ **Cleaner workflow** - Streamlined 4-stage pipeline for faster processing

## Requirements

- Python 3.7+
- FastQC (optional, uses placeholder if not available)
- Cutadapt (optional, uses placeholder if not available)
- Samtools (optional, uses placeholder if not available)
