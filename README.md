# Audio Content Analysis
A Flask application for analysing audio content on Youtube.

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

## Vendors
- VAD: [WebRTC VAD](https://github.com/wiseman/py-webrtcvad)
- ASR: Kaldi-ASR model provided by [Api.ai](https://github.com/dialogflow/api-ai-english-asr-model)
- SED: Pytorch model of paper [PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition](https://arxiv.org/abs/1912.10211)
