"""Write your own docstrings (including this one)!

Note that you can incorporate the given comments into your docstrings!
See docs.py for help and examples.

Author(s): Author 1, Author 2
Date: January 1, 2025
"""

# Import necessary modules
import os

# TODO: Define the necessary constants
# You will need constants for host id, host name, room type, price, min. number of nights, and license
# They can start with IDX_ or INDEX_, whatever you prefer

# Your code for constant definitions goes here


# TODO: Task 0: Read the data (including the first row, i.e. the column names)
def read_data(path_to_csv: str) -> list[list[str]]:
    """..."""
    # Your code goes here

    return []


# TODO: Task 1: Count the number of listings that are short-term rentals (their min. number of nights is < 30).
def count_short_term_rentals(data: list[list[str]]) -> int:
    """..."""
    # Your code goes here

    return 0


# TODO: Task 2: Count listings by their room type (ignore entries with an empty room type).
# Returns a dictionary with string keys and integer values. The keys are taken from the dataset (don't hardcode them).
# ** Note that the dict[str, int] format means a dictionary of [<key_type>, <value_type>] pairs. **
def count_listings_by_type(data: list[list[str]]) -> dict[str, int]:
    """..."""
    # Your code goes here

    return {}


# TODO: Task 3: Count the number of listings by their license type (licensed, unlicensed, pending, or exempt) (*do* hardcode the keys here).
# Returns a dictionary with string keys and integer values. The keys are "unlicensed", "pending", "exempt", "licensed".
def get_license_status(data: list[list[str]]) -> dict[str, int]:
    """..."""
    # For consistency of grading, let's assume that:
    # 1. An entry that is empty is considered unlicensed
    # 2. An entry that has 'pending' anywhere in the license is considered pending (case insensitive)
    # 3. An entry that has either '32+', '32-', '32 +', or '32 -' in the license is considered exempt
    # 4. Anything that is neither pending nor exempt nor unlicensed is considered licensed
    #
    # Some of your values might be different from those on Inside Airbnb, but pending and unlicensed should match

    # Your code goes here

    return {}


# TODO: Task 4: Count the number of listings that are by hosts who have multiple listings.
# Returns the number of listings by hosts with multiple listings (they have > 1 listing).
#
# Refer to the "Listings Per Hosts" section on https://insideairbnb.com/chicago/.
# We are looking for what is referred to as the number of multi-listings.
def count_multi_listings(data: list[list[str]]) -> int:
    """..."""
    # Your code goes here

    return 0


# TODO: Task 5: Count the number of listings that are by hosts who have i listings, where 0 <= i <= 10.
# Returns a list of 11 integers where for every number i from 0 to 10...
#   the element at index i describes how many listings are from hosts with i listings.
#   * At index i, list[i] is how many listings are by hosts with i listings.
#   * At index 4, list[4] is how many listings are by hosts with 4 listings.
#   * At index 10, list[l0] is how many listings are by hosts with >= 10 listings.
#
# Refer to the bar diagram titled "Listings Per Host" on https://insideairbnb.com/chicago.
def count_listings_by_host_count(data: list[list[str]]) -> list[int]:
    """..."""
    listing_counts = [0] * 11  # [0, 0,...0]

    # Your code goes here

    return listing_counts


# TODO: Task 6: Return a list containing listing prices, excluding empty prices.
# The room type is an optional parameter. It's what to filter the listings by.
# * If not specified, consider all listings.
# * If specified (e.g. "Entire home/apt"), then consider only listings with that room type.
#
# Optional meaning that the function can be called like:
#   get_prices(data, "Entire home/apt")
# or:
#   get_prices(data)
# In the second case, the room_type will default to ""
def get_prices(data: list[list[str]], room_type: str = "") -> list[float]:
    """..."""
    # room_type: str = "" means room_type is a str that
    # when not provided will be set to ""
    #
    # Setting empty prices to $0 will yield website results
    # Thus, the website average should be lower
    # Don't worry about this, skip empty prices instead

    # Your code goes here

    return []


