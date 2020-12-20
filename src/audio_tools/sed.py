import os
import numpy as np
import pandas as pd
import librosa
from panns_inference import AudioTagging, SoundEventDetection, labels
from time_cost import time_cost

class SoundEventDetectionX(SoundEventDetection):
    @time_cost
    def detect_sound_event(self, audio_path, n_dominate=5, threshold=0.2):
        """Save sound event detection result as CSV. 

        Args:
          framewise_output (np.array): (time_steps, classes_num)
          n_dominate (int): number of dominated events
          threshold (float): threshold to determine whether the events occur.

        Returns:
          time_stamps (list): a list of sound event time-stamps ({'event', 'id', 'start', 'stop'})
        """
        (audio, _) = librosa.core.load(audio_path, sr=32000, mono=True)
        duration = audio.shape[0]/32000
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
                    elif time_idx == len(activations)-1:
                        time_stamps.append({"label": event_label, "start": round(0.01*start_idx, 4), "stop": round(0.01*time_idx, 4)})
                else:
                    if activate == True:
                        capture_event = True
                        start_idx = time_idx

        self.sort_timestamps(time_stamps, 0, len(time_stamps)-1)

        for ind, time_stamp in enumerate(time_stamps):
            time_stamp["id"] = ind
            if time_stamp["stop"] < duration:
                # Avoid cutting word tail
                time_stamp["stop"] += 0.5
        return time_stamps

    def sort_timestamps(self, time_stamps, head_index, tail_index):
        """ Sort time-stamps based on start time. 
        
        Use quick-sort and pivot is always the last.
        """
        if tail_index >= len(time_stamps):
            raise ValueError("tail_index must less or equal to length of timestamps-1.")

        if tail_index > head_index:
            pivot_index = tail_index
            counter = 0
            for index in range(head_index, tail_index):
                if time_stamps[index-counter]["start"] > time_stamps[pivot_index]["start"]:
                    bigger = time_stamps.pop(index-counter)
                    time_stamps.insert(tail_index, bigger)
                    pivot_index -= 1
                    counter += 1
            self.sort_timestamps(time_stamps, head_index, pivot_index-1)
            self.sort_timestamps(time_stamps, pivot_index+1, tail_index)
        return time_stamps

if __name__ == '__main__':
    model_path = "/Users/mac/panns_data/Cnn14_DecisionLevelMax.pth"
    audio_path = "/Users/mac/data/Eredin/src_wav/audio_16k.wav"
    sed = SoundEventDetectionX(checkpoint_path=model_path, device='cpu')
    event_timestamps = sed.detect_sound_event(audio_path)
    for event in event_timestamps:
        print(event)
