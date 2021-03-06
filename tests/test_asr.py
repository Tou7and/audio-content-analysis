import os
import sys
from pathlib import Path

CWD = os.getcwd()
sys.path.append(CWD+"/src/")

from audio_tools.asr import wavfiles2text

WAVES = [CWD + "/tests/1272-128104-0000.wav"] 
WAVES_CN = [CWD + "/tests/冰風暴_16k.wav"] 

def test_asr():
    status, text_dict = wavfiles2text(WAVES)
    assert status == 0
    print(text_dict)
    print("ASR testing complete.")

def test_asr_cn():
    status, text_dict = wavfiles2text(WAVES_CN, lang="cn")
    assert status == 0
    print(text_dict)
    print("ASR(CN) testing complete.")

if __name__ == "__main__":
    test_asr()
    test_asr_cn()
