# Background and design of mediacacherd

The code used for the transcoder is based on a sample from a [Ubuntu Wiki page][ubuntu-wiki-gstreamer] about porting a project to GStreamer 1.0.

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

# Testing

To upload a file with curl and save the returned transcoded file:

    $ curl -F file=@'source.flac' http://localhost:5000/api/transcode > dest.ogg

In a real client, the HTTP headers should be checked to make sure that the
transcode was actually successful.
