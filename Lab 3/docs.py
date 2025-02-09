"""This file gives examples own how to properly document your code. # A brief one-line file summary

This information will be helpful for Lab 3.                         # An (optional) longer file description
Documentation is needed and graded!

Author: Anonymous                                                   # File information
Date: February 1, 2025
"""

# Notice the docstring above
# In general, docstring are mandatory in 3 places:
#   1. Top of file (very 1st line)
#   2. Functions
#   3. Class definitions (don't worry about for now)


# Example of function docstring
def read_data(path_to_csv: str | None) -> list[list[str]]:
    """Read the listing data.

    Args:
        path_to_csv (str | None): The path to the csv file. Or None if there is no path.

    Returns:
        list: The Airbnb data.

        *Student note: can write either list or list[list] or list[list[str]], same thing
    """
    # Loading data (wrong)
    data = [[path_to_csv]]

    return data


# In general, docstrings follow the format
def function(param_1: type, param_2: type) -> type:
    """_brief one-line summary goes here_

    _*optional* longer, multi-line summary can be included here_
    _remove if unnecessary_

    Args:
        param_1 (type): _description_
        param_2 (type): _description..._
            _...rest of description indented underneath if more than 1 line_

    Returns:
        type: _description_
            _...rest of description indented underneath if more than 1 line_
    """
    return param_1, param_2


# The 'type' of 'param_1: type' simply describes what type we expect param_1 to be
# For example, it can be 'str', 'None', 'list', 'list[str]', etc.
#
# Notice that 'list' and 'list[list]', 'list[list[str]]' are the same
# It's just that each one has more descriptiveness than the previous
#
# Same with 'dict' and 'dict[str, int]'
# We know that param_1 of 'param_1: dict' is a dictionary...
# But of dictionary of what?
# 'param_1: dict[str, int]' is more descriptive, saying it has str keys and int values
#
# In your docstrings, feel free to write whatever level of descriptiveness for your types
#
# Other things to know:
#   param (int | float): A parameter.
#       - '|' means or
#       - 'param' takes in either a int *or* a float
#   param (str, optional): A parameter. Defaults to "".
#       - Means 'param' is optional
#       - The function can be called like 'func(param)' or simply 'func()'
#       - In the second case, 'param' is set to ""


# -----------------------------------------------------------------------------
# Extra
# -----------------------------------------------------------------------------
# There are many docstrings formats.
# In the labs, we use the Google format (the examples above)
# More info here: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
# Feel free to use any other format (or your own!)
# Just BE CONSISTENT throughout your file(s)


# NumPy
def numpy(param1: int, param2: str) -> bool:
    """Example function with types documented in the docstring.

    Longer description.

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str
        The second parameter.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    return param1 < 0 and param2 > 0


# Sphinx
def sphinx(param):
    """[Summary]

    :param [ParamName]: [ParamDescription]
    :type [ParamName]: [ParamType]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    return param
