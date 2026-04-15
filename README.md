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
python lb.py -k <k-value> <file>
```
  
## Arguments
  
- ```-k``` - Minimum significant cluster size **minus 1** (output from Stage 1)

- ```file``` - Input file containing voxel coordinates (`x`, `y` and `z`) for a single region (CSV/TSV format, derived from Stage 1)

  Example of input file format:
  ```
  x,y,z
  26,72,24
  27,72,24
  30,72,24
  ...
  ```
  
## Output

A single integer: the estimated TDN (True Discovery Number) lower bound for the input region.
  
> TDP = TDN / |S|, where |S| is the size (number of voxels) of the region (i.e., row count of the input file).
  
## Example

```bash
python lb.py -k 20 xyz.csv
```

Output:

```
3635
```

## Any questions or bugs?

Please contact Xu Chen at xuchen312@gmail.com.
