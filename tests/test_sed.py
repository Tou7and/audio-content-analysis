import os
import sys
from pathlib import Path

CWD = os.getcwd()
sys.path.append(CWD+"/src/")

from audio_tools.sed import SoundEventDetectionX

SED_MODEL = '{}/panns_data/Cnn14_DecisionLevelMax.pth'.format(str(Path.home()))
AUDIO = CWD + "/tests/1272-128104-0000.wav"

FAKE_TIMESTAMP = [
    {"start": 0.0},
    {"start": 9.0},
    {"start": 7.0},
    {"start": 5.0},
    {"start": 5.0},
    {"start": 6.0},
    {"start": 11.0},
    {"start": 19.0},
    {"start": 16.0}
]

FAKE_TIMESTAMP_SORTED = [
    {"start": 0.0},
    {"start": 5.0},
    {"start": 5.0},
    {"start": 6.0},
    {"start": 7.0},
    {"start": 9.0},
    {"start": 11.0},
    {"start": 16.0},
    {"start": 19.0}
]

def test_sed():
    sed = SoundEventDetectionX(checkpoint_path=SED_MODEL, device='cpu')
    event_timestamps = sed.detect_sound_event(AUDIO)
    event_types = []
    for event in event_timestamps:
        if event["label"] not in event_types:
            event_types.append(event["label"])
    assert "Speech" in event_types
    print(event_timestamps)
    print("SED testing complete.")

def test_sed_sort():
    sed = SoundEventDetectionX(checkpoint_path=SED_MODEL, device='cpu')
    x = FAKE_TIMESTAMP
    sorted_ts = sed.sort_timestamps(x, 0, len(x)-1)
    assert sorted_ts == FAKE_TIMESTAMP_SORTED

if __name__ == "__main__":
    test_sed()
    test_sed_sort()
