""" WAV --> HTML
"""
import os
import pandas as pd
from audio_tools.vad import wav2segments
from audio_tools.asr import wavfiles2text

from common import TMP_DIR

def run_analysis_process(wav_path, html_path):
    """ Given a wavfile, run analysis and write the results to a HTML file.
    Args:
        wav_path: str, path of wavfile
        html_path: str, path of HTML file

    Returns:
        status: int, status code
            0 = success
            1 = VAD fail
            2 = ASR Fail
            3 = Fail to make HTML
    """
    try:
        print("Doing VAD...")
        list_timestamp, list_wavpath = wav2segments(wav_path, outputdir=TMP_DIR)
        print("Number of segments: {}".format(len(list_wavpath)))
    except Exception as error:
        return 1, error

    try:
        print("Doing ASR...")
        _, text_dict = wavfiles2text(list_wavpath)
    except Exception as error:
        return 2, error

    try:
        content_list = []
        for ind, timestamp in enumerate(list_timestamp):
            wav_id = os.path.basename(list_wavpath[ind]).replace(".wav", "")
            content_list.append([ind, timestamp["start"], timestamp["stop"], text_dict[wav_id]])

        dataframe = pd.DataFrame(content_list)
        dataframe.columns = ["id", "start", "stop", "text"]
        dataframe.to_html(html_path, index=None)
        print("Analysis process done.")
    except Exception as error:
        return 3, error

    return 0, "Success"

if __name__ == "__main__":
    run_analysis_process("/opt/src/data/Eredin_1min.wav", "/opt/src/data/Eredin_1min.html")
