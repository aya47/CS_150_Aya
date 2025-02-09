"""
In this lab we will read a CSV and a JSON file and answer queries about the most dogs in NYC.

Some syntax you will need for this assignment
* Checking if an element is already in a list: "if elem in my_list"
* Casting a csv.reader to a list
        list(csv.reader(f))
* Once we discuss list comprehensions, consider using list comprehensions where appropriate.
"""

import os
import csv 
import json 

# -----------------------------------------------------------------------------
# ---------------------------------- INDEXES ----------------------------------
# -----------------------------------------------------------------------------

# Indexes to use with dog_breed_characteristics.csv (breeds, breed_data) ONLY!
INDEX_BREED_NAME = 0
INDEX_BREED_ALT_NAME = 1
INDEX_BREED_WEIGHT = 4
INDEX_BREED_TEMPERAMENT = 5
INDEX_BREED_PRICE = 6
INDEX_BREED_INTELLIGENCE = 7
INDEX_BREED_WATCHDOG = 8

# Indexes to use with nyc_dogs.json (dogs, dog_data) ONLY!
INDEX_DOG_ID = 0
INDEX_DOG_NAME = 1
INDEX_DOG_SEX = 2
INDEX_DOG_BIRTHYEAR = 3
INDEX_DOG_BREED = 4
INDEX_DOG_ZIPCODE = 6


# -----------------------------------------------------------------------------
# ------------------------------ HELPER FUNCTIONS -----------------------------
# -----------------------------------------------------------------------------


def is_breed_match(name: str, query: str) -> bool:
    """Test if these breed names match.

    Args:
        name (str): The name of a breed.
        query (str): The name of a breed.

    Returns:
        bool: True if the name matches or partially matches the query (ignoring case)
        False otherwise.
    """
    # Empty strings don't count as a match for this
    # because they would occur in *any* other string
    if query == "" or name == "":
        return False
    return name.upper() in query.upper() or query.upper() in name.upper()


def dog_to_string(dog_data: list[str]) -> str:
    """Turn a list of dog data into a string that is more human-readable.

    Args:
        dog_data (list[str]): A list of strings representing a single NYC dog (e.g. ["Rocko", "Chihuahua",...]).

    Returns:
        str: A string in the format "NAME (BREED) ZIPCODE" e.g. "Rocko (CHIHUAHUA) 10035".
    """
    return f"{dog_data[INDEX_DOG_NAME]} ({dog_data[INDEX_DOG_BREED]}) {dog_data[INDEX_DOG_ZIPCODE]}"


# -----------------------------------------------------------------------------
# ----------------------------------- TASKS -----------------------------------
# -----------------------------------------------------------------------------


def read_breed_data(path_to_csv: str) -> list[list[str]]:
    """Open a CSV file at the given path, read in the lines, and return a list of lists.

    (You can use "with" syntax or not, but don't change the path).
    Use the CSV module to create a CSV "reader" (don't use readlines()).
    Cast it to a list before returning, as CSV reader objects aren't lists
    when they are read. More information here (https://realpython.com/python-csv/).

    Args:
        path_to_csv (str): A relative path to the breed information comma-separated value file.

    Returns:
        list[list[str]]: A list of lists of str [["Affenpinscher","","Toy"], ...[more breed data]]
        representing all known dog breeds. Note that each item in the list represents info about 1 breed.
    """
    # TODO: TASK 0: load all breed data
    # Your code goes here
    # Casting to a list of lists

    # Open the CSV file and use csv.reader
    with open(path_to_csv, "r") as file:
        reader = csv.reader(file)
        # Cast the reader (iterator) to a list
        dog_breed = list(reader)

    return dog_breed

#read_breed_data('dog_breed_characteristics.csv')

def read_dog_data(path_to_json: str) -> list[list[str]]:
    """Open a JSON file of dog data at the given path, read in the lines, and return a list of lists.

    Use the JSON module to "load" the files contents into data (in this case, a list).
    More on how to use Python's json library https://www.geeksforgeeks.org/json-load-in-python/.

    Args:
        path_to_json (str): A relative path to the nyc dog json file.

    Returns:
        list[list[str]]: A list of lists of str [[Rocko, Chihuahua,...], ..., [<some dog data>]]
        representing all dogs registered in NYC. Note that each item in the list represents 1 (real life) dog.
    """
    # TODO: TASK 1: load all dog data
    with open(path_to_json, "r") as file: 
        dog_nyc = json.load(file)

    # Your code goes here
    return dog_nyc

