""" A Flask Web Application For Converting and Analysing Media Content """
import os
import sys
import logging
from logging import FileHandler, StreamHandler
from logging.handlers import SMTPHandler
from uuid import uuid4
from flask import Flask, render_template, request, redirect, flash, url_for, send_file, session
from flask.logging import default_handler
from download_youtube import YoutubeDownloader
from media_tools.format_trans import segment
from run_analysis import AudioAnalyser
from common import TMP_DIR, TEMPLATE_DIR, SED_MODEL, DEEPSPEECH_CN, DEEPSPEECH_EN

app = Flask(__name__)
app.config['SECRET_KEY'] = 'psychopass'

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

audio_analyser = AudioAnalyser(SED_MODEL, DEEPSPEECH_EN, DEEPSPEECH_CN)

@app.route("/")
def index():
    """ Main entry point """
    title_text = "Youtube Downloader/Analyser"
    f1_text = url_for("download_youtube", _external=True)
    f2_text = url_for("analyse_youtube", _external=True)
    return render_template("welcome.html", title=title_text, f1=f1_text, f2=f2_text)

@app.route("/return-file/")
def return_file():
    """ Return downloaded video/audio to client,
        or return results as table in an HTML page if purpose = analyse
    """
    if session["format"] not in ["wav", "mp4", "mp3"]:
        raise ValueError("{} format not supoort for now".format(session["format"]))
    if session["filename"] == "":
        filename = "default"
    else:
        ## TODO: Remove symbol that may cause error
        filename = session["filename"]

    yt_dl = YoutubeDownloader(session["url"],
            TMP_DIR, session["id"], session["format"], filename)
    yt_dl.run()
    results = yt_dl.results

    logger.info("------------- Finish downloading Video -----------------------")
    for key, val in results.items():
        logger.info("{}:{}".format(key, val))

    if results["status"] != 0:
        return "<h1> Error: Fail to download vidoe using Youtube-DL</h1>"

    location = results["media"]

    if session["purpose"] == "analyse":
        logger.info("---------------- Start analysing Video --------------------")
        try:
            language = session["language"]
            results_html = os.path.join(TEMPLATE_DIR, session["id"]+".html")
            # status_of_analysis, error_description = run_analysis(results["audio"], results_html, asr_lang=language)
            status_of_analysis, error_description = audio_analyser.analyse_long_audio(results["audio"], results_html, language=language)
            if status_of_analysis != 0:
                return "<h1> Fail to analyse audio content: {}</h1>".format(error_description)
            return render_template(session["id"]+".html")
        except Exception as error:
            return "<h1> Error when analysing content: {} </h1>".format(error)

    elif session["start"] != "" or session["stop"] !="":
        try:
            segment_file = segment(location, start=session["start"], end=session["stop"])
        except Exception as error:
            app.logger.warning("Return full video instead of segment due to: {}".format(error))
        return send_file(segment_file, as_attachment=True)
        
    return send_file(location, as_attachment=True)
    # return send_file(location,
    #   attachment_filename=os.path.basename(location), as_attachment=True)

@app.route("/youtubedl/", methods=["GET", "POST"])
def download_youtube():
    """ Entry point for youtubedl """
    title_text = "Download YouTube Video/Audio"
    if request.method == "POST":
        session["url"] = request.form.get('url')
        session["format"] = request.form.get('format')
        session["filename"] = request.form.get('filename')
        session["start"] = request.form.get('start')
        session["stop"] = request.form.get('stop')
        logger.info("------------------------------------------------")
        logger.info("------- Receive Session Data From User: -------")
        logger.info("URL : {}".format(session["url"]))
        logger.info("FORMAT : {}".format(session["format"]))
        logger.info("FILENAME : {}".format(session["filename"]))
        logger.info("START : {}".format(session["start"]))
        logger.info("STOP : {}".format(session["stop"]))
        session["purpose"] = "download"
        session["id"] = str(uuid4())
        return redirect(url_for("return_file"))
    return render_template("url_download.html", title=title_text)

@app.route("/youtubedl/analysis", methods=["GET", "POST"])
def analyse_youtube():
    """ Entry point for youtubedl/analysis """
    title_text = "Get Video/Audio Analysis"
    if request.method == "POST":
        session["url"] = request.form.get('url')
        # session["kata"] = request.form.get('kata')
        session["language"] = request.form.get('language')
        logger.info("------------------------------------------------")
        logger.info("------- Receive Session Data From User: -------")
        logger.info("URL : {}".format(session["url"]))
        logger.info("LANGUAGE : {}".format(session["language"]))
        session["purpose"] = "analyse"
        session["id"] = str(uuid4())
        session["format"] = "wav"
        session["filename"] = "for_analyse"
        return redirect(url_for("return_file"))
    return render_template("url_analyse.html", title=title_text)

if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', port=5000)
