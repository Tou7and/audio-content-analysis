""" Global variables are defined here """
TMP_DIR = "/opt/src/data/"
TEMPLATE_DIR = "/opt/src/templates"
ASR_WORK_DIR = "/opt/kaldi/egs/apiai_decode/s5"
CORPUS_DIR = "/opt/kaldi/egs/apiai_decode/s5/data/test-corpus"
SED_MODEL = "/root/panns_data/Cnn14_DecisionLevelMax.pth"
DEEPSPEECH_CN = {
        "model":"/root/deepspeech_data/deepspeech-0.9.3-models-zh-CN.pbmm",
        "scorer": "/root/deepspeech_data/deepspeech-0.9.3-models-zh-CN.scorer"
        }
DEEPSPEECH_EN = {
        "model":"/root/deepspeech_data/deepspeech-0.9.3-models.pbmm",
        "scorer":"/root/deepspeech_data/deepspeech-0.9.3-models.scorer"
        }
LOG_FILE = "/opt/log.txt"
