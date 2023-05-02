# download_copernicus_py
Python script to download data from Copernicus Open Access Hub

## Instructions

1. Need a file "product_urls.txt" which contains the urls retrieved from an API query in the same directory. One is provided for the TROPOMI_RPRO_XCH4 dataset.
2. Edit "download_copernicus_py" to modify the number of parallel downloads.
3. Run "python download_copernicus_py" in the same directory.
4. Check the created file "download_log.txt" for any errors.
5. Repeat the run as needed to validate a complete dataset.


## Features
- Run parallel file downloads.
- Writes a log to capture errors (incomplete downloads, corrupt files, rejected connections).
- Self-correcting. Validates local dataset on repeat runs by comparing filesizes with remote repository.