x = read_dog_data("nyc_dogs_small.json")
print(x)

def get_breed_data_by_name(breeds: list[list[str]], query_name: str) -> list[str] | None:
    """Get the first list of breed information from breeds that matches (ignoring case) the query name.

    Look at each breed in breeds. Use the "is_breed_match" helper function above to compare this breed's name
    against the query name. When you find a breed whose name matches the query, return the breed's data (a list).
    - get_breed_data_by_name(breeds, "poodle") -> ['Poodle', Œ'', 'Non Sporting', 'Gun', '26', 'Active,
        Alert, Faithful, Instinctual, Intelligent, Trainable','1250', '2', '4', '', '', '1', '7']
    - get_breed_data_by_name(breeds, "zoodle") -> None

    Args:
        breeds (list[list[str]]): A list of breeds information.
        query_name (str): A name of a breed ("CHIHUAHUA", "Welsh corgi").

    Returns:
        list[str] | None: A list of str ["Corgi","","Herding"...] with a breed name that matches the query.
        Or None if no match is found.
    """
    # This is an assert that will fail if something unexpected is passed as an argument to this function
    # Asserts like these will inform you if a user calls this function incorrectly
    # "isinstance(var, some_type)" is the same as "some_type == type(var)"
    assert isinstance(
        query_name, str
    ), f"expected 'query_name' argument to be str, got {type(query_name)}{query_name}"

    # TODO: TASK 2: get breed data by breed name

    # Your code goes here

    return []  # if match is found, return None if match is not found


def get_breed_data_for_dog(breeds: list[list[str]], dog_data: list[str]) -> list[str] | None:
    """Get the first list of breed information, e.g. ["Corgi","","Herding"...], in breeds.

    Args:
        breeds (list[list[str]]): A list of breeds information.
        dog_data (list[str]): A list of strings representing a single NYC dog (e.g. ["Rocko", "Chihuahua",...]).

    Returns:
        list[str] | None: A list of str ["Chihuahua","","Toy","Companion"...] with a breed name that
        matches the breed name in the dog_data. This represents the breed associated with the given dog.
        Or None if no match is found.
    """
    assert isinstance(
        dog_data, list
    ), f"expected 'dog_data' to be list, got {type(dog_data)}{dog_data}"
    assert (
        len(dog_data) == 10
    ), "expected 'dog_data' to have 10 elements (thats the format of the nyc data)"

    # TODO: TASK 3: get breed data by individual dog

    # Your code goes here

    return []  # if match is found, return None if match is not found


# Example of list comprehension usage here!
def get_missing_breeds(breeds: list[list[str]], dogs: list[list[str]]) -> list[str]:
    """Return a list of breeds that are listed in the dogs, but do not have breed data in breeds.

    Args:
        breeds (list[list[str]]): A list of breeds information.
        dogs (list[list[str]]): A list of NYC dogs.

    Returns:
        list[str]: A list of str ["Pitbull","Zoodle","PIT AMERICAN","UNKNOWN"...]
        of all dogs in dogs that don't have breed-data matches on breeds.
    """
    # EXAMPLE CODE: An example of a simple list comprehension that gets
    # each dog's breed that doesn't appear in the list of dog breeds

    # You can see how an existing function can be used to filter a list of dogs
    #   into just the dogs we care about, and can them map that filter into
    #   just the data (breed names) that we care about

    return [
        dog[INDEX_DOG_BREED] for dog in dogs if not get_breed_data_for_dog(breeds, dog)
    ]


def get_dogs_by_breed(dogs: list[list[str]], breed_name: str) -> list[list[str]]:
    """Return a list of all dogs whose breed matches breed name (using is_breed_match).

    Args:
        dogs (list[list[str]]): A list of NYC dogs.
        breed_name (str): A name of a breed ("Pitbull","Zoodle").

    Returns:
        list[list[str]]: A list of lists of str, (e.g. a list of all dog-data records)
        that are all dogs in "dogs" who have a match for that breed.
    """
    assert isinstance(breed_name, str), f"expected 'breed_name' to be str, got {type(breed_name)}{breed_name}"

    # TODO: TASK 4: get dogs by breed name

    # Hint: consider rewriting your code as a list comprehension

    # Your code goes here

    return []


