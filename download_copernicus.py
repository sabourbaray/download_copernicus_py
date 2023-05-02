#!/usr/bin/env python3

import os
import urllib.parse
from multiprocessing import Pool
import time

# Define the number of parallel downloads
NUM_PARALLEL_DOWNLOADS = 2

# Define the URL file
URL_FILE = "product_urls.txt"

# Define the username and password
USERNAME = "s5pguest"
PASSWORD = "s5pguest"

# Define the log file
LOG_FILE = "download_log.txt"


def download_file(url):
    # Parse the URL to deal with escape characters
    escaped_url = url.rstrip().replace(")/$", ")/\\$")

    # Download the file
    num_connection_failures = 0
    while True:
        # Get the remote headers to check if the file already exists
        curl_head_command = f"curl --user {USERNAME}:{PASSWORD} -sI \"{escaped_url}\""
        remote_headers = os.popen(curl_head_command).read()

        # Extract the remote filename and file size from the headers
        remote_file_size = None
        remote_filename = None
        for header in remote_headers.split('\n'):
            if header.startswith('Content-Length:'):
                remote_file_size = int(header.split(': ')[1])
            elif header.startswith('Content-Disposition:'):
                remote_filename = header.split('"')[1]

        # Check if the file already exists with the correct size
        if remote_filename is not None and remote_file_size is not None:
            output_file = remote_filename
            if os.path.isfile(output_file):
                local_file_size = os.path.getsize(output_file)
                print("local filesize:",local_file_size,"remote filesize:",remote_file_size)
                if local_file_size == remote_file_size:
                    message = f"Skipping {url} - file already exists with correct size ({remote_file_size} bytes)"
                    with open(LOG_FILE, "a") as f:
                        f.write(f"{message}\n")
                    print(message)
                    return
                else:
                    os.remove(output_file)
                    message = f"File {output_file} exists but has incorrect size, downloading again"
                    # Log the result in the log file
                    with open(LOG_FILE, "a") as f:
                        f.write(f"{message}\n")
                    # Print the output
                    print(message)

        curl_command = f"curl --user {USERNAME}:{PASSWORD} -JLO --remote-header-name --location --retry-all \"{escaped_url}\""
        output = os.system(curl_command)

        # Determine the message based on the curl output code
        if output == 0:
            message = f"Downloaded {url} to {output_file} ({remote_file_size} bytes)"
            break
        elif output == 4606 or output == 14336:
            num_connection_failures += 1
            if num_connection_failures >= 2:
                message = f"Skipping {url} - connection failed twice in a row"
                break
            time.sleep(5)
        else:
            message = f"Error downloading {url}"
            break

    # Log the result in the log file
    with open(LOG_FILE, "a") as f:
        f.write(f"{message}\n")

    # Print the output
    print(output)
    print(message)


# Read the URLs from the URL file
with open(URL_FILE, "r") as f:
    urls = f.readlines()

# Download the files in parallel
with Pool(NUM_PARALLEL_DOWNLOADS) as p:
    p.map(download_file, urls)

