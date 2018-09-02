# Rodent
A simple CLI utility that can add license headers to your files.

## Motives
Attempted using the Apache RAT https://creadur.apache.org/rat/apache-rat/index.html
and failed. Had to download the Java SDK, executed the thing and got a
Java stacktrace. I wanted a utility that would:

* mass insert Apache license headers throughout large code bases
* allow to break a build when a new file without header is introduced
  in the code base