# TODO: Task 7: Get the host name associated with the given query_id.
# Returns the host name or "Name not found" if there is no host with that query_id.
def get_host_name_by_id(data: list[list[str]], query_id: str) -> str:
    """..."""
    # Your code goes here

    return "Name not found"


# TODO: Task 8: Get the number of listings per host.
# Returns a dictionary where the keys are strings denoting host ids and the values are integers denoting each host's listing count.
# The room type is an optional parameter. It's what to filter the listings by (same as task 6).
# * If not specified, consider all listings.
# * If specified (e.g. "Entire home/apt"), then consider only listings with that room type.
def listings_per_host_with_type(data: list[list[str]], room_type: str = "") -> dict[str, int]:
    """..."""
    # Your code goes here

    return {}


def run_test_code() -> None:
    """Test the code.

    This is your scratchpad. Do not write any code outside of this
    function or outside of any of the other functions written above.
    """
    # Checking your current working directory
    # Making sure that you have the csv file in this folder
    working_directory = os.getcwd()
    print("-" * 60)
    print("Current working directory: ", working_directory)
    print("-" * 60)
    print("files in this directory")
    for filename in os.listdir():
        if not filename.startswith("."):
            print(" ->", filename)

    FILE_NAME_INPUT = "chicago_listings.csv"
    FILE_NAME_OUTPUT = "report.txt"

    assert FILE_NAME_INPUT in os.listdir(), "check that you have downloaded all files"

    print("-" * 60)
    print("Testing code and generating report for " + FILE_NAME_INPUT)

    f = open(FILE_NAME_OUTPUT, "w")
    f.write("*" * 31)
    f.write(f"\nREPORT FOR {FILE_NAME_INPUT}\n")
    f.write("(Data as of December 18, 2024)\n")
    f.write("*" * 31)

    # # Test Task 0
    # listings = read_data(FILE_NAME_INPUT)[1:]  # We skip the first row here
    # n = len(listings)
    # assert isinstance(listings[0], list), "listings should be a list of lists"
    # assert isinstance(listings[0][1], str), "listings should be a list of lists of strings"
    # assert n > 0, "listings should have at least one entry"
    # f.write(f"\n\nTotal listings: {n:,}\n")

    # # Test Task 1
    # strs = count_short_term_rentals(listings)
    # assert isinstance(strs, int), "count_short_term_rentals() should return an integer"
    # f.write("\nListings that are:")
    # f.write(
    #     f"\nShort-term rentals : {strs:,} ({round(((strs/n)*100),1)}%)"
    #     f"\nLonger-term rentals: {n-strs:,} ({round((((n-strs)/n)*100),1)}%)\n\n"
    # )

    # # Test Task 2
    # listings_type = count_listings_by_type(listings)
    # assert isinstance(listings_type, dict), "count_listings_by_type should return a dictionary"
    # assert "Private room" in listings_type, "count_listings_by_type should include string keys 'Private room'"
    # assert sum(list(listings_type.values())) == len(listings), "all listings should be accounted for"
    # f.write("Listings with room type:\n")
    # for listing, count in sorted(listings_type.items(), key=lambda item: -item[1]):
    #     f.write(f"{listing:<15}: {count:,} ({round(((count/n)*100),1)}%)\n")

    # # Test Task 3
    # license_status = get_license_status(listings)
    # assert isinstance(license_status, dict), "get_license_status should return a dictionary"
    # assert "exempt" in license_status, "get_license_status should have string keys 'licensed', 'unlicensed', 'exempt',and 'pending'"
    # assert sum(list(license_status.values())) == len(listings), "check the values returned by get_license_status"
    # unlicensed = license_status["unlicensed"] + license_status["pending"]
    # f.write(
    #     f"\nNumber of unlicensed current listings, at least {unlicensed:,} ({round(((unlicensed/n)*100),1)}%); "
    #     f"including {license_status['unlicensed']:,} with missing license and {license_status['pending']:,} pending\n"
    # )

    # for status, count in sorted(license_status.items(), key=lambda item: -item[1]):
    #     f.write(f"{status:<10}: {count:,}\n")

    # # Test Task 4
    # multihosts = count_multi_listings(listings)
    # assert isinstance(multihosts, int), "count_multi_listings should return an integer"
    # f.write(
    #     f"\nNumber of listings by hosts with multiple listings: {multihosts:,} out of {n:,} total listings "
    #     f"({round(((multihosts/n)*100),1)}%)\n\n"
    # )

    # # Test Task 5
    # counts = count_listings_by_host_count(listings)
    # assert counts[0] == 0, "No host has 0 listings, otherwise they wouldn't be in the data"
    # assert counts[1] == len(listings) - count_multi_listings(listings), "Single listing count incorrect"

    # assert sum(counts) == len(listings), "Number of listings per hosts computed incorrectly"
    # f.write(f"Listings by hosts with 1 listing   : {counts[1]:,}\n")
    # for i in range(2, len(counts) - 1):
    #     f.write(f"Listings by hosts with {i} listings  : {counts[i]:,}\n")
    # f.write(f"Listings by hosts with 10+ listings: {counts[10]:,}\n")

    # # Test Task 6
    # prices = get_prices(listings)
    # assert isinstance(prices, list), "get_prices should return a list"
    # assert isinstance(prices[0], float), "get_prices should return a list of floats"

    # f.write("\n-----Analyzing prices-----\n")

    # f.write(f"{len(prices):,} prices in the list\n")
    # if len(prices) > 0:  # Avoiding division by 0
    #     average = sum(prices) / len(prices)
    #     f.write(f"Average listing price ${average:.02f}\n")
    #     f.write(f"Median listing price  ${statistics.median(prices):.02f}\n")

    # f.write("\n")
    # home_prices = get_prices(listings, "Entire home/apt")
    # f.write(f"{len(home_prices):,} prices for Entire home/apt\n")
    # if len(home_prices) > 0:  # Avoiding division by 0
    #     average = sum(home_prices) / len(home_prices)
    #     f.write(f"Average entire apt price ${average:.02f}\n")
    #     f.write(f"Median entire apt price  ${statistics.median(home_prices):.02f}\n")

    # # TODO: Test Task 7
    # # Add at a call to get_host_name_by_id and at least three assert statements
    # # Your code goes here

    # # Test Task 8
    # # Get names of hosts and their listings
    # listing_counts = listings_per_host_with_type(listings)
    # assert sum(list(listing_counts.values())) == len(listings), "Number of listings per host computed incorrectly"
    # # Get top ten listing counts
    # top_hosts = sorted(listing_counts.items(), key=lambda item: item[1], reverse=True)[:10]
    # f.write(f"\n-----Top {len(top_hosts)} hosts with the largest number of listings-----\n")
    # for host_id, count in top_hosts:
    #     f.write(f"{get_host_name_by_id(listings, host_id):<17} has {count}\n")

    # listing_counts = listings_per_host_with_type(listings, "Entire home/apt")
    # top_hosts = sorted(listing_counts.items(), key=lambda item: item[1], reverse=True)[:10]
    # f.write(f"\n-----Top {len(top_hosts)} hosts with largest number of entire home listings-----\n")
    # for host_id, count in top_hosts:
    #     f.write(f"{get_host_name_by_id(listings, host_id):<17} has {count}\n")

    f.close()

    # Display report to the user
    print("-" * 60)
    print("Report has been written to", FILE_NAME_OUTPUT)
    print("-" * 60 + "\n")
    with open(FILE_NAME_OUTPUT, "r") as file:
        print(file.read())


# Skip the test code if we are running this as a *module* (i.e. when we are grading it)
# Otherwise, run your test code!
if __name__ == "__main__":
    run_test_code()
