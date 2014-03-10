Script for the Robust Ensemble of SVMs (RESVM) method. For algorithm details, 
please refer to:
    ftp://ftp.esat.kuleuven.be/pub/SISTA/claesenm/reports/14-22.pdf

If you use this software in research, please cite the associated paper.

This script allows you to perform the following tasks:
- `train`          : train an RESVM model.
- `predict`        : predict with an existing RESVM model.
- `cross-validate` : perform k-fold cross-validation for a parameter tuple.
- `grid-search`    : select an optimal parameter tuple (+optionally train model).

To perform a specific task, call `./resvm.py task options`.
An overview of task specific arguments is shown using `./resvm.py help task`.

Training and testing data files must be provided in LIBSVM format, e.g.
> label index_1:value_1 index_2:value_2 ... index_p:value_p

For additional information, updates or bug reports, please refer to:
    https://github.com/claesenm/resvm

---

#### EnsembleSVM

This script generates intermediate files in a folder of your choosing. 
The EnsembleSVM library is used as a back-end and must be installed.
EnsembleSVM is freely available at: 
  http://esat.kuleuven.be/stadius/ensemblesvm/

General options related to EnsembleSVM, usable in all tasks listed above:
- `esvm-prefix` : prefix used in all EnsembleSVM executables (default '').
- `esvm-suffix` : suffix used in all EnsembleSVM executables (default '').
- `work-dir`    : working directory to use for intermediate files (default '`/tmp/`').
- `noclean`     : retain intermediate files (flag, default: remove intermediates).

---

#### Example

As an example we have included one pair of training and test sets used in the associated paper.
These data sets are based on MNIST with digit 7 as positive, with 50 positives and 2000 unlabeled
instances. The provided positive and unlabeled sets contain 10% contamination.

Train an RESVM with 200 base models, each trained using 10 positives and 100 unlabeled instances.
The resulting model will be saved in `model.txt`.
```bash
./resvm.py train data=data/train.libsvm nmodels=200 npos=10 nunl=100 c=1 wpos=1.6 model=model.txt
```

Predict the test set using the model we trained and save to `predictions.txt`. The output file
contains predicted labels in the first column and decision values in the second.
```bash
./resvm.py predict data=data/test.libsvm model=model.txt predictions=predictions.txt
```

To compute area under the PR and ROC curves, please use `./evaluate.py` (requires scikit-learn).
