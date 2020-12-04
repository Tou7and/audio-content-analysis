import os
import numpy as np
import pandas as pd
import librosa
from panns_inference import AudioTagging, SoundEventDetection, labels

class SoundEventDetectionX(SoundEventDetection):
    def detect_sound_event(self, audio_path, n_dominate=5, threshold=0.2):
        """Save sound event detection result as CSV. 

        Args:
          framewise_output (np.array): (time_steps, classes_num)
          n_dominate (int): number of dominated events
          threshold (float): threshold to determine whether the events occur.

        Returns:
          time_stamps (list): a list of sound event time-stamps ({'event', 'start', 'stop'})
        """
        (audio, _) = librosa.core.load(audio_path, sr=32000, mono=True)
        audio = audio[None, :]  # (batch_size, segment_samples)

        framewise_output = self.inference(audio) # (batch_size, time_steps, classes_num)
        framewise_output = framewise_output[0]

        classwise_output = np.max(framewise_output, axis=0) # (classes_num,)
        dominate_events = np.argsort(classwise_output)[::-1]
        dominate_events = dominate_events[0:n_dominate]

        ix_to_lb = {i : label for i, label in enumerate(labels)}
        
        time_stamps = []
        for event_id in dominate_events:
            event_info = dict()
            event_label = ix_to_lb[event_id]
            event_info["prob"] = framewise_output[:, event_id]
            activations = framewise_output[:, event_id] > threshold
            event_info["active"] = activations

            capture_event = False
            start_idx = 0
            for time_idx, activate in enumerate(activations):
                if capture_event:
                    if activate == False:
                        capture_event = False
                        time_stamps.append({"label": event_label, "start": round(0.01*start_idx, 4), "stop": round(0.01*time_idx, 4)})
                else:
                    if activate == True:
                        capture_event = True
                        start_idx = time_idx
        # df_timestamp = pd.DataFrame(time_stamps)
        # df_timestamp.to_csv("results/timestamps.csv")
        return time_stamps

    def get_speech_segments(self, audio_path, outputdir=None):
        event_dict = self.detect_sound_event(audio_path)
        # TODO: get speech time stamps and cut them to outputdir
        return list_timestamp, list_wavpath

if __name__ == '__main__':
    model_path = "/Users/mac/panns_data/Cnn14_DecisionLevelMax.pth"
    audio_path = "/Users/mac/data/Eredin/src_wav/audio_16k.wav"
    sed = SoundEventDetectionX(checkpoint_path=model_path, device='cpu')
    event_timestamps = sed.detect_sound_event(audio_path)
    for event in event_timestamps:
        print(event)
