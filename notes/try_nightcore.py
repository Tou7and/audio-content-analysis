import nightcore as nc
from glob import glob

mp3_files = glob("/Users/mac/data/mp3/*.mp3")

for mp3 in mp3_files:
    # nc_audio = "/Users/mac/data/mp3/ninelie-aimer.mp3" @ nc.Tones(1)
    audio = nc.nightcore(mp3, nc.Tones(1), format="mp3")
    new_mp3 = mp3.replace(".mp3", "-nc.mp3")
    audio.export(new_mp3)
    print(new_mp3)
