# tenable-was2
```
**** This tool is not an officially supported Tenable project ***

Generates html reports for was2 scans from tenable.io using the json export APIs.

run with

python3 was2_exports.py
python3 gen2_html_reports.py

Keys should be placed in a file called keys.json. Format of file is
{"tio_AK":"your access key","tio_SK":"your secret key"}

Directory location for the keys file is controlled by the variable keys_dir

Raw json dump results will be written to the directory results_dir

html reports will be written to the directory reports_dir

```
