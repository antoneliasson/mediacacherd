package se.antoneliasson.mediacacherd

import org.scalatest.{Matchers, FlatSpec}

class MediaLoaderSpec extends FlatSpec with Matchers {
  "A MediaLoader" should "hold a source filename" in {
    val ml = new MediaLoader("dir/test1.flac")
    ml.source should be ("dir/test1.flac")
  }

  it can "determine the target path for a media file" in {
    val ml = new MediaLoader("test1.flac")
    //ml.getPath() should be ("Artist/Album/01 Title.ogg")
  }

  ignore should "ensure that the source contains the required metadata fields" in {

  }

  ignore should "ensure that the source contains the suggested metadata fields" in {

  }
}
