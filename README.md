# Paradux: recover from maximum personal data disaster

## What's this about?

Many of the residents of the towns that were wiped out recently by the
California wildfires did not have time to grab their laptops, bring their
hard disks, or take their password recovery sheets with them. Similarly,
what if your favorite cloud services simply kicked you off? Personal data
disasters lurk everywhere. If one hits you, could you recover your data
and your passwords?

Paradux is a new scheme, and supporting software, that stores your
personal data, and your passwords, in several different places that you
choose, so that:

* no third party can read it
* there are redundant copies of everything
* the effort for you to maintain the scheme is minimal, and
* you can recover even if you remember nothing and have full amnesia.

It does this with the help of cryptographic key splitting and trusted
friends. It applies to personal data, and secrets like passwords and
private keys.

## Linuxfest NorthWest 2019 presentation

The [Paradux presentation](https://lfnw.org/conferences/2019/program/proposals/264)
at Linuxfest Northwest 2019 was recorded! Here it is:

[![YouTube video](http://img.youtube.com/vi/Ld85wTh9uZs/0.jpg)](http://www.youtube.com/watch?v=Ld85wTh9uZs "YouTube video")

## Status

Version 0.2 is here. It's somewhat painful to use (edit JSON files!
Manually upload data! Bring your terminal skills! Linux only so far.)
but the most important functionality is working.

Help wanted! File an issue or submitting a PR is best.

## What's new in 0.2

* Renamed some terms: instead of "configuration" it is now "metadata". The
  names of the commands have changed accordingly
* Paradux now knows how to upload its metadata via scp and rsync over ssh,
  with new command `paradux publish-metadata`
* The data transfer protocols are pluggable, so it is really easy to add
  new ones. We are looking for somebody to implement "upload to Amazon S3"
  (see [issue](https://github.com/paradux/paradux/issues/18))
* To edit or display the metadata locations, there are new commands
  `paradux edit-metadata-locations` and `paradux status-metadata-locations`
* Some minor internal refactoring
* Various bug fixes

## Howto

[Installation instructions](docs/install.md). Note that:
* paradux depends on `cryptsetup` and thus only works on Linux.
  (Want to port to Windows or the Mac? Pull requests appreciated!)
* The edit functionality depends on the `EDITOR` environment variable being
  set to your favorite editor, such as `export EDITOR=/usr/bin/vi`.
* The following executables must be installed for upload: `ssh` and
  `rsync`.

There are some examples for the data files in [directory example-data](example-data/)

More details are in the most current presentation at
[upon2020.com/talks/paradux](https://upon2020.com/talks/paradux/).
