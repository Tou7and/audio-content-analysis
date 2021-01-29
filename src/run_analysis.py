""" Analyse the audio content of the media and write results to an HTML file. """
import logging
import os
import wave
import threading
import queue
from timeit import default_timer as timer
import numpy as np
import pandas as pd
from opencc import OpenCC
from audio_tools.vad import wav2segments
from audio_tools.deepspeech_asr import Model, convert_samplerate
from audio_tools.sed import SoundEventDetectionX
from media_tools.format_trans import segment
from common import TMP_DIR

logger = logging.getLogger(__name__)

class AudioAnalyser:
    """ Current pipeline: Long Audio --> SED --> ASR --> Report """
    def __init__(self, sed_path:str, asr_en:dict, asr_cn:dict, asr_nj=8):
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
        self.asr_nj = asr_nj
        self.converter = OpenCC('s2t')

    def exec_sed(self, audio_path:str):
        """ Given a WAVE file, return SED results using a model trained with AudioSet.
            AudioSet: <https://research.google.com/audioset/>

        Returns:
            event_timestamps (list):
                each item is a dict with following keys - label, start, stop, wavfile
        """
        event_timestamps = self.sed.detect_sound_event(audio_path)

        for event in event_timestamps:
            if "eech" in event["label"]:
                filename = "chunk-{}.wav".format(str(event["id"]).zfill(4))
                filepath = os.path.join(TMP_DIR, filename)
                segment(audio_path, out_filepath=filepath, start=event["start"], end=event["stop"])
                event["wavfile"] = filepath
            else:
                event["wavfile"] = "NULL"

        return event_timestamps

    def exec_vad(self, audio_path: str):
        """ Given a WAVE file, return SED results using a model trained with AudioSet.
            AudioSet: <https://research.google.com/audioset/>

        Returns:
            event_timestamps (list):
                each item is a dict with following keys - label, start, stop, wavfile
        """
        list_timestamp, list_wavpath = wav2segments(audio_path, outputdir=TMP_DIR)

        for ind, timestamp in enumerate(list_timestamp):
            timestamp["wavfile"] = list_wavpath[ind]

        return list_timestamp

    def exec_asr(self, audio_path: str, language="en", verbose=0):
        """ Given a WAVE file, return ASR results using an English model.

        Returns:
            infer_text (str)
        """
        if language == "en":
            desired_sample_rate = self.asr_en.sampleRate()
        else:
            desired_sample_rate = self.asr_cn.sampleRate()

        fin = wave.open(audio_path, 'rb')
        fs_orig = fin.getframerate()
        if fs_orig != desired_sample_rate:
            _, audio = convert_samplerate(audio_path, desired_sample_rate)
        else:
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        audio_length = fin.getnframes() * (1/fs_orig)
        fin.close()

        inference_start = timer()

        if language == "en":
            infer_text = self.asr_en.stt(audio)
        else:
            infer_text = self.asr_cn.stt(audio)
            if language == "tw":
                infer_text = self.converter.convert(infer_text)

        inference_end = timer() - inference_start
        if verbose > 0:
            logger.info('ASR took %s sec for %s sec audio.', inference_end, audio_length)
            logger.info('%s : %s', audio_path, infer_text)
        return infer_text

    def analyse_long_audio(self, audio_path, html_path, use_sed=True, language='en'):
        """ Analyse long audio.

        Returns:
            status (int): 0 = Success, 1 = SED Error, 2 = ASR Error
            detail (str)
        """

        try:
            logger.info("Excecuting SED ...")
            start_sed = timer()
            if use_sed:
                list_timestamp = self.exec_sed(audio_path)
            else:
                list_timestamp = self.exec_vad(audio_path)
            time_cost_sed = timer() - start_sed
            logger.info("SED done, cost %s seconds.", time_cost_sed)
        except Exception as error:
            return 1, error

        def asr_worker(asr_q, result_list, lang):
            """ Attach ASR results to the events, and append the events to the list. """
            while asr_q.empty() is False:
                event = asr_q.get()

                if os.path.exists(event["wavfile"]):
                    event["text"] = self.exec_asr(event["wavfile"], language=lang, verbose=2)
                else:
                    event["text"] = "---"*3
                result_list.append(event)
                asr_q.task_done()

        the_asr_q = queue.Queue()
        the_content_list = []
        for event in list_timestamp:
            the_asr_q.put(event)

        try:
            logger.info("Excecuting ASR ...")
            start_asr = timer()

            for _ in range(self.asr_nj):
                threading.Thread(
                    target=asr_worker,
                    daemon=True,
                    args=(the_asr_q, the_content_list, language)
                ).start()

            the_asr_q.join()

            time_cost_asr = timer() - start_asr
            logger.info("ASR done, cost %s seconds.", time_cost_asr)
        except Exception as error:
            return 2, error

        dataframe = pd.DataFrame(the_content_list)
        dataframe = dataframe[['id', 'label', 'start', 'stop', 'text']]
        dataframe = dataframe.sort_values(by=["id"])
        dataframe.to_html(html_path, index=None, justify="left")
        return 0, "Success"
