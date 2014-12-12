from tempfile import mkstemp

from flask import Flask, request

from transcoder import Transcoder

app = Flask(__name__)

def transcode(input_file):
    # input_file är en temporär fil
    # skapa ny temporär fil
    # omkoda
    # # om vi har för många jobb igång redan:
    # # return "how about no"?
    # # else:
    # # t = Transcode(temporär infil, temporär utfil)
    # # p = Process(target=t.run)
    # # p.start()
    # # p.join()
    # returnera omkodad fil
    pass


@app.route('/api/transcode', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        _, fname = mkstemp()
        file = request.files['file']
        if file:
            file.save(fname)
            # anropa transcode
            # returnera resultatet
            f = open(fname, 'rb')
            return f.read()
    else:
        return 'Invalid usage', 400

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
