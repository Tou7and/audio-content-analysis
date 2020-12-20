#!/usr/bin/env bash

. ./path.sh
MODEL_DIR="exp/api.ai-model"
DATA_DIR="data/test-corpus"
NJ=$1

steps/online/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 --cmd run.pl --nj $NJ exp/api.ai-model/ data/test-corpus/ exp/api.ai-model/decode/
