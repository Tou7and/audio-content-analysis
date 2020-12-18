import os
import sys

CWD = os.getcwd()
sys.path.append(CWD+"/src/")

from audio_tools.vad import wav2segments

AUDIO = CWD + "/tests/1272-128104-0000.wav"

def test_vad():
    timestamps, _ = wav2segments(AUDIO)
    assert isinstance(timestamps, list) == True
    assert len(timestamps) > 0
    print(timestamps)
    print("VAD testing complete.")

if __name__ == "__main__":
    test_vad()
