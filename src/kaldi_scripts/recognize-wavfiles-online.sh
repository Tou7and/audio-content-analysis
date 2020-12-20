#!/usr/bin/env bash

. ./path.sh
MODEL_DIR="exp/api.ai-model"
DATA_DIR="data/test-corpus"
NJ=$1
BEAM_SIZE=$2

steps/online/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 --beam $BEAM_SIZE --cmd run.pl --nj $NJ exp/api.ai-model/ data/test-corpus/ exp/api.ai-model/decode/
