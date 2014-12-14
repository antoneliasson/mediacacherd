Mediacacherd
============

Uploading a file with curl and saving the returned file:

    $ curl -F file=@'source.flac' http://localhost:5000/api/transcode > dest.ogg
