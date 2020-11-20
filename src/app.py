""" A Flask Web Application For Converting and Analysing Media Content """
import os
from uuid import uuid4
from flask import Flask, render_template, request, redirect, flash, url_for, send_file, session

from download_youtube import YoutubeDownloader
from run_analysis import run_analysis
from common import TMP_DIR, TEMPLATE_DIR

app = Flask(__name__)
app.config['SECRET_KEY'] = 'psychopass'

@app.route("/")
def index():
    """ Main entry point """
    title_text = "Welcome."
    f1_text = url_for("download_youtube", _external=True)
    f2_text = url_for("download_and_analysis", _external=True)
    return render_template("welcome.html", title=title_text, f1=f1_text, f2=f2_text)

@app.route("/return-file/")
def return_file():
    """ Return downloaded video/audio to client,
        or return results as table in an HTML page if analysis=True
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

    app.logger.info("----- YDL Returns ------")
    for key, val in results.items():
        app.logger.info("{}:{}".format(key, val))

    if results["status"] != 0:
        return "<h1> Error: Fail to download vidoe using Youtube-DL</h1>"

    location = results["media"]
    if session["analysis"]:
        results_html = os.path.join(TEMPLATE_DIR, session["id"]+".html")
        status_of_analysis, error_description = run_analysis(results["audio"], results_html)
        if status_of_analysis != 0:
            return "<h1> Fail to analyse audio content: {}</h1>".format(error_description)
        return render_template(session["id"]+".html")
    else:
        return send_file(location, attachment_filename=os.path.basename(location), as_attachment=True)

@app.route("/youtubedl/", methods=["GET", "POST"])
def download_youtube():
    title_text = "Download YouTube"
    if request.method == "POST":
        session["url"] = request.form.get('url')
        session["id"] = str(uuid4())
        session["format"] = request.form.get('format')
        session["filename"] = request.form.get('filename')
        session["analysis"] = False

        app.logger.info("------- Receive Session Data From User: -------")
        app.logger.info("URL : {}".format(session["url"]))
        app.logger.info("FORMAT : {}".format(session["format"]))
        app.logger.info("FILENAME : {}".format(session["filename"]))
        return redirect(url_for("return_file"))
    return render_template("url_download.html", title=title_text)

@app.route("/youtubedl/analysis", methods=["GET", "POST"])
def download_and_analysis():
    title_text = "Download YouTube and run analysis"
    if request.method == "POST":
        session["url"] = request.form.get('url')
        session["id"] = str(uuid4())
        session["format"] = "wav"
        session["filename"] = request.form.get('filename')
        session["analysis"] = True
        return redirect(url_for("return_file"))
    return render_template("url_download.html", title=title_text)

if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', port=5000)
