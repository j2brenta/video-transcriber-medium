import time
from flask import Flask, render_template, request, jsonify
import os
import subprocess
from llama_cpp import Llama
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PATH_TO_SAVE_VIDEO = "./input-videos/"
CONVERTER_SCRIPT = "convert-mp4-to-text.py"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    filename = request.form.get('filename')
    language = request.form.get('language')
    
    path = filename + ".mp4"
    print(path)
    process = subprocess.Popen(['python3', CONVERTER_SCRIPT, '--convert-transcribe', '--language', language, path])
    process.wait()

    txt_file_path = "text/" + filename + ".txt"

    if os.path.exists(txt_file_path):
        # Return the transcript as a JSON response
        return jsonify({'transcript': open(txt_file_path).read()})
    else:
        return jsonify({'error': 'Error while processing, file not found.'})

@app.route('/summarize_text', methods=['GET', 'POST'])
def summarize_text():
    #filename = request.form.get('filename')
    start_time = time.time()
    token_count = 0

    filename = "2024-03-14-Sleep-Engineering"
    llama = Llama(
        model_path="../models/mistral-7b-instruct-v0.1.Q4_0.gguf",
        n_gpu_layers=16, # Uncomment to use GPU acceleration
      # seed=1337, # Uncomment to set a specific seed
        n_ctx=4096, # Uncomment to increase the context window
    )
    text = open("text/" + filename + ".txt").read()

    while True:
        output = llama(
            "Q: Summarize this text in just two paragraphs each 5-6 sentences long. " + text + " A: ",
            max_tokens=None,
            stop=["Q:", "\n"],
            echo=True
        )
        generated_text = output['choices'][0]['text']
        token_count += len(generated_text.split())
        print(f"Progress: {token_count} tokens generated, {time.time() - start_time:.2f} seconds elapsed")
        if "." in generated_text.strip().split()[-1]:
            break

    # Extract the generated text from the output dictionary, removing the initial prompt
    generated_text = generated_text.split("A: ", 1)[1]

    # Write the generated text to a file
    summary_file_path = "summary/" + filename + ".txt"
    with open(summary_file_path, 'w') as file:
        file.write(generated_text)

    return jsonify({'summary': generated_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)