def get_names_by_breed(dogs: list[list[str]], breed_name: str) -> list[str]:
    """Return a sorted list of all the NYC dogs' names whose breed listed matches breed name.

    Args:
        dogs (list[list[str]]): A list of NYC dogs.
        breed_name (str): A name of a breed (e.g. "Pitbull").

    Returns:
        list[str]: A SORTED list of strings of the names of dogs
        with that breed ["Alphonso", "Butter", "Cordelia"....].
    """
    assert isinstance(
        breed_name, str
    ), f"expected 'breed_name' to be str, got {type(breed_name)}{breed_name}"

    # TODO: TASK 5: for a given breed, return a sorted list of all dog' names with that breed

    # Hint: sorted(some_list) will return a sorted copy of a list (if strings, this will sort them alphabetically)

    # Your code goes here

    return []


def has_temperament(breed_data: list[str] | None, adjective: str) -> bool:
    """Return if a specific breed contains a particular adjective (case-sensitive) in it's "temperament" column.

    ie ["Chihuahua",...,"Courageous, Devoted, Lively, Intelligent, Quick",...], "Quick" => True
       ["Chihuahua",...,"Courageous, Devoted, Lively, Intelligent, Quick",...], "Silly" => False

    Args:
        breed_data (list[str] | None): A list of str representing a breed or None.
        adjective (str): An adjective ("Devoted", "Quick", etc).

    Returns:
        bool:
        - True:  If that breed's temperament contains that adjective.
        - False: If the breed's temperament doesn't contain that adjective.
        - False: If the breed_data is None.
    """
    assert (
        isinstance(breed_data, list) or breed_data is None
    ), f"expected 'breed_data' to be list or None, got {type(breed_data)}: {breed_data}"
    assert isinstance(
        adjective, str
    ), f"expected 'adjective' to be str, got {type(adjective)}: {adjective}"

    # TODO: TASK 6: return True/False if a breed has a particular personality trait

    # Hint: "some_value in some_string" will return True if that value can be found in the string
    # Notice that we can *get rid of the easy case first*:
    #   If you return False for any dog with no breed data...
    #   Then any dog remaining *after* that line *must have breed data*

    # Your code goes here

    return False


def get_breeds_by_temperament(breeds: list[list[str]], adjective: str) -> list[list[str]]:
    """Return a list of all breeds that have this adjective in their "temperament" column.

    Args:
        breeds (list[list[str]]): A list of breeds information.
        adjective (str): An adjective ("Devoted", "Quick", etc).

    Returns:
        list[list[str]]: A list of breeds with the given adjective in their temperament.
    """
    assert isinstance(
        adjective, str
    ), f"expected 'adjective' to be str, got {type(adjective)}: {adjective}"

    # TODO: TASK 7: get a list of all breeds that have a given temperament

    # Your code goes here

    return []


def list_all_zip_codes(dogs: list[list[str]]) -> list[str]:
    """Return a sorted list of all unique (no duplicates) zip codes in NYC dogs list.

    Note: "sorted(some_list)" => a sorted copy of the list!
    - Keep a list of zip codes
    - For each dog in all dogs, get its zip code...
    -   If that zip code *doesn't* already exist in the list, add it
    -   (so each zip code will only be in the list once)
    - Return a SORTED version of the list

    Args:
        dogs (list[list[str]]): A list of NYC dogs.

    Returns:
        list[str]: A list of str e.g.["10001", "10012", "100022"...] of each zip.
    """
    assert isinstance(
        dogs, list
    ), f"expected 'dogs' to be list, got {type(dogs)}: {dogs}"

    # TODO: TASK 8: return a list of all zip codes in the dogs database, sorted.

    # Your code goes here

    return []


def list_breeds(dogs: list[list[str]]) -> list[str]:
    """Return a sorted list of all unique (no duplicates) dog breeds in the NYC dogs list.

    Args:
        dogs (list[list[str]]): A list of NYC dogs.

    Returns:
        list[str]: A SORTED list of str e.g.["Australian Cattledog", "Beagle", "Bloodhound", Corgi"...]
        of each unique breed in the dogs dataset.
    """
    assert isinstance(
        dogs, list
    ), f"expected 'dogs' to be list, got {type(dogs)}: {dogs}"

    # TODO: TASK 9: return a list of all unique breed names in dogs, sorted alphabetically (very similar to Task 8!)

    # Your code goes here

    return []


# -----------------------------------------------------------------------------
# ---------------------------------- TESTING ----------------------------------
# -----------------------------------------------------------------------------


