#!/bin/bash
source /das/work/p20/p20847/code/install_anaconda/anaconda3/etc/profile.d/conda.sh
conda activate mtbig
python -u test.py "$@"




