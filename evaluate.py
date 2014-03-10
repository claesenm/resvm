#! /usr/bin/env python

# Copyright (c) 2014 Marc Claesen
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither name of copyright holders nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, traceback, subprocess, itertools
from sklearn.metrics import roc_curve, precision_recall_curve, auc
from numpy import ravel

####################################################
# DEFAULT CONFIGURATION & PARAMETER PARSING
####################################################

# Default configuration
defaults = {
    'predictions':'predictions.txt',
    'test':'data/test.libsvm',
    'positive':'1'
    }

class Config:
    def __init__(self,defaults):
        self.dict = defaults
    def __str__(self):
        return str(self.dict)
    def __contains__(self, key):
        return key in self.dict
    def __setitem__(self, key, value):
        self.dict[key]=value
    def __getitem__(self, key):
        val = self.dict.get(key)
        if val==None:
            traceback.print_stack()
            sys.exit("\nError: parameter \"" + key + "\" is not configured.")
        return val            
    def update(self,newconfig):
        self.dict.update(newconfig)
    def get(self):
        return self.dict
        
# Read command line configuration and set global config
cfg = Config(defaults)
# http://stackoverflow.com/a/4260304/2148672
cli_args = dict([arg.split('=', 1) if len(arg.split('=', 1))==2 else [arg, ''] for arg in sys.argv[1:]])
cfg.update(cli_args)

debug="debug" in cfg

####################################################
# PRINT HELP
####################################################

if "help" in cfg or "--help" in cfg:

    print(
"""Compute area under the PR and ROC curves for a set of decision values.

Command line arguments:
predictions : file containing the predictions (default 'predictions.txt').
test        : test data set (must be labeled, default 'data/test.libsvm').
positive    : the positive label (default '1').

This script requires scikit-learn.""")
        
    sys.exit(0)
    
####################################################
# FUNCTIONS TO READ TEST LABELS AND DECISION VALUES
####################################################

def read_labels(filename, delimiter):
    """Reads the labels from filename with given column delimiter."""
    labels = []
    with open(filename,'r') as f:
        for line in f:
            cols = line.split(delimiter)
            labels.append(cols[0])
    if len(labels)==0:
        sys.exit("Error: " + filename + " is empty.")
    return labels

def read_binary_labels(filename, delimiter, positive):
    """Reads the binary labels from filename with given column delimiter.
    
    All labels not equal to positive_label are treated as negative.
    """
    labels = read_labels(filename, delimiter)
    binary_labels = [x==positive for x in labels]
    sum_labels = sum(binary_labels)    
    if sum_labels == 0:
        sys.exit("Error: " + filename + " contains only negative labels.")
    elif sum_labels == len(binary_labels):
        sys.exit("Error: " + filename + " contains only positive labels.")
    return binary_labels
    
def read_decision_values(filename):
    """Reads the decision values."""
    decvals = []
    with open(filename,'r') as f:
        for line in f:
            cols = line.split(' ')
            decvals.append(float(cols[1]))
    if len(decvals)==0:
        sys.exit("Error: " + filename + " is empty.")
    return decvals
    
####################################################
# COMPUTE PERFORMANCE
####################################################
    
labels = read_binary_labels(cfg["test"]," ","1")
decision_values = read_decision_values(cfg["predictions"])

precision, recall, thresholds = precision_recall_curve(ravel(labels), ravel(decision_values))
pr_auc = auc(recall, precision)
print("Area under PR curve: " + str(pr_auc) + ".")

fpr, tpr, thresholds = roc_curve(labels, decision_values)
roc_auc = auc(fpr, tpr)
print("Area under ROC curve: " + str(roc_auc) + ".")

sys.exit(0)
