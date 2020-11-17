""" A Flask Web Application For Converting and Analysing Media Content """
import os
from uuid import uuid4
from flask import Flask, render_template, request, redirect, flash, url_for, send_file, session

from ydl_process import run_ydl_process
from analysis_process import run_analysis_process
from common import TMP_DIR, TEMPLATE_DIR

app = Flask(__name__)
app.config['SECRET_KEY'] = 'psychopass'

@app.route("/")
def index():
    """ Main entry point """
    return "<h1>Hello World!<h1>"

@app.route("/return-file/")
def return_file():
    """ Return downloaded video/audio to client """
    results = run_ydl_process(session["url"], TMP_DIR, session["id"], session["format"])

    for key, val in results.items():
        print("[debug] {}:{}".format(key, val))

    if results["status"] != 0:
        return "<h1> Error: [{}] </h1>".format(results["status"])

    location = results["media"]
    return send_file(location, attachment_filename=os.path.basename(location), as_attachment=True)

@app.route("/show-results/")
def show_results():
    """ Show anlysis results to client """
    results_html = os.path.join(TEMPLATE_DIR, session["id"]+".html")
    results = run_ydl_process(session["url"], TMP_DIR, session["id"], session["format"])
    status_of_analysis, error_of_analysis = run_analysis_process(results["audio"], results_html)
    app.logger.info(error_of_analysis)

    if status_of_analysis == 1:
        return "<h1> Fail when doing VAD </h1>"
    if status_of_analysis == 2:
        return "<h1> Fail when doing ASR </h1>"
    if status_of_analysis == 3:
        return "<h1> Fail to generate results </h1>"
    return render_template(session["id"]+".html")

@app.route("/youtubedl/wav", methods=["GET", "POST"])
def download_wavfile():
    title_text = "Download YouTube as WAV (sample rate = 16000)"
    if request.method == "POST":
        session["url"] = request.form.get('url')
        session["id"] = str(uuid4())
        session["format"] = "wav"
        return redirect(url_for("return_file"))
    return render_template("url_download.html", title=title_text)

@app.route("/youtubedl/mp4", methods=["GET", "POST"])
def download_video():
    title_text = "Download YouTube as MP4"
    if request.method == "POST":
        session["url"] = request.form.get('url')
        session["id"] = str(uuid4())
        session["format"] = "mp4"
        return redirect(url_for("return_file"))
    return render_template("url_download.html", title=title_text)

@app.route("/youtubedl/analysis", methods=["GET", "POST"])
def download_and_analysis():
    title_text = "Download YouTube and run analysis"
    if request.method == "POST":
        session["url"] = request.form.get('url')
        session["id"] = str(uuid4())
        session["format"] = "wav"
        return redirect(url_for("show_results"))
    return render_template("url_download.html", title=title_text)

if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', port=5000)
