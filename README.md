# Paradux: a scheme to recover from maximum personal data disaster

This repo is intended for code that implements Paradux, the data
recovery scheme outlined
[here](https://upon2020.com/blog/2019/01/paradux-a-scheme-to-recover-from-maximum-personal-data-disaster/).

So far, there is no code to see here, because no code has been written yet :-)

But here's the plan for V1:

* It can all be much nicer and more user-friendly after V1. First
  we need to get it to work, and gain practical experience with
  running it. So the rest of this doc is only about V1.

* Command-line only.

* Implemented in Python3.

* A primary command `paradux` with subcommands, such as `paradux status`.
  Sub-commands should be "pluggable" without needing to modify the primary
  command; this makes it easy to experiment with subcommand alternatives.
  E.g. simply by adding the code implementing the subcommand in a particular
  directory, and `paradux` finding it there.

* All data that drives Paradux is contained in a single JSON file. This
  includes everything in the "Metadata Stash" described in the blog post,
  and whatever else is needed.

* This JSON file is stored in an encrypted LUKS file, with the credential
  required to decrypt being the "Operational Credential" from the post.

* `paradux edit` or such will:

  1. Ask the user for the Operational Credential.

  1. Decrypt and mount the LUKS file, in a way that only the current user
     can get at it (or such).

  1. Execute the file editor in `$EDITOR` on that JSON file.

  1. Upon edit abort, everything is aborted.

  1. Upon edit save of the editor, a syntax/structure check is performed.
     If invalid, the editor is re-invoked.

  1. Once syntax/structure check has passed, various configuration files
     are being generated, daemons started/restarted/etc so that by the
     time this command quits, Paradux runs according to the spec in the
     JSON file.

  1. A copy of the JSON file is encrypted and uploaded to the the metadata
     stashes defined in the JSON file.

  1. The LUKS filesystem is unmounted and the `cryptsetup` device mapping
     is removed.

* The JSON file describes the Replica Sets and each Data Stash in each
  Replica Set. (We may want to use different names for those things,
  because I'm told those are difficult-to-follow terms.)

* Just like the sub-commands should be pluggable, there should be a
  pluggable set of backup protocols, e.g. ftp, S3, disk, ...
  and common backup software like restic etc. Each Data Stash defined
  in the JSON file indicates which backup protocol to use.

* The JSON should also define frequencies of data transfer. Those drive
  generated `.timer` jobs for `.service`s that run periodically and
  perform the backup.

* One of the members of each Data Stash is a directory hierarchy on the
  machine that runs Paradux.

* One member of the Data Stash is defined as the source of the data.
  This member can be a local directory, or it can be accessed over
  the network via one of the pluggable backup protocols. For example,
  it could be my home directory on my laptop, accessible via
  `rsync` over `ssh`. In this case, Paradux pulls the data from the
  source Data Stash into the local directory hierarchy, and once
  that is done, it pushes it out to other Data Stashes. We probably
  want some policy parameters, such as how frequently that should
  occur.

* Encryption is generally done with `gpg` (could also be pluggable,
  however) and private keys are held in the JSON file. Public keys
  are saved in some suitable spots when `paradux edit` finishes, so
  the backup tasks can get at them.

* Some other commands:

  * `paradux setup`: initial setup. Will generate initial JSON file
     based on user input such as: number of stewards, how many stewards
     are required to recover, etc. Also will securely generate recovery
     keypair, split it into the right number of fragments, etc.
     Public and private key are stored in the JSON file.

  * `paradux create-steward-device(s)`: Will ask the user to insert a
     USB flash drive to which all necessary information is written
     for a steward. (This is in lieu of the sheet of paper that was
     assumed in the post. Seems like a better idea.)

  * `paradux status`: shows current system status, such as which backups
     have run last, etc.

Want to help? Get in touch! My contact info is in the commit log.

