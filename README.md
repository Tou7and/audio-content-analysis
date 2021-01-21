# Audio Content Analysis
A Flask application for analysing audio content on Youtube.

分析 Youtube 影片的音訊內容。

## Setup
下載 Docker Image，透過 scripts/run.sh 腳本在 localhost 啟動服務。
1. Pull image from DockerHub: docker pull tou7and/audio-content-analysis
2. ./scripts/run.sh
3. The service should be running on localhost:5566 by default

透過 Docker 重新建 image: scripts/build.sh
- 需要另外下載以下資料並置於 data 目錄下。
  - `Cnn14_DecisionLevelMax.pth` : <https://zenodo.org/record/3987831/files/Cnn14_DecisionLevelMax_mAP%3D0.385.pth?download=1>
  - `multi_cn_chain_sp_online` : <https://kaldi-asr.org/models/m11>

## Files
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
- SED: 
  - [PANNs] (https://github.com/qiuqiangkong/panns_inference) 
  - reference [PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition](https://arxiv.org/abs/1912.10211)
