#!/usr/bin/env python
""" Media format transform with FFmepg """
import sys
import os
import warnings
import ffmpeg

def decode_as_wavfile(in_filepath, **input_kwargs):
    """ Convert any media to 16k WAV 
    Notes:
        format = 's16le' --> RAW PCM (no header)
        format = 'wav' --> WAV
    """
    out_filepath = os.path.join(os.path.dirname(in_filepath), "audio_16k.wav")
    try:
        out, err = (ffmpeg
            .input(in_filepath, **input_kwargs)
            .output(out_filepath, format='wav', acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as error:
        raise RuntimeError(error.stderr)
    return out_filepath

def probe(in_filepath, verbose=0):
    """ Get media information of input file. 

    Returns:
        format_info: dict, with the following keys --
            filename /Users/mac/Downloads/HiroyukiSawano–ashes.mp3
            nb_streams 1
            nb_programs 0
            format_name mp3
            format_long_name MP2/3 (MPEG audio layer 2/3)
            start_time 0.023021
            duration 545.040000
            size 13081581
            bit_rate 192009
            probe_score 51
            tags {'encoder': 'Lavf57.56.101'}
    """
    try:
        infos = ffmpeg.probe(in_filepath)
    except Exception as error:
        raise RuntimeError(error)
    stream_list = infos["streams"]
    format_info = infos["format"]

    if verbose > 0:
        print("Number of stream : {}".format(len(stream_list)))
        for key, val in format_info.items():
            print(key, val)
    return format_info

def segment(in_filepath, out_filepath=None, start=0.0, end=0.0):
    """ Make video/audio clip by trimming original file. """
    if out_filepath == None:
        base, ext = os.path.splitext(in_filepath)
        out_filepath = base + "_segment" + ext

    try:
        start = float(start)
        end = float(end)
    except Exception as error:
        raise TypeError("start and end must be int or float, or string that can be convert to float.")

    try:
        info = probe(in_filepath)
        src_duration = float(info["duration"])
    except Exception as error:
        raise RuntimeError("Fail to get file information with FFmpeg.")

    if end > src_duration:
        warnings.warn("format_trans.segment: end timestamp not in duration range, using duration instead.", Warning)
        end = src_duration
    seg_duration = end - start
    if seg_duration <= 0:
        warnings.warn("format_trans.segment: segment duration below zero, return original file.", Warning)
        return in_filepath

    try:
        out, err = (ffmpeg
            .input(in_filepath, ss=start, t=seg_duration)
            .output(out_filepath)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except Exception as error:
        raise RuntimeError("{}".format(error))
    return out_filepath

if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    start = sys.argv[3]
    end = sys.argv[4]
    # out = decode_as_wavfile(video)
    # out = probe(video, verbose=1)
    segment(src, dst, start, end)
