# Audio Content Analysis
A web application made by Flask.

Users can paste the URL and download the content as video or audio (with youtube-dl),

or get the analyis report. (currently it's just an ASR transcription, planning to add more features)

## TODO
- Use logger for tracing stauts
- Add test scripts
- Add scene classification: make hashtags?
- Add sentient analysis
- Add Mandarin ASR Model
- Add redirection for each functions in main page. 

## Tree
```
src
├── analysis_process.py
├── app.py
├── audio_tools
│   ├── __init__.py
│   ├── asr.py
│   └── vad.py
├── common.py
├── kaldi_scripts
│   ├── recognize-wav.sh
│   └── recognize-wavfiles.sh
├── media_tools
│   ├── format_trans.py
│   ├── generate_subtitle.py
│   └── youtube_download.py
├── templates
│   ├── error_template.html
│   ├── material-life.html
│   └── url_download.html
└── ydl_process.py
```