def run_test_code() -> None:
    """Test the code.

    This run_test_code is your scratchpad and testing place
    You can run functions, print the output, write asserts
    and comment-out things that you are not currently working on.
    """
    # -----------------------------------------------------------------------------
    # Checking your current working directory
    # Make sure you have ALL 4 CSV FILES in this folder!
    working_directory = os.getcwd()

    print("Current working directory: ", working_directory)
    print("files in this directory")

    for filename in os.listdir():
        if not filename.startswith(".") and not filename.startswith("_"):
            print("\t", filename)

    assert (
        "dog_breed_small.csv" in os.listdir()
    ), "check that you have downloaded all four files"

    # Let's see if your dog data loads!
    # Note that we have ONE FILE (CSV) for breed data
    path_to_breed_characteristics = "dog_breed_characteristics.csv"
    path_to_nyc_dogs = "nyc_dogs.json"

    # UNCOMMENT THE FOLLOWING LINES TO LOCALLY TEST EACH TASK
    # In any editor, highlight the lines you want to (un)comment
    # and press "CMD + /" (command & the forward slash) (CTRL for Windows)

    # # -----------------------------------------------------------------------------
    # # Test TASK 0 and TASK 1
    # breeds = read_breed_data(path_to_breed_characteristics)
    # dogs = read_dog_data(path_to_nyc_dogs)
    #
    # print("\n--------------------\nLoading data")
    #
    # assert isinstance(breeds, list), "breeds should be a list"
    # assert (
    #     len(breeds) > 0
    # ), "breeds should have at least one entry, are you loading the data yet?"
    #
    # # The labels
    # print("\nLabels for the breeds\n", breeds[0])
    # # The first line of data
    # print("\nFirst breed\n", breeds[1])
    # # The first line of data (the dog data doesnt have labels)
    # print("\nFirst dog\n", dogs[0])
    #
    # print(f"\nThere are {len(breeds)} breeds and {len(dogs)} dogs in this dataset")
    #
    # assert isinstance(breeds[0], list), "breeds should be a list of lists"
    # assert isinstance(breeds[0][1], str), "breeds should be a list of lists of strings"
    # assert len(dogs) > 0, "breeds should have at least one entry"
    # assert isinstance(dogs[0], list), "dogs should be a list of lists"
    # assert isinstance(dogs[0][1], str), "dogs should be a list of lists of strings"
    #
    # # -----------------------------------------------------------------------------
    # # Test TASK 2
    # print("\n--------------------\nGetting data about breeds")
    # print("\nPoodle breed data:", get_breed_data_by_name(breeds, "POODLE"))
    # print(
    #     "\nWire Haired Fox Terrier:",
    #     get_breed_data_by_name(breeds, "Wire Haired Fox Terrier"),
    # )
    # print("\nZoodle data:", get_breed_data_by_name(breeds, "ZOODLE"))
    #
    # assert isinstance(
    #     get_breed_data_by_name(breeds, "POODLE"), list
    # ), "getting the breed of POODLE should return a list"
    # assert (
    #     get_breed_data_by_name(breeds, "ZOODLE") is None
    # ), "getting the breed of ZOODLE should return None"
    # # -- NOTICE! --
    # # We use "INDEX_BREED_..." for breeds, and "INDEX_DOG..." for dogs
    # assert (
    #     breeds[1][INDEX_BREED_NAME] == "Affenpinscher"
    # ), "The first breed is named 'Affenpinscher'"
    # assert dogs[0][INDEX_DOG_NAME] == "MAX", "The first dog is named 'MAX'"
    #
    # print("\n--------------------\nGetting data about dogs")
    #
    # # -----------------------------------------------------------------------------
    # # Test TASK 3
    # rocko = dogs[1]
    #
    # print("\nThe second dog in the dataset is Rocko:\n", rocko)
    #
    # rocko_breed_data = get_breed_data_for_dog(breeds, rocko)
    #
    # assert rocko_breed_data is not None, "Should not be None, Rocko is a real dog"
    #
    # print("\nRocko's breed info:", rocko_breed_data)
    #
    # assert (
    #     rocko_breed_data[INDEX_BREED_NAME] == "Chihuahua"
    # ), "Rocko's breed data should list him as a 'Chihuahua' breed"
    #
    # # -----------------------------------------------------------------------------
    # # Test TASK 4
    # mastiffs_found = get_dogs_by_breed(dogs, "mastiff")
    #
    # print("\n--------------------\nGetting data about mastiffs")
    # print(f"\nMastiffs found {len(mastiffs_found)}: ")
    # print(mastiffs_found)
    #
    # assert isinstance(mastiffs_found, list), "Get dogs by breed should return a list"
    # assert (
    #     len(mastiffs_found) == 5
    # ), "There are 5 mastiffs (Kevin, Alfonso, Princess, Butter, Massimo)"
    #
    # for dog in mastiffs_found:
    #     print(f"{dog[INDEX_DOG_NAME]} ({dog[INDEX_DOG_BREED]}) is a mastiff")
    #
    # zoodles_found = get_dogs_by_breed(dogs, "zoodle")
    #
    # assert (
    #     len(zoodles_found) == 0
    # ), f"There should be no zoodles in the data, found {len(zoodles_found)}"
    #
    # # -----------------------------------------------------------------------------
    # # Test TASK 5
    # corgi_names = get_names_by_breed(dogs, "corgi")
    #
    # print("\n--------------------\nGetting data about corgis")
    # print("\nCorgi names: ", corgi_names)
    #
    # assert (
    #     len(corgi_names) == 15
    # ), f"There should be 15 corgis, you found {len(corgi_names)}"
    # assert (
    #     corgi_names[0] == "BADGER"
    # ), f"If sorted, the first corgi should be 'BADGER', not {corgi_names[0]}"
    #
    # # -----------------------------------------------------------------------------
    # # Test TASK 6
    # print("\n--------------------\nGetting data about breed temperaments")
    #
    # affenpinscher = breeds[1]
    #
    # assert has_temperament(
    #     affenpinscher, "Curious"
    # ), "Affenpinscher should have temperament Curious"
    # assert not has_temperament(
    #     affenpinscher, "Friendly"
    # ), "Affenpinscher should not have temperament Friendly"
    # assert not has_temperament(
    #     None, "Friendly"
    # ), "None should not have temperament Friendly"
    #
    # # -----------------------------------------------------------------------------
    # # Test TASK 7
    # clown_breeds = get_breeds_by_temperament(breeds, "Clownish")
    #
    # print("\n--------------------\nGetting data about breed temperaments (task 7)")
    # print("\nClownish breeds:")
    #
    # for breed in clown_breeds:
    #     print(f"\t{breed[INDEX_BREED_NAME]} ({breed[INDEX_BREED_TEMPERAMENT]})")
    #
    # assert len(clown_breeds) == 4, "There should be 4 clownish breeds in this dataset"
    #
    # psychic_breeds = get_breeds_by_temperament(breeds, "Psychic")
    #
    # print("\nPsychic breeds:", psychic_breeds)
    #
    # assert len(psychic_breeds) == 0, "There should be 0 psychic breeds in this dataset"
    #
    # # -----------------------------------------------------------------------------
    # # Test TASK 8
    # zipcodes = list_all_zip_codes(dogs)
    #
    # print("\n--------------------\nGetting data about breed zip codes\n")
    # print(
    #     f"{len(zipcodes)} zip codes found {zipcodes[0]}-{zipcodes[-1]}",
    # )
    #
    # assert (
    #     len(zipcodes) == 188
    # ), f"there are 188 zipcodes in this dataset, you found {len(zipcodes)}"
    #
    # assert "10035" in zipcodes, "10035 should be in the zipcodes"
    # assert zipcodes[-1] == "7733", f"7733 is the last zipcode, you found {zipcodes[-1]}"
    #
    # # -----------------------------------------------------------------------------
    # # Test TASK 9
    # # Take a *small slice* of all the dog data
    # # Use this for the next few tasks, to avoid dealing with ALL the dog data
    # print("\n--------------------\nPracticing queries on smaller datasets\n")
    #
    # test_dogs = dogs[0:10]
    # test_dog_breeds = list_breeds(test_dogs)
    #
    # print(f"{len(test_dog_breeds)} breeds in this dataset\n", test_dog_breeds)
    #
    # assert (
    #     "Pug" in test_dog_breeds
    # ), "Pug should be in list of breeds found in this test data"
    # assert (
    #     len(test_dog_breeds) == 8
    # ), "8 different breeds should have been found in this test data"


# Skips the test code if we are running this as a *module* (ie, when we are grading it)
# Otherwise, run your test code!
if __name__ == "__main__":
    run_test_code()
