# Background and design of mediacacherd

## Server

There are basically two good open source media transcoding softwares out there
that I'm aware of: GStreamer and ffmpeg/avconv. GStreamer is widely used, seems
to be well-maintained and has bindings for many languages. It seems that nobody
is really using ffmpeg in their multimedia processing code. Most examples I've
seen just construct command lines and execute them in a shell. I believe that
it's really hard to make a good program based on subprocessing external programs
and parsing their output, so I'd like to avoid that. Furthermore, I have some
previous experience in creating simple GStreamer pipelines, so GStreamer is what
I chose for the server.

I really want a reason to do a Scala project soon. Unfortunately there seems to
be no good Java/Scala bindings for GStreamer 1.0. There is an unmaintained
project that has developed Java bindings for GStreamer 0.10[[1]][gstreamer-java],
but I'm not looking to start a new project based on legacy code.
[As his GSoC project for 2014, a guy][gsoc-gstreamer-java] started to rewrite
the gstreamer-java bindings for GStreamer 1.0, but I could never get his code to
compile. So, for the server I settled with Python, which has good bindings for
GStreamer 1.0.

The code used for the transcoder is based on a sample from a [Ubuntu Wiki page][ubuntu-wiki-gstreamer] about porting a project to GStreamer 1.0.

[gsoc-gstreamer-java]: https://www.google-melange.com/gsoc/project/details/google/gsoc2014/octachoron/5738600293466112
[gstreamer-java]: https://code.google.com/p/gstreamer-java/
[ubuntu-wiki-gstreamer]: https://wiki.ubuntu.com/Novacut/GStreamer1.0 "Novacut/GStreamer1.0 -- Ubuntu Wiki"

Because the number of concurrent jobs will be fairly low (around the number of
CPU cores in the machine), even though they take a significant amount of time to
process, I've opted to make the server handle requests synchronously. The
backend will only be used by computers, not humans, so there is not much need
for a fancy progress indicator during the upload. The requester should be happy
to wait for the result, which might take tens of seconds to process.

For the same reasons I've opted for the simple approach of letting the web
server spawn a new worker process for every incoming request. A more scalable
solution is probably to split the server into two applications that are
communicating through a queuing system like Redis. Again, the frequency of
submitted jobs is expected to be fairly low so there will not be any problems
with the web server running out of resources.

There will probably be a short duration between jobs where one CPU core is not
doing anything useful because the client is busy downloading the resulting file
and uploading the next job, occupying a worker process. The simple workaround is
to overload the server slightly, by submitting a few more jobs than there are
CPU cores available and letting the operating system schedule all of them to run
concurrently. The number of concurrent jobs then varies between *n* and *n + o*,
instead of between *n - o* and *n*, where *n* is the number of cores and *o* is
the overload constant. When a new job is submitted and the number of running
jobs are equal to *n + o*, the web server should respond with a HTTP 503 Service
Unavailable.

The web server could simply use multiple processes and handle the heavy
processing itself, but as I want the number of concurrent jobs to be variable
depending on how much overloading is allowed, I opted to make it threaded
instead and letting the web server spawn or fork a new process when a job is
submitted.

## Client

The client doesn't care about the audio stream, it just needs to read the
metadata (writing metadata is not necessary). This is easier to find Java/Scala
libraries for. I found two good candidates: [VorbisJava][] and [jaudiotagger][].

[VorbisJava]: https://github.com/Gagravarr/VorbisJava
[jaudiotagger]: http://www.jthink.net/jaudiotagger/index.jsp

VorbisJava seems more capable, but also more complex. There are no official
up-to-date binaries, so it would have to be bundled with this project. It does
not seem to have any code for detecting the media container file type. It can
apparently be integrated in Apache Tika, which seems to be able to detect and
parse anything containing text in some form. But this is another thick
abstraction layer I don't feel like deploying and learning.

The jaudiotagger project was created in 2005 and is still maintained so it
should be pretty stable by now. If the commercial is correct it can decode all
interesting audio containers. It has functionality to abstract away the
different names of field names with the same function in different tagging
formats. Updated binary releases are available in VCS. A not that out-of-date
Maven repository is also available.

Both were fairly easy to get running. Because of its advantages listed above,
I'll use jaudiotagger for now.

### GUI

The Scala bindings for Swing reportedly work well. However, as
[JavaFX is intended to replace Swing][javafx-replace-swing] in the long run, I'd
prefer to base my new project on that instead. [ScalaFX][] is a Scala wrapper
for JavaFX that is also [reportedly nice][stackoverflow-scala-gui]. JavaFX is
included in Java SE as of JDK 7u6, but is [broken][javafx-maven-classpath]
(see also [this][guigarage-javafx-maven] and [this][stackoverflow-maven-javafx]) in Java 7 and is
[not included][github-scalafx-bug] in Debian's and Ubuntu's OpenJDK packages. As
nobody likes maintaining legacy software, I doubt this will ever be solved.

[javafx-replace-swing]: http://www.oracle.com/technetwork/java/javafx/overview/faq-1446554.html#6 "JavaFX FAQ: 6. Is JavaFX replacing Swing as the new client UI library for Java SE?"
[scalafx]: http://www.scalafx.org/
[stackoverflow-scala-gui]: http://stackoverflow.com/a/24214379/2756984
[javafx-maven-classpath]: http://zenjava.com/javafx/maven/fix-classpath.html
[guigarage-javafx-maven]: http://www.guigarage.com/2012/10/building-javafx-applications-with-maven/
[stackoverflow-maven-javafx]: https://stackoverflow.com/questions/15278215/maven-project-with-javafx-with-jar-file-in-lib
[github-scalafx-bug]: https://github.com/scalafx/scalafx/issues/141

JavaFX seems to be more [correctly included in][wp-javafx-8] Java 8 (compare
"bundled with" with "part of"). Perhaps it even works. OpenJDK 8
[is not yet packaged][ubuntu-trusty-java-8] for Ubuntu 14.04.

[wp-javafx-8]: https://en.wikipedia.org/wiki/JavaFX#JavaFX_8
[ubuntu-trusty-java-8]: https://bugs.launchpad.net/ubuntu/+source/openjdk-8/+bug/1341628

So I built OpenJDK 8 with OpenJFX from source with the help of guides
[1][obuild-openjfx] and [2][obuild-package] in cleanroom environment (newly
installed Ubuntu 14.04 amd64 VM). I did not get any JavaFX libs in the result.

[obuild-openjfx]: https://github.com/hgomez/obuildfactory/wiki/How-to-build-and-package-OpenJDK-8-with-OpenJFX-on-Linux
[obuild-package]: https://github.com/hgomez/obuildfactory/wiki/How-to-build-and-package-OpenJDK-8-on-Linux

Next alternative: Install Oracle Java 8. I used [Web Upd8's PPA][webupd8-java].
Everything works now. I would imagine that one could also update Ubuntu to a
version that ships OpenJDK 8 (with [OpenJFX separately][udeb-openjfx]) in the
official repositories (>=14.10).

[webupd8-java]: http://www.webupd8.org/2012/09/install-oracle-java-8-in-ubuntu-via-ppa.html
[udeb-openjfx]: http://packages.ubuntu.com/utopic/openjfx

# Testing

To upload a file with curl and save the returned transcoded file:

    $ curl -F file=@'source.flac' http://localhost:5000/api/transcode > dest.ogg

In a real client, the HTTP headers should be checked to make sure that the
transcode was actually successful.
