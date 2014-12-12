from flask import Flask
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

@app.route('/api/transcode', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return ''
        # skapa temporär fil
        # ladda upp
        # anropa transcode
        # returnera resultatet
    else:
        return 'Invalid usage'

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    print(Transcoder)
    app.run(debug=True)
