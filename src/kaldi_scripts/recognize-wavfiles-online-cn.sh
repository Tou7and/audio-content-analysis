#!/usr/bin/env bash

. ./path.sh
MODEL_DIR="exp/multi_cn_chain_sp_online"
DATA_DIR="data/test-corpus"
NJ=$1
BEAM_SIZE=$2

steps/online/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 --beam $BEAM_SIZE --cmd run.pl --nj $NJ exp/multi_cn_chain_sp_online/ data/test-corpus/ exp/multi_cn_chain_sp_online/decode/
