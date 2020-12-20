import sys
import os

CWD = os.getcwd()
sys.path.append(CWD+"/src")

from download_youtube import YoutubeDownloader

LINK = "https://www.youtube.com/watch?v=oRdxUFDoQe0"

def test_ydl():
    ydl_p = YoutubeDownloader(LINK, storage_dir=CWD, dst_format="wav", dst_filename="beat_it")
    ydl_p.run()

    assert os.path.exists(CWD+"/default/beat_it.wav") == True
    print("YDL testting compete.")

if __name__ == "__main__":
    test_ydl()
