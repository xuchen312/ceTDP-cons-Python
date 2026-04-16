# ceTDP-cons-Python

**Stage 2 Python tool** for computing the lower bounds on TDP (True Discovery Proportion) from **ceTDP-cons**.

## Installation

No additional packages required. Download `lb.py` and run directly. Or clone the repository:

```bash
git clone https://github.com/xuchen312/ceTDP-cons-Python.git
cd ceTDP-cons-Python
```
  
## General Usage
  
```bash
python lb.py -k <k-value> <input> -o <output>
```
  
## Arguments
  
- `-k` - Minimum significant cluster size **minus 1** (output from Stage 1)

- `input` - Either:

    - A directory containing multiple input files (CSV/TSV), or

    - A single file with voxel coordinates (x, y, z) for a single region (CSV/TSV format, derived from Stage 1)

- `-o` - (Optional) Output CSV file name. If provided, results are saved to the specified file.

### Input file format

CSV or TSV format with x, y, z columns:

```
x,y,z
26,72,24
27,72,24
30,72,24
...
```
  
## Output

A table summarizing the estimated lower bounds for each input region:

- `file`: input file name
- `size`: |S| = number of voxels in the region (row count)
- `TDN`: estimated TDN (True Discovery Number) lower bound
- `TDP`: corresponding TDP lower bound = TDN / |S|

If `-o` is specified, the table is also saved as a CSV file.

## Example

```bash
python lb.py -k 20 xyz.csv -o results
```

Output (printed to terminal, and saved to `results.csv`):

```
file              size       TDN        TDP       
xyz.csv           7689       3635       0.472753 
```

## Any questions or bugs?

Please contact Xu Chen at xuchen312@gmail.com.
