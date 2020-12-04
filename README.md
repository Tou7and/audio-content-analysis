# Audio Content Analysis
A Flask application for analysing audio content on Youtube.

## TODO
- Replace current VAD with a SED (sound event detector)
- Use logger for tracing stauts
- Add test scripts
- Scene classification: make hashtags?
- Sentient analysis?
- Mandarin ASR

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
