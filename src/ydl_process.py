""" URL --> MP4 --> WAV """
import os
import sys
import youtube_dl
from common import TMP_DIR
from media_tools.format_trans import decode_as_wavfile

WAV_OPTS = {
    'verbose': 1,
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'noplaylist': True,
    'continue_dl': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }]
}

MP4_OPTS = {
    'verbose': 1,
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'noplaylist': True,
    'continue_dl': True,
    'writesubtitles': True,
    'subtitleslangs': ["en", "cn"],
    'postprocessors': [
        {'key': 'FFmpegVideoConvertor', 'preferedformat': "mp4"}
    ]
}

class YDLProcess:
    """ A Youtue download process """
    def __init__(self, url, storage_dir, session_id, dst_format="mp4"):
        self.format = dst_format
        self.url = url
        process_id = session_id
        self.data_dir = os.path.join(storage_dir, process_id)
        self.make_datadir()

        if dst_format == "mp4":
            self.opts = MP4_OPTS
        else:
            self.opts = WAV_OPTS
        self.opts['outtmpl'] = self.data_dir+'/%(title)s-%(id)s.%(ext)s'

        self.results = {"status": -1, "video": "none", "audio": "none", "media": "none"}

    def make_datadir(self):
        """ Make directory to store media data """
        try:
            os.makedirs(self.data_dir)
        except Exception as error:
            raise RuntimeError(error)

    def run(self):
        """ Download video from channel and convert to WAV format.

        Status codes for results:
            -1: "Process initialed"
            0: "Process finished"
            1: "Fail to get content from channel"
        """
        with youtube_dl.YoutubeDL(self.opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(self.url, download=True)
            file_name = "{}-{}.{}".format(info_dict["title"], info_dict["id"], self.format)

        media_path = os.path.join(self.data_dir, file_name)
        if os.path.exists(media_path):
            self.results["media"] = media_path
            audio_path = decode_as_wavfile(media_path)
            self.results["audio"] = audio_path
            self.results["status"] = 0
        else:
            self.results["status"] = 1

def run_ydl_process(url, dst_dir=TMP_DIR, session_id="default", dst_format="mp4"):
    """ Run a youtube download process.
    Args:
        url: str, a youtube URL
        dst_dir: str, the dir to store the media files.

    Returns:
        results: dict, with status(int), video(str), audio(str)
    """
    ydl_process = YDLProcess(url, dst_dir, session_id, dst_format)
    ydl_process.run()
    return ydl_process.results

if __name__ == "__main__":
    run_ydl_process(sys.argv[1], dst_dir=sys.argv[2])
