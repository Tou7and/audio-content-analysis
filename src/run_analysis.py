""" WAV --> HTML
"""
import os
import pandas as pd
from audio_tools.vad import wav2segments
from audio_tools.asr import wavfiles2text
from audio_tools.sed import SoundEventDetectionX

from common import TMP_DIR, SED_MODEL

def postprocess_asrtext(text):
    """ Post-process on ASR text for better visuals
    Args:
        text (str)
    Returns:
        text (str)
    """
    text = text.lower()
    text = text.replace("\n", "")
    return text 

def run_analysis(wav_path, html_path, segment_method="sed"):
    """ Given a wavfile, run analysis and write the results to a HTML file.
    Args:
        wav_path (str): path of wavfile
        html_path (str): path of HTML file
        segment_method (str): 
            "sed" for using sound event detector to segment wavfile. 
            Otherwise use webrtcvad.

    Returns:
        status (int): status code
            0 = success
            1 = VAD fail
            2 = ASR Fail
            3 = Fail to make HTML
    """
    try:
        if segment_method == "sed":
            sed = SoundEventDetectionX(checkpoint_path=model_path, device='cpu')
            # event_timestamps = sed.detect_sound_event(audio_path)
            list_timestamp, list_wavpath = sed.get_segments(audio_path, outputdir=TMP_DIR)
            # TODO: modify the whole function for SED results presentation
        else:
            # print("Doing VAD...")
            list_timestamp, list_wavpath = wav2segments(wav_path, outputdir=TMP_DIR)
            # print("Number of segments: {}".format(len(list_wavpath)))
    except Exception as error:
        return 1, "Fail when doing VAD/SED: {}".format(error)

    try:
        # print("Doing ASR...")
        _, text_dict = wavfiles2text(list_wavpath)
    except Exception as error:
        return 2, "Fail when doing ASR: {}".format(error)

    try:
        content_list = []
        for ind, timestamp in enumerate(list_timestamp):
            wav_id = os.path.basename(list_wavpath[ind]).replace(".wav", "")
            content_list.append([ind, timestamp["start"], timestamp["stop"], postprocess_asrtext(text_dict[wav_id])])

        dataframe = pd.DataFrame(content_list)
        dataframe.columns = ["id", "start", "stop", "text"]
        dataframe.to_html(html_path, index=None, justify="left")
    except Exception as error:
        return 3, "Fail when generating table: {}".format(error)

    return 0, "Success"

if __name__ == "__main__":
    run_analysis("/opt/src/data/Eredin_1min.wav", "/opt/src/data/Eredin_1min.html")
