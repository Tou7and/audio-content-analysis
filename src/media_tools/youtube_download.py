""" Download media using youtibe-dl library """
import sys
import youtube_dl

AUDIO_OPTS = {
    'verbose': 8,
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

VIDEO_OPTS = {
    'verbose': 8,
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'noplaylist': True,
    'continue_dl': True,
    'writesubtitles': True,
    'subtitleslangs': ["en", "cn"],
    'writeautomaticsub': True,
    'postprocessors': [
        {
            'key': 'FFmpegVideoConvertor', # FFmpegVideoConvertor
            'preferedformat': 'mp4', # mp4, webm are the most common formats
        },
    ]
}

def download_from_url(url, opts=VIDEO_OPTS):
    try:
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            # print(info_dict["title"])
            # print(info_dict["id"])
            # print(info_dict["ext"])
            file_name = "{}-{}.{}".format(info_dict["title"], info_dict["id"], info_dict["ext"])
            print("[debug] {}".format(file_name))
            ydl.download([url])
        status = 0
    except Exception as e:
        print("-------- Error occurs ----------")
        print(e)
        print("--------------------------------")
        status = 1
        file_name = "none"

    return status, file_name 

def check_info(url, opts=VIDEO_OPTS):
    try:
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            print(info_dict["title"])
            print(info_dict["id"])
            print(info_dict["ext"])
        status = 0
    except Exception as e:
        # print(e)
        status = 1
    print("status: {}".format(status))

if __name__ == "__main__":
    url = sys.argv[1]
    # url = "https://www.youtube.com/watch?v=nr6Ma3H1NXo"
    # url = "https://www.youtube.com/watch?v=E1KkQrFEl2I"
    # download_from_url(url)
    check_info(url)
