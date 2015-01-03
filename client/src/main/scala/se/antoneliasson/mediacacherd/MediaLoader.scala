package se.antoneliasson.mediacacherd

import java.io.File
import java.nio.file.{Path, Paths}

import org.jaudiotagger.audio.AudioFileIO
import org.jaudiotagger.tag.FieldKey

class MediaLoader(val source: String) {
  def getPath: Path = {
    val sourceFile = AudioFileIO.read(new File(source))
    val tag = sourceFile.getTag

    val artist = tag.getFirst(FieldKey.ARTIST)
    val album = tag.getFirst(FieldKey.ALBUM)
    val track = tag.getFirst(FieldKey.TRACK)
    val title = tag.getFirst(FieldKey.TITLE)

    Paths.get(artist, album, s"$track $title.ogg")
  }
}
