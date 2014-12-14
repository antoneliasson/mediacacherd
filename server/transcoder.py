#!/usr/bin/python3
# Copyright 2014 Anton Eliasson
# Copyright 2012 Jason Gerard DeRose
# https://bazaar.launchpad.net/~jderose/+junk/gst-examples/view/head:/transcoder-1.0

from os import path

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

GObject.threads_init()
Gst.init(None)

class AudioEncoder(Gst.Bin):
    def __init__(self):
        super().__init__()

        # Create elements
        q1 = Gst.ElementFactory.make('queue', None)
        resample = Gst.ElementFactory.make('audioresample', None)
        convert = Gst.ElementFactory.make('audioconvert', None)
        rate = Gst.ElementFactory.make('audiorate', None)
        enc = Gst.ElementFactory.make('vorbisenc', None)
        q2 = Gst.ElementFactory.make('queue', None)

        # Add elements to Bin
        self.add(q1)
        self.add(resample)
        self.add(convert)
        self.add(rate)
        self.add(enc)
        self.add(q2)

        # Link elements
        q1.link(resample)
        resample.link(convert)
        convert.link(rate)
        rate.link(enc)
        enc.link(q2)

        # Add Ghost Pads
        self.add_pad(Gst.GhostPad.new('sink', q1.get_static_pad('sink')))
        self.add_pad(Gst.GhostPad.new('src', q2.get_static_pad('src')))

class Transcoder:
    def __init__(self, options):
        self.mainloop = GObject.MainLoop()
        self.pipeline = Gst.Pipeline()
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        # Create elements
        self.src = Gst.ElementFactory.make('filesrc', None)
        self.dec = Gst.ElementFactory.make('decodebin', None)
        self.audio = AudioEncoder()
        self.mux = Gst.ElementFactory.make('oggmux', None)
        self.sink =  Gst.ElementFactory.make('filesink', None)

        # Add elements to pipeline
        self.pipeline.add(self.src)
        self.pipeline.add(self.dec)
        self.pipeline.add(self.audio)
        self.pipeline.add(self.mux)
        self.pipeline.add(self.sink)

        # Set properties
        self.src.set_property('location', options['input'])
        self.sink.set_property('location', options['output'])

        # Connect signal handlers
        self.dec.connect('pad-added', self.on_pad_added)

        # Link elements
        self.src.link(self.dec)
        self.audio.link(self.mux)
        self.mux.link(self.sink)

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        self.mainloop.run()

    def kill(self):
        self.pipeline.set_state(Gst.State.NULL)
        self.mainloop.quit()

    def on_pad_added(self, element, pad):
        string = pad.query_caps(None).to_string()
        print('on_pad_added():', string)
        if string.startswith('audio/'):
            pad.link(self.audio.get_static_pad('sink'))

    def on_eos(self, bus, msg):
        print('on_eos()')
        self.kill()

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())
        self.kill()
