import os

from flask import Flask, jsonify, render_template, request, send_file
from flask_cors import CORS

from views.handler_document import create_document

app = Flask(__name__, template_folder="templates")
CORS(app)


@app.route("/", methods=["GET", "POST"])
def page():
    if request.method == "POST":
        data_form = request.form
        print(data_form)
        file = create_document(**data_form)
        return render_template("homepage.html", file=file)
    return render_template("homepage.html")


@app.route("/download/<file>", methods=["GET"])
def download(file):
    file = os.path.join("documents", file)
    try:
        if not os.path.exists(file):
            return jsonify({"error": "File not found"}), 404
        return send_file(file, as_attachment=True, download_name=os.path.basename(file))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
