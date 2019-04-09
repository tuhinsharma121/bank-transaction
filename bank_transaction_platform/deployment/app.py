import os
import flask
from flask import Flask, request, jsonify
from bank_transaction_platform.src.read_pdf import ReadPDF

app = Flask(__name__)


@app.route('/')
def heart_beat():
    return flask.jsonify({"status": "ok"})


@app.route('/api/parse-trans', methods=['GET'])
def parse_transaction():
    print("Transaction parsing has been started .................")
    file_name = request.args.get("file")
    folder_name = "bank_statements"
    rp = ReadPDF()
    parsed_data = rp.parse_pdf(folder_name, file_name)
    return jsonify({"Categorized Transaction": parsed_data})

@app.route('/api/parse-transaction', methods=['POST'])
def post_transaction():
    file = request.files['files']
    current_dir = os.path.dirname(__file__)
    folder_name = "/tmp"
    file_name = "temp.pdf"
    file.save(os.path.join(current_dir, folder_name + "/" + file_name))
    rp = ReadPDF()
    parsed_data = rp.parse_pdf(folder_name, file_name)
    return_dict = {"Categorized Transaction": parsed_data}
    return jsonify(return_dict)


@app.route('/api/cat-trans', methods=['GET'])
def categorize_trasaction():
    print("Categorizing the transactions.....")
    file_path = request.args.get("path")
    rp = ReadPDF()
    parsed_data = "cbabk"
    return jsonify({"data": parsed_data})


@app.route('/api/parse-all', methods=['GET'])
def parsed_all_transaction():
    folder_name = request.args.get("path")
    rp = ReadPDF()
    parsed_data = rp.parse_all(folder_name)
    return str(parsed_data)


if __name__ == "__main__":
    app.run()
