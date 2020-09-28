from flask import (
        Flask,
        request,
        jsonify,
        Response,
        )

# {
# Install the app
app = Flask('deepgram')
# }

MAXIMUM_AGE = 'max-age=%d' % (60 * 60 * 24 * 7)
NEW_TRACKS = {}
TRACKS = {}
IMAP_MAX = 1


class Track:
    def __init__(self, is_new, value=0):
        self.is_new = is_new
        self.value = value

def next_id():
    global IMAP_MAX
    id = IMAP_MAX
    IMAP_MAX = id + 1
    return id

def ip():
    return request.environ['REMOTE_ADDR']

@app.route('/sentinal/head')
def sentinal_head():
    print('*** CREATING NEW')

    track = Track(is_new=True, value=next_id())
    NEW_TRACKS[ip()] = track

    response = Response('')
    response.headers['Cache-Control'] = MAXIMUM_AGE
    return response

@app.route('/sentinal/<offset>')
def sentinal_identity(offset):
    offset = int(offset)

    # -
    if ip() in NEW_TRACKS:
        track = NEW_TRACKS[ip()]
    else:
        track = NEW_TRACKS[ip()] = Track(is_new=False)

    # -
    # Then we need to update the mask.
    if not track.is_new:
        track.value |= (1 << offset)

    if track.value & (1 << offset):
        age = 'no-cache'
    else:
        age = MAXIMUM_AGE

    print(offset, age)

    response = Response('')
    response.headers['Cache-Control'] = age
    return response

@app.route('/sentinal/tail')
def sentinal_tail():
    print('*** TAILED: %s' % (ip() in NEW_TRACKS))

    if ip() in NEW_TRACKS:
        name = '%s' % hex(NEW_TRACKS[ip()].value)
        del NEW_TRACKS[ip()]
    else:
        name = 'Unknown'

    print(name)

    response = Response('You are: %s' % name)
    response.headers['Cache-Control'] = 'no-cache'

    return response


@app.route('/')
def root():
    return '''
<html>
  <head>
    <link rel="stylesheet" href="http://localhost:5000/sentinal/head" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/0" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/1" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/2" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/3" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/4" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/5" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/6" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/7" />
    <link rel="stylesheet" href="http://localhost:5000/sentinal/tail" />
  </head>
</html>
'''

app.run(port=5000)
