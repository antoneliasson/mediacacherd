package se.antoneliasson.mediacacherd

import java.io.File
import java.nio.file.{Path, Paths}

import org.jaudiotagger.audio.AudioFileIO
import org.jaudiotagger.tag.FieldKey

class MediaLoader(val source: String) {
  def getPath: Path = {
    val sourceFile = AudioFileIO.read(new File(source))
    val tag = sourceFile.getTag

    val fields = Seq(FieldKey.ARTIST, FieldKey.ALBUM, FieldKey.TRACK, FieldKey.TITLE)
      .map(key => sanitizeField(tag.getFirst(key)))
    val (artist, album, track, title) = fields match {
      case Seq(a, b, c, d) => (a, b, c, d)
    }

    Paths.get(artist, album, s"$track $title.ogg")
  }

  def sanitizeField(str: String): String = {
    str.replaceAll("\u0000|/|\\\\|:|\\*|\\?|\"|<|>|\\|", "-")
  }
}
