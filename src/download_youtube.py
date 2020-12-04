""" Given Video URL, run youtube-dl to retrieve its content """
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

MP3_OPTS = {
    'verbose': 1,
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'noplaylist': True,
    'continue_dl': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
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

class YoutubeDownloader:
    """ A Youtue downloader """
    def __init__(self, url, storage_dir=TMP_DIR, session_id="default", dst_format="mp4", dst_filename="default"):
        self.format = dst_format
        self.url = url
        process_id = session_id
        self.data_dir = os.path.join(storage_dir, process_id)
        self.make_datadir()

        if dst_format == "mp4":
            self.opts = MP4_OPTS
        elif dst_format == "mp3":
            self.opts = MP3_OPTS
        else:
            self.opts = WAV_OPTS
            self.format = "wav"

        if dst_filename == "default":
            self.opts['outtmpl'] = self.data_dir+'/%(title)s-%(id)s.%(ext)s'
            self.filepath = "default"
        else:
            self.opts['outtmpl'] = self.data_dir+'/'+dst_filename+'.%(ext)s'
            self.filepath = self.data_dir+'/'+dst_filename+'.'+self.format

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
            if self.filepath == "default":
                file_name = "{}-{}.{}".format(info_dict["title"], info_dict["id"], self.format)
                self.filepath = os.path.join(self.data_dir, file_name)

        if os.path.exists(self.filepath):
            self.results["media"] = self.filepath
            audio_path = decode_as_wavfile(self.filepath)
            self.results["audio"] = audio_path
            self.results["status"] = 0
        else:
            self.results["status"] = 1

if __name__ == "__main__":
    ydl_p = YoutubeDownloader(sys.argv[1], storage_dir=sys.argv[2])
