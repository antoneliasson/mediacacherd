package se.antoneliasson.mediacacherd

import java.nio.file.Paths

import org.scalatest.{Matchers, FlatSpec}

class MediaLoaderSpec extends FlatSpec with Matchers {
  "A MediaLoader" should "hold a source filename" in {
    val ml = new MediaLoader("dir/test1.flac")
    ml.source should be ("dir/test1.flac")
  }

  it can "determine the target path for a media file" in {
    // Not sure why the full path to the resource must be entered
    val ml = new MediaLoader("src/test/resources/sine.flac")
    ml.getPath should be (Paths.get("Artist", "Album", "01 Sine wave.ogg"))
  }

  ignore should "ensure that the source contains the required metadata fields" in {

  }

  ignore should "ensure that the source contains the suggested metadata fields" in {

  }
}
