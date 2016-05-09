package se.antoneliasson.mediacacherd

import java.nio.file.attribute.BasicFileAttributes
import java.nio.file.{SimpleFileVisitor, Path}

import scala.collection.mutable

class LibraryTraverser(val libraryRoot: Path) extends SimpleFileVisitor[Path] {
  var paths = new mutable.MutableList[Path]

  override def visitFile(file: Path, attr: BasicFileAttributes): Unit = {
    paths += file
  }
}
