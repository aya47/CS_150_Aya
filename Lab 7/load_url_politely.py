"""Load a URL politely."""

import re
import time
from os import mkdir
from os.path import exists
from urllib.parse import urlparse

import requests

requested_urls = []
MAX_URL_REQUESTS = 50


def load_url_politely(
    url: str,
    cache_file_name: str = "",
    ignore_cache: bool = False,
    print_debug: bool = False,
) -> str:
    """
    This is a function to do webscraping as politely as possible
    What does that mean?

    We check to see if we have requested anything
    from this site in the past N seconds
    so that we don't overwhelm the site with requests
    because we have a runaway loop (accidental DDS attack)

    When we request a site, we make a local "cached copy"
    and if we have a cached copy, we use that instead of asking the server.

    Caching is a super-important practical part of programming
    that we don't often talk about in CS!

    "Caching" means that rather than always requesting a resource,
    we keep a local copy and only update that copy when
    we think its out of date (cache invalidation)
    """
    if print_debug:
        print(f"--- LOAD URL: '{url}' (politely) ---")

    # Make a cache folder if we don't have one
    cache_dir = "cache"
    if not exists(cache_dir):
        if print_debug:
            print("\t...No cache directory yet, creating one")
        mkdir(cache_dir)

    # Set the initial last request time
    if not hasattr(load_url_politely, "last_request_time"):
        load_url_politely.last_request_time = -10

    # Generate a cache name, if we don't have one, by parsing the URL
    if not cache_file_name:
        parsed = urlparse(url)
        cache_file_name = parsed.netloc.split(".")[-2] + re.sub("[^0-9a-zA-Z]+", "_", parsed.path)
        if cache_file_name[-1] == "_":
            cache_file_name = cache_file_name[0:-1]

    file_path = f"{cache_dir}/{cache_file_name}.html"

    # Does this file already exist? Use the cache!
    if exists(file_path) and not ignore_cache:
        # Read from cache
        cached_html = open(file_path, encoding="utf-8").read()
        if print_debug:
            print(f"\t...Successfully loaded '{url}' from cache '{file_path}'")
        return cached_html

    # Cache doesn't exist? Load from real Wikipedia!

    # How long has it been since we made a request?
    current_time = time.process_time()
    time_elapsed = (current_time - load_url_politely.last_request_time) * 1000
    load_url_politely.last_request_time = current_time

    # If we made a request recently, wait 1 second before making a new request
    if time_elapsed < 100:
        if print_debug:
            print(
                f"\tLast request at time {load_url_politely.last_request_time:.5f}s, elapsed {round(time_elapsed)} ms ({url})"
            )
            print("\t*** Sleeping for 1 second ***")
        time.sleep(0.2)
        # return None

    # Add to total requests
    requested_urls.append(url)
    if len(requested_urls) > MAX_URL_REQUESTS:
        print("**** YOU MAY HAVE A BUG CAUSING TOO MANY URL REQUESTS: ****")
        print("**** FREEZING REQUEST ACCESS FOR SAFETY FOR THIS PROGRAM RUN ****")
        print("Last URLs requested: ", requested_urls)
        raise ValueError("Requested too many URLS")

    # Start a timeer
    start_request = time.process_time()

    # Attempt to read the URL from Wikipedia
    try:
        page_response = requests.get(url)

    # Deal with if the site is down or doesn't exist
    except Exception as e:
        print(f"\t*** ERROR: Could not connect to url: {url} ***")
        print(e)
        return ""

    # Stop the timer and calculate how long the request took
    stop_request = time.process_time()
    if print_debug:
        print(f"\tSuccessfully loaded from Wikipedia in {round((stop_request - start_request)*1000):4}ms:  {url}")

    # Save a cached copy
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(page_response.content))

    # Return the HTML content
    return page_response.content.decode()
