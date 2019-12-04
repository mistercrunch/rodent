# Rodent
A simple CLI utility that can add license headers to your files.

## Motives
Attempted using the Apache RAT https://creadur.apache.org/rat/apache-rat/index.html
and failed. Had to download the Java SDK, executed the thing and got a
Java error.

# Features

* `rodent list`: lists the files that are in scope (git-aware, only includes
  files tracked by git)
* `rodent check`: allows to break a build when a new file without
  header is introduced in the code base, logs all non-compliant files
* `rodent apply`: mass inserts Apache license headers throughout large
   code bases

All commands receive a `-f` `--file-regex` argument that allow to filter
files that are affected.

## Limitations

* Currently only works for py/js/jsx, can easily be extended to support
  more file types
TEST
