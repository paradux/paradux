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
* you can even recover if you remember nothing.

It does this with the help of key splitting and trusted friends. It
applies to personal data, and credentials.

## Linuxfest NorthWest 2019 presentation

We got to [present](https://lfnw.org/conferences/2019/program/proposals/264)
at Linuxfest Northwest, and they recorded it! Here it is:

[![YouTube video](http://img.youtube.com/vi/Ld85wTh9uZs/0.jpg)](http://www.youtube.com/watch?v=Ld85wTh9uZs "YouTube video")

## Status

Version 0.1 is here. It's somewhat painful to use (edit JSON files! Manually
upload data! Bring your terminal skills! Linux only so far.) but the
most important functionality is working.

Help wanted! File an issue or submitting a PR is best.

## Howto

[Installation instructions](docs/install.md). Note that paradux depends on
`cryptsetup` and thus only works on Linux. The edit functionality depends on
the `EDITOR` environment variable being set to your favorite editor, such
as `setenv EDITOR /usr/bin/vi`.

There are some examples for the data files:
* [datasets](example-data/datasets.json)
* [stewards](example-data/stewards.json)
* [user](example-data/user.json)

Here is a typical sequence to set up the scheme
* Create a new paradux configuration: `paradux init`. This will ask you
  to set your everyday password.
* Enter your datasets when prompted by `paradux edit-datasets`. See examples
  linked above.
* Export your encrypted configuration (automatically strips everyday password)
  with `paradux export-configuration` and store it in various on-line
  locations from where your stewards can recover it.
* Find a set of N stewards whom you trust. Enter their information when
  prompted by `paradux edit-stewards` (see example file above)
* Give your stewards their respective steward package. You export them with
  `paradux export-steward-packages`. Currently you need to manually add
  the location of your exported encrypted configuration.

To update the configuration:
* Edit your configuration again, and overwrite the uploaded encrypted
  configuration files with the new file.

To recover in case of disaster:
* Install paradux on a new machine
* From your stewards, find the location of one of the encrypted configuration
  files and download it
* Find at least three stewards (the number was configurable during
  init) and obtain their fragment of the recovery secret
* [For now](https://github.com/paradux/paradux/issues/8), assemble the
  information you got from the stewards into a JSON file.
* Run `paradux recover`.

