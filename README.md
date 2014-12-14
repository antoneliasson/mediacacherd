Mediacacherd
============

Mediacacherd caches media files! Currently audio files are supported.

Lets say you have a fairly large collection of nice losslessly encoded music.
You want to copy this collection, or parts of it, to your portable music player.
As the space is probably limited on this device, it's time to bring out a good
audio compressor. Vorbis in this example.

Encoding hundreds of gigabytes worth of FLAC music takes time. It is a massively
parallelizable task, since each track is encoded individually. We should be able
to spread it out over all available CPU cores, even if they are located in
different machines. For example, in my household there are 14 CPU cores that are
somehow connected to power and Ethernet. Let's put all of them to work!

## Dependencies

You need the Python 3 bindings for GObject introspection libraries. On Debian/Ubuntu this is the package `python3-gi`. You also need GStreamer 1.0 and its GObject introspection data. I'm not sure which packages are strictly necessary, but it should be a subset of the following so I recommend just installing all of them:

    gstreamer1.0-tools
    gir1.2-gstreamer-1.0
    gir1.2-gst-plugins-base-1.0
    gstreamer1.0-plugins-good
    gstreamer1.0-plugins-ugly
    gstreamer1.0-plugins-bad
    gstreamer1.0-libav

The `python3-gst-1.0` package is not used.

As these are installed system-wide, make sure to enable global site packages in
your Python virtualenv. The server is based on [Flask][]. You can install it in your virtualenv with pip:

    $ pip install flask

[flask]: http://flask.pocoo.org/
