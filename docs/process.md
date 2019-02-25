Process
=======

Init
----

Set up a new Paradux configuration from scratch. This will:
* setup an encrypted store for the Paradux Configuration Data Master
* setup the Day-to-Day Password
* generate a Recovery Key
* split the Recovery Key into fragments

It will not:
* configure User Datasets
* configure Configuration Data Backups
* distribute anything to Stewards

How to:
* `paradux init`


Status
------

Reports on the status of the system, such as:
* where Configuration Data and User Data resides etc.
* when a backup was last performed (? Can this be done?)

How to:
* `paradux status`


Add/modify User Datasets, User Dataset Locations or User Dataset Backup Locations
---------------------------------------------------------------------------------

How to:
* `paradux edit`


Add/modify Configuration Data Backup Locations
----------------------------------------------

How to:
* `paradux edit`


Provide necessary information to Stewards
-----------------------------------------

How to:
* `paradux print-steward-package` or `paradux export-steward-package`
* Then convey the printed paper, or saved USB stick to the Steward.
