# Paradux: a scheme to recover from maximum personal data disaster

This repo implements Paradux, the data recovery scheme outlined
[in this blog post](https://upon2020.com/blog/2019/01/paradux-a-scheme-to-recover-from-maximum-personal-data-disaster/).

Status: about the first version that does something useful, on the way to
[plan for V1](docs/v1-plan.md).

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
* Enter your datasets when prompted by `paradux edit-datasets`.
* Export your encrypted configuration with `paradux export-configuration`
  and store it in various on-line locations from where your stewards can
  recover it.
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
* Run `paradux recover`.

Want to help? Submit issues, pull requests, ... and/or get in touch! My contact info
is in the commit log.

