import os
import sys
CWD = os.getcwd()
sys.path.append(CWD+"/src/")
# from run_analysis import run_analysis
from run_analysis import AudioAnalyser
from common import SED_MODEL, DEEPSPEECH_CN, DEEPSPEECH_EN
ANALYSER = AudioAnalyser(SED_MODEL, DEEPSPEECH_EN, DEEPSPEECH_CN)
AUDIO = CWD + "/tests/1272-128104-0000.wav" 
HTML = CWD + "/tests/1272-128104-0000.html" 

def test_analysis():
    # status, _ = run_analysis(AUDIO, HTML)
    status, _ = ANALYSER.analyse_long_audio(AUDIO, HTML)
    assert status == 0, "Status should be 0"
    print("{} pass.".format(sys.argv[0]))

if __name__ == "__main__":
    test_analysis()
