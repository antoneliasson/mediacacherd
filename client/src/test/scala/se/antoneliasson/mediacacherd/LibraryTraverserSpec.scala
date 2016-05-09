package se.antoneliasson.mediacacherd

import java.nio.file.Paths

import org.scalatest.{FlatSpec, Matchers}

class LibraryTraverserSpec extends FlatSpec with Matchers {
  "A LibraryTraverser" can "create MediaLoaders for each file in a media library" in {
    val libraryRoot = Paths.get("src/test/resources/sourcedir")
    val lt = new LibraryTraverser(libraryRoot)
  }
}
