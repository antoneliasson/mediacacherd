package se.antoneliasson.mediacacherd

import java.nio.file.Paths

import org.scalatest.{FlatSpec, Matchers}

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

  it can "sanitize metadata fields" in {
    // Invalid chars in ext4: NUL and /
    // Invalid chars in NTFS with Win32 namespace: NUL and \ / : * ? " < > |
    // Invalid chars in classic (8.3) FAT32: Many. I won't support this one.
    // Invalid chars in FAT32 with LFN: NUL
    // Invalid chars in HFS and HFS+: : or / (so let's ban both)
    // Source: https://en.wikipedia.org/w/index.php?title=Comparison_of_file_systems&oldid=635728858#Limits
    val ml = new MediaLoader("nothing")
    // should make this static
    ml.sanitizeField("! ' & ( ) = + , . _ $ \u0000 / \\ : * ? \" < > |") should be ("! ' & ( ) = + , . _ $ - - - - - - - - - -")
  }

  it should "properly sanitize invalid pathname chars and survive unicode" in {
    val ml = new MediaLoader("src/test/resources/sine ünicode+esçape.flac")
    ml.getPath should be(Paths.get("DJ- Escaped - chars-", "Love this album -3", "02 Sine wave with int. chars å, ä and ö.ogg"))
  }

  ignore should "ensure that the source contains the required metadata fields" in {

  }

  ignore should "ensure that the source contains the suggested metadata fields" in {

  }
}
