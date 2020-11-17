#!/usr/bin/env python
""" Media format transform with FFmepg 
"""
import sys
import os
import ffmpeg

def decode_as_wavfile(in_filename, **input_kwargs):
    """ Convert any media to 16k WAV 
    Notes:
        format = 's16le' --> RAW PCM (no header)
        format = 'wav' --> WAV
    """
    out_filename = os.path.join(os.path.dirname(in_filename), "audio_16k.wav")
    try:
        out, err = (ffmpeg
            .input(in_filename, **input_kwargs)
            .output(out_filename, format='wav', acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as error:
        raise RuntimeError(error.stderr)
    return out_filename

if __name__ == "__main__":
    video = sys.argv[1]
    out = decode_as_wavfile(video)
    print(out)
