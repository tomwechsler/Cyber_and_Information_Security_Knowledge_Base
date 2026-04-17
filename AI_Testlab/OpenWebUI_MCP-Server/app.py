from flask import Flask, request, jsonify, send_from_directory, make_response
import subprocess
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EXPORT_FOLDER = 'exports'
os.makedirs(EXPORT_FOLDER, exist_ok=True)

def run_tool(command, csv_filename=None):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        result = output.decode().splitlines()

        response_data = {
            'status': 'success',
            'results': result
        }

        if csv_filename:
            csv_path = os.path.join(EXPORT_FOLDER, csv_filename)
            with open(csv_path, 'w') as f:
                for line in result:
                    f.write(f"{line}\n")
            response_data['csv_download'] = f"/download/{csv_filename}"

        # Ensure OpenWebUI displays entire list
        response = make_response(jsonify(response_data))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'output': e.output.decode()}), 500

@app.route('/run-subfinder', methods=['POST'])
def run_subfinder():
    domain = request.get_json().get('domain')
    if not domain:
        return jsonify({'error': 'Domain not provided'}), 400
    filename = f"subfinder_{domain}.csv"
    return run_tool(['subfinder', '-d', domain, '-silent'], csv_filename=filename)

@app.route('/run-httpx-tech-detection', methods=['POST'])
def run_httpx_tech_detection():
    domains = request.get_json().get('domains')
    if not domains:
        return jsonify({'error': 'Domains not provided'}), 400
    with open('httpx_input.txt', 'w') as f:
        f.write('\n'.join(domains))
    return run_tool(['httpx', '-silent', '-l', 'httpx_input.txt'], csv_filename='httpx_output.csv')

@app.route('/run-gau', methods=['POST'])
def run_gau():
    domain = request.get_json().get('domain')
    if not domain:
        return jsonify({'error': 'Domain not provided'}), 400
    filename = f"gau_{domain}.csv"
    return run_tool(['gau', domain], csv_filename=filename)

@app.route('/run-waybackurls', methods=['POST'])
def run_waybackurls():
    domain = request.get_json().get('domain')
    if not domain:
        return jsonify({'error': 'Domain not provided'}), 400
    filename = f"wayback_{domain}.csv"
    return run_tool(['waybackurls', domain], csv_filename=filename)

@app.route('/run-nuclei', methods=['POST'])
def run_nuclei():
    urls = request.get_json().get('urls')
    if not urls:
        return jsonify({'error': 'URLs not provided'}), 400
    with open('nuclei_input.txt', 'w') as f:
        f.write('\n'.join(urls))
    return run_tool(['nuclei', '-l', 'nuclei_input.txt', '-silent'], csv_filename='nuclei_output.csv')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(EXPORT_FOLDER, filename, as_attachment=True)

@app.route('/.well-known/openapi.json')
def serve_openapi():
    return send_from_directory(os.path.join(app.root_path, 'static/.well-known'), 'openapi.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
