Mediacacherd
============

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
