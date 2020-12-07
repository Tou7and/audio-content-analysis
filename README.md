# Audio Content Analysis
A Flask application for analysing audio content on Youtube.

## TODO
- Trace computation and time cost
- ASR scripts multiprocessing
- logger for tracing status and errors
- Scene classification: make hashtags?
- Sentient analysis?
- Mandarin ASR

# DONE
- Replace current VAD with a SED (sound event detector)

## Tree
```
├── docker  :  Dockefiles
├── scripts :  Scripts for building and deploying service
├── src   :  Source codes
│   ├── audio_tools
│   ├── kaldi_scripts
│   ├── media_tools
│   └── templates
```
