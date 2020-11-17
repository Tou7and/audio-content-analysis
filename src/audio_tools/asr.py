""" ASR wrapper of Kaldi script """
import os
import sys
import subprocess
from shutil import rmtree
from common import ASR_WORK_DIR, CORPUS_DIR

def create_corpus_dir(corpus_dir, list_wavfiles):
    """ Create Corpus Directory """
    if os.path.isdir(corpus_dir) == False:
        os.makedirs(corpus_dir)
    else:
        rmtree(corpus_dir)
        os.makedirs(corpus_dir)

    wav_scp = os.path.join(corpus_dir, "wav.scp")
    spk2utt = os.path.join(corpus_dir, "spk2utt")
    utt2spk = os.path.join(corpus_dir, "utt2spk")     
    text = os.path.join(corpus_dir, "text")

    wavscp_lines = []
    spk2utt_lines = []
    utt2spk_lines = []
    text_lines = []
    for wavfile in list_wavfiles:
        wav_id = os.path.splitext(os.path.basename(wavfile))[0]
        wavscp_lines.append("{} {}\n".format(wav_id, wavfile))
        spk2utt_lines.append("{} {}\n".format(wav_id, wav_id))
        utt2spk_lines.append("{} {}\n".format(wav_id, wav_id))
        text_lines.append("{} {}\n".format(wav_id, "NO_TRANSRIPTION"))
    
    try:
        with open(wav_scp, "w") as writer:
            writer.writelines(wavscp_lines)

        with open(spk2utt, "w") as writer:
            writer.writelines(spk2utt_lines)

        with open(utt2spk, "w") as writer:
            writer.writelines(utt2spk_lines)

        with open(text, "w") as writer:
            writer.writelines(text_lines)
        status = 0
    except Exception as err:
        raise RuntimeError(err)

def wav2text(wavfile):
    results = subprocess.run(["./recognize-wav.sh", wavfile],
            stdout=subprocess.PIPE, cwd=ASR_WORK_DIR)
    status = results.returncode

    if status == 0:
        with open(os.path.join(ASR_WORK_DIR, "exp/api.ai-model/log/decode.1.log"), "r") as reader:
            lines = reader.readlines()
        for line in lines:
            if (os.path.basename(wavfile).replace(".wav", "") in line) and ("LOG" not in line):
                text = line.replace("\n", "")
    else:
        text = "[{}]".format(results.stderr)
    return status, text

def wavfiles2text(list_wavfiles):
    text_dict = {}
    create_corpus_dir(CORPUS_DIR, list_wavfiles)
    results = subprocess.run(["./recognize-wavfiles.sh"],
            stdout=subprocess.PIPE, cwd=ASR_WORK_DIR)
    status = results.returncode

    for wavfile in list_wavfiles:
        wav_id = os.path.basename(wavfile).replace(".wav", "")
        text_dict[wav_id] = ""

    if status == 0:
        with open(os.path.join(ASR_WORK_DIR, "exp/api.ai-model/log/decode.1.log"), "r") as reader:
            lines = reader.readlines()
        for line in lines:
            asr_content = line.split(" ")
            key = asr_content[0]
            if key in text_dict:
                text_dict[key] = " ".join(asr_content[1:])

    return status, text_dict