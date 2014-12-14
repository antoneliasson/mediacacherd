#!/usr/bin/env python3
from multiprocessing import Process
import os
from tempfile import mkstemp

from flask import Flask, request

from transcoder import Transcoder

app = Flask(__name__)

def transcode(in_fname):
    _, out_fname = mkstemp()
    # # om vi har för många jobb igång redan:
    # # return "how about no"?
    # # else:
    options = {
        'input' : in_fname,
        'output' : out_fname
    }
    transcoder = Transcoder(options)
    proc = Process(target=transcoder.run)
    proc.start()
    proc.join()
    return out_fname

@app.route('/api/transcode', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        _, in_fname = mkstemp()
        file = request.files['file']
        if file:
            file.save(in_fname)
            out_fname = transcode(in_fname)
            os.remove(in_fname)

            f = open(out_fname, 'rb')
            # Unlinking an opened file only works in Unix
            os.remove(out_fname)
            return f.read()
    else:
        return 'Invalid usage', 400

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
