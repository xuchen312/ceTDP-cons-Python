# ceTDP-cons-Python

### Installation

- Go to the project page: [ceTDP-appr](https://github.com/ppgorecki/ceTDP-appr).

- Download the standalone tool from the repository.

- Open a terminal, navigate to the tool directory, and run:
  ```
  cd upperbounds
  make
  ```
  
### General Usage

- **Syntax**:
  ```
  ./fgreedy -x batch7.cnf -T0 -N60 –k[kval] [file]
  ```
- **Inputs** (*optional*)
  - ```batch7.cnf``` Configuration file specifying parameters and rules essential for the algorithm,
  - ```-T``` Global time limit in seconds (use ```0``` to disable the time limit),
  - ```-N``` No improvement time threshold in seconds (recommended: ```60```),
  - ```-k``` k-value = min. significant cluster size − 1 (from **ClusterTDP**),
  - ```file``` Input cluster file in CSV/TSV format (function ```WriteClusterFiles``` can be used to create these files).
  
- **Outputs** (*optional; must use none or all for interactive exploration*)
  - ```minscore``` Estimated TDN = TDP × cluster size.
  
- **Example**
  ```
  ./fgreedy -x batch7.cnf -T0 -N60 –k128 clus1.csv
  ```
  


RNifti sources, mainly c, are integrated for reading 
[NIFTI](https://brainder.org/2012/09/23/the-nifti-file-format/) files. To 
build the executable `lb`, first build the RNifti object files with 
`RNifti/Makefile`. [CLion IDE](https://www.jetbrains.com/clion/) was 
used for the development. The CMakeLists.txt contains the instructions 
to build targets `lb`.

