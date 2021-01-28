""" Analyse the audio content of the media and write results to an HTML file. """
import logging
import os
import wave
import numpy as np
import pandas as pd
from timeit import default_timer as timer
from opencc import OpenCC
from audio_tools.vad import wav2segments
# from audio_tools.asr import wavfiles2text
from audio_tools.deepspeech_asr import Model
from audio_tools.sed import SoundEventDetectionX
from media_tools.format_trans import segment
from common import TMP_DIR, SED_MODEL

logger = logging.getLogger(__name__)

class AudioAnalyser:
    def __init__(self, sed_path:str, asr_en:dict, asr_cn:dict):
        """ Initialize all models needed for audio analysis.
        Args:
            sed_path (str): path of SED model
            asr_en (dict): contain model and scorer of deepspeech
            asr_cn (dict): contain model and scorer of deepspeech
        """
        self.sed = SoundEventDetectionX(checkpoint_path=sed_path, device='cpu')

        self.asr_en = Model(asr_en["model"])
        self.asr_en.enableExternalScorer(asr_en["scorer"])
        self.asr_cn = Model(asr_cn["model"])
        self.asr_cn.enableExternalScorer(asr_cn["scorer"])

        self.converter = OpenCC('s2t')

    def exec_sed(self, audio_path):
        event_timestamps = self.sed.detect_sound_event(audio_path)
        list_wavpath = []
        for timestamp in event_timestamps:
            if "eech" in timestamp["label"]:
                segment_path = os.path.join(TMP_DIR, "chunk-{}.wav".format(str(timestamp["id"]).zfill(4)))
                segment(audio_path, out_filepath=segment_path, start=timestamp["start"], end=timestamp["stop"])
                list_wavpath.append(segment_path)
                timestamp["wavfile"] = segment_path
        return event_timestamps, list_wavpath

    def exec_vad(self, audio_path):
        list_timestamp, list_wavpath = wav2segments(audio_path, outputdir=TMP_DIR)
        return list_timestamp, list_wavpath

    def exec_asr_en(self, audio_path):
        desired_sample_rate = self.asr_en.sampleRate()

        fin = wave.open(audio_path, 'rb')
        fs_orig = fin.getframerate()
        if fs_orig != desired_sample_rate:
            fs_new, audio = convert_samplerate(audio, desired_sample_rate)
        else:
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        audio_length = fin.getnframes() * (1/fs_orig)
        fin.close()
        infer_text = self.asr_en.stt(audio)
        # print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
        return infer_text

    def exec_asr_cn(self, audio_path):
        desired_sample_rate = self.asr_cn.sampleRate()

        fin = wave.open(audio_path, 'rb')
        fs_orig = fin.getframerate()
        if fs_orig != desired_sample_rate:
            fs_new, audio = convert_samplerate(audio, desired_sample_rate)
        else:
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        audio_length = fin.getnframes() * (1/fs_orig)
        fin.close()
        infer_text = self.asr_cn.stt(audio)
        # print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)
        return infer_text

    def analyse_long_audio(self, audio_path, html_path, use_seg=True, language='en'):
        """ Analyse long audio.

        Returns:
            status (int): 0 = Success, 1 = SED Error, 2 = ASR Error
            detail (str)
        """
        try:
            content_list = []

            logger.info("Excecuting SED ...")
            start_sed = timer()
            if use_seg:
                list_timestamp, list_wavpath = self.exec_sed(audio_path)
            else:
                list_timestamp, list_wavpath = self.exec_vad(audio_path)
            time_cost_sed = timer() - start_sed
            logger.info("SED done, cost {} seconds.".format(time_cost_sed))
        except Exception as error:
            return 1, error

        try:
            logger.info("Excecuting ASR ...")
            start_asr = timer()
            for timestamp in list_timestamp:
                if "eech" in timestamp["label"]:
                    if language == "en":
                        asr_content = self.exec_asr_en(timestamp['wavfile'])
                    else:
                        asr_content = self.exec_asr_cn(timestamp['wavfile'])
                        if language == "tw":
                            asr_content = self.converter.convert(asr_content)
                    if use_seg:
                        content_list.append([timestamp["id"], timestamp["start"], timestamp["stop"], timestamp["label"], asr_content])
                    else:
                        content_list.append([timestamp["id"], timestamp["start"], timestamp["stop"], "Voice", asr_content])
            time_cost_asr = timer() - start_asr
            logger.info("ASR done, cost {} seconds.".format(time_cost_asr))
        except Exception as error:
            return 2, error

        dataframe = pd.DataFrame(content_list)
        dataframe.columns = ["id", "start", "stop", "event", "text"]
        dataframe = dataframe.sort_values(by=["start"])
        dataframe.to_html(html_path, index=None, justify="left")
        return 0, "Success"

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

def run_analysis(wav_path, html_path, segment_method="sed", asr_lang="en"):
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
        status, text_dict = wavfiles2text(list_wavpath, lang=asr_lang)
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
