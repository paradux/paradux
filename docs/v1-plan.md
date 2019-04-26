Plan for V1
===========

* It can all be much nicer and more user-friendly after V1. First
  we need to get it to work, and gain practical experience with
  running it. So the rest of this doc is only about V1.

* Command-line only.

* Implemented in Python 3. There is no goal to make it work with Python 2.

* A primary command `paradux` with subcommands, such as `paradux status-stewards`.
  Sub-commands are "pluggable" without needing to modify the primary
  command; this makes it easy to experiment with subcommand alternatives.
  E.g. simply by adding the code implementing the subcommand in a particular
  directory, and `paradux` finding it there.

* All data that drives Paradux is contained in JSON files, broken down so that it is
  unlikely that when the user edits one of them, they will accidentally screw up some
  other data.

* There may be some other JSON file(s) that aren't edited directly by the user

* One of the JSON files describes the DataSets and each data location in each
  DataSet. (We have started to use different names for those things than in the blog post,
  because I'm told those are difficult-to-follow terms.)

* Just like the sub-commands should be pluggable, there should be a
  pluggable set of backup protocols, e.g. ftp, S3, disk, ...
  and common backup software like restic etc. Each Data Location defined
  in the JSON file indicates which backup protocol to use.

* The JSON should also define frequencies of data transfer. Those drive
  generated `.timer` jobs for `.service`s that run periodically and
  perform the backup.

* One of the members of each Data Set is a directory hierarchy on the
  machine that runs Paradux.

* One member of the DataSet is defined as the source of the data.
  This member can be a local directory, or it can be accessed over
  the network via one of the pluggable backup protocols. For example,
  it could be my home directory on my laptop, accessible via
  `rsync` over `ssh`. In this case, Paradux pulls the data from the
  source Data Location into the local directory hierarchy, and once
  that is done, it pushes it out to other Data Locations. We probably
  want some policy parameters, such as how frequently that should
  occur.

* All JSON files are stored in an encrypted LUKS file.

* The encrypted LUKS file has two alternate secrets: the Everyday Passphrase,
  and the Recovery Secret.

* When exported to backup, the encrypted LUKS file has its Everyday Passphrase
  stripped, for added security.

* The recovery secret is a long, random integer that is only stored within the LUKS
  file (otherwise we can't create more shares for more Stewards) and conveyed as
  Shamir shares (i.e. only in pieces) to the Stewards.

