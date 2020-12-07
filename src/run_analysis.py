""" Analyse the audio content of the media and write results to an HTML file. """
import logging
import os
import pandas as pd
from audio_tools.vad import wav2segments
from audio_tools.asr import wavfiles2text
from audio_tools.sed import SoundEventDetectionX
from media_tools.format_trans import segment
from common import TMP_DIR, SED_MODEL

logger = logging.getLogger(__name__)

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
        logger.info("---------- Doing SED --------------")
        if segment_method == "sed":
            sed = SoundEventDetectionX(checkpoint_path=SED_MODEL, device='cpu')
            event_timestamps = sed.detect_sound_event(wav_path)
            list_wavpath = []
            for timestamp in event_timestamps:
                if "eech" in timestamp["label"]:
                    segment_path = os.path.join(TMP_DIR, "chunk-{}.wav".format(str(timestamp["id"]).zfill(4)))
                    segment(wav_path, out_filepath=segment_path, start=timestamp["start"], end=timestamp["stop"])
                    list_wavpath.append(segment_path)
                    timestamp["wavfile"] = segment_path
        else:
            logger.info("---------- Doing VAD --------------")
            list_timestamp, list_wavpath = wav2segments(wav_path, outputdir=TMP_DIR)
            # print("Number of segments: {}".format(len(list_wavpath)))
    except Exception as error:
        return 1, "Fail when doing VAD/SED: {}".format(error)

    try:
        logger.info("---------- Doing ASR --------------")
        status, text_dict = wavfiles2text(list_wavpath)
    except Exception as error:
        return 2, "Fail when doing ASR: {}".format(error)

    try:
        content_list = []
        if segment_method == "sed":
            for timestamp in event_timestamps:
                if "wavfile" in timestamp:
                    wav_id = os.path.basename(timestamp["wavfile"]).replace(".wav", "")
                    asr_content = postprocess_asrtext(text_dict[wav_id])
                else:
                    asr_content = "---"
                content_list.append([timestamp["id"], timestamp["start"], timestamp["stop"], timestamp["label"], asr_content])
            dataframe = pd.DataFrame(content_list)
            dataframe.columns = ["id", "start", "stop", "event", "text"]
            dataframe = dataframe.sort_values(by=["start"])
        else:
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
