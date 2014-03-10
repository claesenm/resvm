Script for the Robust Ensemble of SVMs (RESVM) method. For algorithm details, 
please refer to:
    ftp://ftp.esat.kuleuven.be/pub/SISTA/claesenm/reports/14-22.pdf

If you use this software in research, please cite the associated paper.

This script allows you to perform the following tasks:
- train          : train an RESVM model.
- predict        : predict with an existing RESVM model.
- cross-validate : perform k-fold cross-validation for a parameter tuple.
- grid-search    : select an optimal parameter tuple (+optionally train model).

To perform a specific task, call "./resvm.py <task> options".
An overview of task specific arguments is shown using "./resvm.py help <task>".

Training and testing data files must be provided in LIBSVM format, e.g.
> label index_1:value_1 index_2:value_2 ... index_n:value_n

---

This script generates intermediate files in a folder of your choosing. 
The EnsembleSVM library is used as a back-end and must be installed.
EnsembleSVM is freely available at: 
  http://esat.kuleuven.be/stadius/ensemblesvm/

General options related to EnsembleSVM, usable in all tasks listed above:
- esvm-prefix : prefix used in all EnsembleSVM executables (default '').
- esvm-suffix : suffix used in all EnsembleSVM executables (default '').
- work-dir    : working directory to use for intermediate files (default '/tmp/').
- noclean     : retain intermediate files (flag, default: remove intermediates).

---

For additional information, updates or bug reports, please refer to:
    https://github.com/claesenm/resvm.
