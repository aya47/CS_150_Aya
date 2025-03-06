"""
In this assignment, we will build a class "WikiPage" that stores
information about individual Wikipedia pages.

Author(s): Aya Ben Saghroune
Date: March 6, 2025
"""

import random
import re
from collections import Counter
from datetime import datetime
from pprint import pprint

from bs4 import BeautifulSoup
from treelib import Node, Tree

from load_url_politely import load_url_politely


def get_title(soup: BeautifulSoup) -> str:
    """Get the title of this page.

    How do you find an element, like a title tag
    "<title>My Cool Page</title>" in Beautiful Soup?

    Given some BeautifulSoup instance ("soup"),
    get the title of this page

    Getting data from a soup object:
    We can get an element from a soup instance in many different ways
    (see get_all_links for more)

    One way is to get the *first* element of some type,
    which we can do through the "." notation, like
    soup.h3 or soup.a or soup.title, to get the html's first
    <h3> or <a> or <title> tag

    Args:
        soup (bs4.BeautifulSoup): A processed HTML page.

    Returns:
        str: The string of its page title
        (up to the first dash, we don't need "Cat - Wikipedia",
        we just want "Cat").

    (remember that you can use some_text.find("some_substring")
    to find the index of a substring in some text,
    and can use that index to make a *slice* of the text
    e.g: text[0:text.find(some_substring_to_remove_from_the_end)])
    """
    assert isinstance(soup, BeautifulSoup), "Expected a soup object"

    # Uncomment to explore ways to access elements in a soup object:
    # What type is "soup"?
    # print(type(soup))
    # Example (uncomment to see)
    # print("The first h3 element is", soup.h3)
    # print(f"The first h3 element's text is '{soup.h3.text}'")

    # Task 0: Get the title of the page, and return it (minus " - Wikipedia")
    return ""


def get_last_edit(soup: BeautifulSoup) -> str:
    """Get the date of the last edit of this page.

    How do you find elements with an id in Beautiful Soup?

    The last edit on a wiki page has an id:
        id="footer-info-lastmod"

    Previously we got the first element with a *type*
    Now we have to get an element by an id
    * You can do that with soup.find(id="some_id_name")
    * We also want the *text*, not the whole element,
        so use the .text to get the text contents
    * Finally, we don't want the whole text,
        just a substring of everything after the prefix
        and not including the last period

    All last-edits in Wikipedia are of the format
    " This page was last edited on 9 November 2021, at 13:44"

    Args:
        soup (bs4.BeautifulSoup): A processed HTML page.

    Returns:
        str: All the text between the substring " on " and ", at"
        e.g: "9 November 2021".
    """
    assert isinstance(soup, BeautifulSoup), "Expected a soup object"

    # The substrings that surround the information we want
    start_text = " on "
    end_text = ", at"

    # Example:
    # print(f"the copyright element is: {soup.find(id='footer-info-copyright')}")
    # print(f"the copyright element's text is: {soup.find(id='footer-info-copyright').text}")

    # Task 1: Get date of the last edit of this page (e.g. 9 November 2021)
    return ""


def get_wordcount(soup: BeautifulSoup) -> int:
    """Get the number of words in this page.

    Beautiful Soup objects contain a tree of elements
    We can look at either individual elements
    (all the <div> and <p> and <img> elements, etc),
    or just the inner text of the elements (ignoring all the HTML markup)
    using some_element.text (Note: its a *property* and not a method)
    **To get just the text of a whole page, use "soup.text"**

    To get individual words from text, you can use Python's "split" method
    If used without any parameters, it will split on any "whitespace"
    (spaces, tabs, newlines, etc)
    https://www.programiz.com/python-programming/methods/string/split

    Use these two techniques to return the number of words in this article

    Args:
        soup: A BeautifulSoup instance (some parsed HTML).

    Returns:
        int: The number of words in this article.
    """
    assert isinstance(soup, BeautifulSoup), "Expected a soup object"

    # Example:
    # print("The raw HTML of this page: ", str(soup)[0:100])
    # print("The *text* of this page: ", soup.text[0:100])
    # print("""some text 	to
    # 	split up""".split())

    # Task 2: Get wordcount of this page
    return 0


def get_all_links(soup: BeautifulSoup) -> list[str]:
    """Get all the links in this page.

    How do you find *all* the tags of a type in Beautiful Soup?

    We can use soup.find_all() to find all elements of some type or class
    Consider the example below, and use it as a template for code to
    * get all the "a" tags in the soup (links),
    * and return a list of all the "href" attributes (the link urls)

    Args:
        soup: A BeautifulSoup instance (some parsed HTML).

    Returns:
        list[str]: All URLs linked to in this page.
    """
    assert isinstance(soup, BeautifulSoup), "Expected a soup object"

    # Example: find all the image alt-text in this page
    # * find all the img tags in this soup
    # * for each img tag, see if it has an "alt" attribute
    #    (captioning for photos)
    # * if it has that attribute, add that alt attribute to the list

    # all_images = soup.find_all("img")
    # all_alt_text = []
    # for img in all_images:
    #   if "alt" in img.attrs and img.attrs["alt"] != "":
    #       all_alt_text.append(img.attrs["alt"])
    # print(f"found {len(all_alt_text)} alt-texts:", all_alt_text)

    # Task 3: Using the example above, get all the "href"
    #   (the url of a link) values for all "a" tags to
    #   get a list of all urls linked to in this page
    return []


def get_all_wiki_link_ids(soup: BeautifulSoup) -> list[str]:
    """Get all the wiki link ids linked to in this page.

    We can get a list of all links, using "get_all_links" above
    Can we use that to get a list of all wiki article ids
    (e.g. Thank_U,_Next_(song), Cat, Evanston,_Illinois)
    that are linked to?

    Each link to another article in wikipedia has the format
    "/wiki/Article_ID", e.g "/wiki/Cat", "/wiki/Thank_U,_Next_(song)"
    If we take a slice starting at 6 or links like these, we can get *just the id*

    Some links have ":" or "#" in them: "/wiki/Category:Cats", "/wiki/Red_panda#Taxonomy"
    but these are for resources, subsections or category articles and we don't want those

    Use a for-loop or a list comprehension to return a list
    of *just* the wiki article ids from URLS that:
    * start with "/wiki/"
    * don't have ":" or "#"
    BE sure to get the part of the link *without* "/wiki/"

    Args:
        soup: A BeautifulSoup instance (some parsed HTML).

    Returns:
        list[str]: All wiki article ids linked to in this page
            e.g. 'Single_(music)', 'Ariana_Grande', 'A-side_and_B-side', 'Imagine_(Ariana_Grande_song)'
            (links from the "Thank You, Next" article).
    """
    assert isinstance(soup, BeautifulSoup), "Expected a soup object"

    # Task 4: get all of the wiki article ids linked from this page
    return []


def get_shortest_page(page_directory: dict[str, "WikiPage"]) -> "WikiPage":
    """Get the shortest page in the directory.

    Recall how in lab 1 you had to find the most northern student?
    Use the same approach here to find the *shortest* article (i.e. the lowest wordcount)

    Args:
        page_directory (dict[str, WikiPage]): A dictionary of WikiPage instances that we have loaded.

    Returns:
        WikiPage: The WikiPage with the lowest wordcount.
    """
    assert isinstance(page_directory, dict), f"page_directory should be a dict not {page_directory}"

    # Task 6: Find the shortest article

    # Assuming no wiki articles have more than a million words, any article will beat this
    winning_count = 999999
    winner = None

    # Your code goes here

    return winner


def get_oldest_page(page_directory: dict[str, "WikiPage"]) -> "WikiPage":
    """Get the oldest page in the directory.

    https://stackoverflow.com/questions/466345/converting-string-into-datetime
    The same as get_shortest_page, but how do we compare dates?
    We can use a not-very-readable Python trick to turn it into a timestamp
    "timestamp = datetime.strptime(page.last_edit, '%d %B %Y')"
    which we can then compare like a normal number: e.g. "time_a < time_b"

    Args:
        page_directory (dict[str, WikiPage]): A dictionary of WikiPage instances that we have loaded.

    Returns:
        WikiPage: The WikiPage with the oldest last-edit property.
    """
    assert isinstance(page_directory, dict), f"page_directory should be a dict not {page_directory}"

    # Task 7: Find the oldest article

    # The timestamp for right now, any article is older than this
    winning_timestamp = datetime.today()
    winner = None

    # Your code goes here

    return winner


class WikiPage:
    """A class to represent a Wikipedia page.

    Attributes:
        url (str): The URL of this page.
        html (str): The HTML of this page.
        soup (BeautifulSoup): The BeautifulSoup object of this page.
        title (str): The title of this page.
        wordcount (int): The wordcount of this page.
        page_directory (dict[str, WikiPage]): A dictionary of all the pages
            we have loaded so far, organized by their page_id.
        page_id (str): The page id of this page.
        last_edit (str): The date of the last edit of this page.
        wiki_links (list[str]): The wiki links of this page.
    """

    def __init__(self, page_directory: dict[str, "WikiPage"], page_id: str) -> None:
        """Initialize a WikiPage instance.

        Load this page (from Wikipedia or our cache)
        Creates a BeautfulSoup object from the loaded HTML
        Store this instance in a page_directory under the key of its page_id
                (i.e. "Thank_U,_Next_(song)")
        Sets the URL, HTML, soup, wordcount, last_edit, page_id, and wiki_links of this instance

        Args:
            page_directory (dict[str, WikiPage]):A A dictionary of all the pages
                we have loaded so far, organized by their page_id.
            page_id (str): The wikipedia page id, like "Thank_U,_Next_(song)".
        """
        # Some asserts to catch if we pass in the wrong parameters
        assert isinstance(page_directory, dict), f"page_directory should be a dict not {page_directory}"
        assert not page_id.startswith("/wiki/"), "Expecting just the id a wiki article, not /wiki/some_id"
        assert not page_id.startswith("http"), "Expecting just the id of a wiki article, not the full url"

        # This is a useful line to alert you whenever you create a new WikiPage
        # Helps catch bugs if you are creating WikiPages multiple times, unintentionally
        # print(f"\n★ Create WikiPage for '{page_id}'")

        # Create the URL of this page
        # (what we need to pass to the load_url_politely function)
        wiki_prefix = "https://en.wikipedia.org/wiki/"
        self.url = wiki_prefix + page_id

        # Task 5
        # We need to do a lot of things to initialize a wiki page
        #   but we already have methods for most of them
        #   (...and there are examples of the others in __main__)
        # * Add this WikiPage instance to the page_directory using its page_id as the key

        # Your code here

        # * Use load_url_politely to load HTML from page's URL (from cache or Wikipedia)
        self.html = load_url_politely(self.url)

        # * Create a BeautifulSoup instance for this HTML
        self.soup = BeautifulSoup(self.html, "html.parser")

        # * Store the title, wordcount, page_directory, page_id,
        # * and last_edit as attributes on this instance

        # Your code here

        # * Calculate all the wiki link ids using get_all_wiki_link_ids
        #  * and store it as a wiki_links property on this instance

        # Your code here

    def get_interesting_links(self) -> list[str]:
        """Get all the wiki article ids linked to in this page.

        The newest version of Wikipedia puts boring links (to Main Page, etc) at the top.
        We can make our data science more interesting by making a copy of wiki_ids
        with the boring ones *FILTERED OUT*

        Returns:
            list[str]: A list of all the wiki article ids linked to in this page.
        """

        # Look, a list comprehension!
        all_interesting = [
            wiki_id for wiki_id in self.wiki_links if "Main_Page" not in wiki_id and "_(album)" not in wiki_id
        ]

        # Remove duplicates
        # https://stackoverflow.com/questions/480214/how-do-i-remove-duplicates-from-a-list-while-preserving-order
        return list(dict.fromkeys(all_interesting))

    def load_links(self, recursion_count=0, links_per_article=5, randomize_links=False) -> None:
        """Load the pages linked to from this article by making new WikiPage instances for them.

        Args:
            recursion_count (int): How many levels of recursion to load.
                If 0, only load the links from this page.
            links_per_article (int): How many links to load from each page.
            randomize_links (bool): Whether to randomize the order of the links.

        Note that many pages have hundreds of Wiki articles linked,
        so we only want to load the first "links_per_article"
        """

        # **Trick for printing out recursive function information:**
        # Indent the output with the amount of recursion
        spacer = "\t" * (5 - recursion_count)
        print(
            spacer + f"➡ LOADING LINKS {links_per_article} links from {self.title},"
            f"recursion count {recursion_count} (this number should go down)"
        )

        # Load all links from this
        # Get all the "interesting links" from this page (see above)
        #   If randomize_links is true, use "shuffle" to randomly re-order them
        #   https://www.w3schools.com/python/ref_random_shuffle.asp
        #   Pick the first N links (using links_per_article)
        #       to make a *shorter* list of links to load

        #   (i.e, ['Felidae', 'Cat_(disambiguation)', 'Cats_(disambiguation)',
        #   'Conservation_status', 'Taxonomy_(biology)'] in the Cats article)

        # Get the links to load
        interesting_links = self.get_interesting_links()

        if randomize_links:
            random.shuffle(interesting_links)

        short_list = interesting_links[:links_per_article]
        print(spacer + f" {short_list}")

        for wiki_id in short_list:

            if wiki_id not in self.page_directory:
                print(spacer + f"{self.page_id} -> {wiki_id} load page recursion count = {recursion_count}")
                page = WikiPage(self.page_directory, wiki_id)

                if recursion_count > 0:
                    page.load_links(
                        recursion_count=recursion_count - 1,
                        links_per_article=links_per_article,
                    )

            else:
                print(spacer + f"{self.page_id} -> {wiki_id} - skip page, is already in directory")

    def print_summary(self) -> None:
        """Print a summary of this page."""
        print(f"{self.page_id} (title:'{self.title}')")
        print(f"\tURL:       {self.url}")
        print(f"\tLast edit: {self.last_edit}")
        print(f"\tWordcount: {self.wordcount}")
        link_text = ",".join(self.wiki_links[:5]) + "..." + ",".join(self.wiki_links[-5:])
        print(f"\t{len(self.wiki_links)} links:     {link_text}")

    def find_path(self, current_path, query_id, max_path_length=4) -> list[str] | None:
        """Return the path if this page has a path to this id.

        This solves the wiki game "Six degrees of Wikipedia"
        https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia

        Args:
            current_path (list[str): The path we have taken so far,
                 we need this so we can see if we in a loop
                (i.e. "Illinois -> US State -> Indiana -> Illinois -> US State".....).
            query_id (str): The page id we are trying to get to.
            max_path_length (int): the longest path we are allowed to take
                (prevents unproductively long searches).

        Returns:
            list[str]: The path of wiki page ids that take us from the
                start to the query_id, if a path exists from this page.
            None: If there is no path found.
        """

        # Add ourselves to the current path
        # Note that this makes a *copy* of the path
        next_path = current_path + [self.page_id]

        if self.page_id in current_path:
            # We've been here before, no loops!
            # So stop here
            return None

        if self.page_id == query_id:
            return next_path

        # Search all subpages
        for wiki_id in self.wiki_links:

            # Is the query one of our direct links?
            if wiki_id == query_id:
                return next_path + [wiki_id]

            # If this next page is in our directory
            # AND we still have path length left,
            # RECURSE to search this page next
            # and if it finds a successful path return it
            if wiki_id in self.page_directory and len(current_path) < max_path_length:
                subpage = self.page_directory[wiki_id]
                potential_path = subpage.find_path(next_path, query_id, max_path_length)
                if potential_path:
                    return potential_path

        # If we get here, we have not found a path
        return None

    # ---------------------------
    # Methods to display a nice tree diagram

    def display_tree(self) -> None:
        """Display a tree diagram of all the pages linked to from this page."""
        print(f"\nTree diagram, starting at page '{self.title}'")
        tree = Tree()

        tree.create_node(self.page_id, self.page_id)
        self.add_to_tree(tree)
        tree.show()

    def add_to_tree(self, tree: Tree) -> None:
        """Add this page and all its links to a tree."""
        max_links_to_display = 20

        # Definitely show any links we have loaded,
        # otherwise just the first and last N
        for link_id in self.wiki_links[0:max_links_to_display]:

            # Add this link to our tree, if it's not already in the tree
            # (no loops allowed!)
            if not tree.contains(link_id):

                tree.create_node(link_id, link_id, parent=self.page_id)
                if link_id in self.page_directory:
                    self.page_directory[link_id].add_to_tree(tree)


def run_test_code() -> None:
    """Test the code."""
    print("-" * 36)
    print("** Welcome to Wikipedia explorer! **")
    print(
        """
    ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣤⣄⠀⠀⣤⣿⣤⡀⠀⢠⣿⣤⠀⢠⣼⣧⡤⠀⣠⣼⣿
    ⣿⣿⣿⣇⠀⠘⣿⣿⣷⡀⠈⠿⠃⣠⣿⣿⣿⠃⣸⣿⣿⣿
    ⣿⣿⣿⣿⣆⠀⠹⣿⣿⣷⡀⠀⣰⣿⣿⣿⠃⣰⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣆⠀⠹⣿⡿⠃⠀⠘⣿⣿⠃⣰⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣆⠀⠻⢁⣼⣧⠀⠘⠏⣰⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣄⢀⣾⣿⣿⣧⠀⣠⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿
    ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
    """
    )
    print("Cached page results from March 6, 2025")
    print("-" * 36 + "\n\n")

    test_song_articles = [
        "Airplane_Pt._2",
        "Thank_U,_Next_(song)",
        "Montero_(Call_Me_by_Your_Name)",
        "Savage_Love_(Laxed_%E2%80%93_Siren_Beat)",
    ]
    test_interesting_articles = [
        "Trojan_Room_coffee_pot",
        "Rubber_duck_debugging",
        "IP_over_Avian_Carriers",
        "Scunthorpe_problem",
        "The_Complexity_of_Songs",
        "Illegal_number",
        "MONIAC",
    ]
    test_chicago_articles = [
        "List_of_nicknames_for_Chicago",
        "List_of_songs_about_Chicago",
        "Max_Headroom_signal_hijacking",
        "Raising_of_Chicago",
        "Flag_of_Chicago",
        "Great_Chicago_Fire",
    ]

    # Load a Wikipedia article (you can change this to look at any article)
    # (Comment out the asserts if you want to test other articles)
    test_url = "https://en.wikipedia.org/wiki/Cat"
    # test_url = "https://en.wikipedia.org/wiki/" + test_interesting_articles[0] # Try loading "Rubber_duck_debugging"

    # Load the HTML from either online, or from a cache
    # (notice what happens when you run it multiple times,
    # and notice the "cache" folder that appears in your assignment)
    # You can also print out the debug information when the page loads
    test_html = load_url_politely(test_url, print_debug=True)
    test_soup = BeautifulSoup(test_html, features="html.parser")

    # This will print the whole page (a lot!)
    # print(test_soup)

    # This will print just the *plaintext* (without all the <> markup)
    # print(test_soup.text)

    # ------------------------------------------------------------------
    # Scraping basic information out of Beautiful Soup

    # Test Tasks 0, 1, 2

    test_count = get_wordcount(test_soup)
    test_title = get_title(test_soup)
    test_edit = get_last_edit(test_soup)

    print("-" * 50 + "\nBASIC PAGE INFO:")
    print(f"\tURL =		'{test_url}'")
    print(f"\tWordcount =	'{test_count}'")
    print(f"\tTitle =		'{test_title}'")
    print(f"\tLast edit =	'{test_edit}'")

    assert test_title == "Cat", f"Expecting title 'Cat', your answer: '{test_title}'"
    expected_cat_count = 17516
    expected_cat_edit = "19 May 2024"
    if test_count != expected_cat_count:
        print(
            f"*** POSSIBLE ERROR: Don't worry if this isn't exact (articles get edited), but your word count is {test_count} and we expected something close to {expected_cat_count}"
        )
    if test_edit != expected_cat_edit:
        print(
            f"*** POSSIBLE ERROR: Don't worry if this isn't exact (articles get edited), but your edit date is {test_edit} and we expected something close to {expected_cat_edit}"
        )

    # ------------------------------------------------------------------
    # Getting and processing links

    # Get all the links in the Cat article
    # Notice that there are a bunch of different kinds of links here

    # Test Tasks 3
    test_links = get_all_links(test_soup)
    print("-" * 50 + "\nLINK DATA:")
    print(f"Found {len(test_links)} links in {test_title}")
    print("\tincluding", test_links[:10])  # You can change this "5" to see more than 5 links

    # Test Tasks 4
    wiki_ids = get_all_wiki_link_ids(test_soup)
    print(f"Found {len(wiki_ids)} links to other Wiki articles in {test_title}")
    print("\tincluding", wiki_ids[:10])

    # ------
    # Interesting data science:
    # Have a lot of something? Here are a few ways to look at large lists of information

    # Print all of the wiki ids, sorted alphabetically ("sorted"), with duplicates removed ("set")
    # alphabetical_wiki_ids = sorted(set(wiki_ids))
    # print(",".join(alphabetical_wiki_ids))

    # How many times was each link referenced? Make a counter!
    # https://realpython.com/python-counter/
    # counts = Counter(wiki_ids)

    # Just print all the counts
    # pprint(counts)

    # Calculate how many articles are referenced 1, 2, 3, 4... times in this article
    # What is the most common outgoing link from the Cat article?
    # for i in range(1, 7):
    #     wiki_ids_with_count = [id for (id, count) in counts.items() if count == i]
    #     print(f"Seen {i} times: {len(wiki_ids_with_count)} total", wiki_ids_with_count[0:5])

    assert "Purring" in wiki_ids, "Should have found a link to the wiki page for 'Purring'"
    assert "Kneading_(cats)" in wiki_ids, "Should have found a link to the wiki page for 'Kneading_(cats)'"
    assert "Category:Cats" not in wiki_ids, "Remember to remove links with a ':'"
    assert "Red_panda#Taxonomy" not in wiki_ids, "Remember to remove links with a '#'"

    # # ------------------------------------------------------------------
    # # Putting information into a WikiPage class instance
    # # so we can do advanced queries on it

    # # Like in the last assignment, we have a data structure to hold everything
    # # 	But this time its a *dictionary* instead of a list
    # # 	So that we can easily look pages up by their id:
    # # 	e.g "page_directory['Cat']", page_directory['Montero_(Call_Me_by_Your_Name)']"
    # page_directory = {}

    # test_page = WikiPage(page_directory, "Evanston,_Illinois")

    # # Test Task 5

    # assert test_page.title == "Evanston, Illinois"
    # assert isinstance(test_page.soup, BeautifulSoup), "Did you save the BeautifulSoup object?"
    # assert isinstance(test_page.wordcount, int), f"Wordcound should be an integer, was {test_page.wordcount}"
    # assert isinstance(test_page.last_edit, str), f"Last edit should be a date (str), was {test_page.last_edit}"
    # assert (
    #     "Northwestern_University" in test_page.wiki_links
    # ), "Northwestern should be one of the wiki links of the article on Evanston"

    # assert isinstance(
    #     test_page.page_directory, dict
    # ), "Did you store page_directory as a property on the WikiPage instance?"
    # assert (
    #     page_directory["Evanston,_Illinois"] == test_page
    # ), "Did you store the WikiPage instance in the directory so we can access it later?"

    # # Load several pages
    # for wiki_id in test_interesting_articles:
    #     new_page = WikiPage(page_directory, wiki_id)

    # # Test Task 6 and 7

    # print("-" * 50 + "\nSHORTEST AND OLDEST PAGES:")

    # # Printing out each page and its length
    # # (may be useful to both debug *and* program Task 6!)
    # # No asserts, because these might change, but hopefully this makes the right answer obvious
    # for page_id in page_directory:
    #     page = page_directory[page_id]
    #     print(f"\t{page_id:30} {page.last_edit:20} {page.wordcount} words")

    # shortest = get_shortest_page(page_directory)
    # oldest = get_oldest_page(page_directory)
    # print("Shortest article: ", shortest.title, shortest.wordcount)
    # print("Oldest article: ", oldest.title, oldest.last_edit)

    # # ------------------------------------------------------------------
    # # Load links *recursively*

    # page_directory = {}
    # cat_page = WikiPage(page_directory, "Cat")

    # # Try without recursion
    # print("\n-- Load NON-RECURSIVELY --")
    # cat_page.load_links(links_per_article=5, recursion_count=0)
    # print("All loaded pages ", page_directory.keys())
    # assert (
    #     "Precambrian" in page_directory
    # ), "If it loaded the first 5 links from Cat, 'Precambrian' should be in the directory"

    # # Reset the cat page
    # # Load recursively ONE level
    # # Show a tree visualization of all links accessible from this page
    # # (Wikipedia isn't actually a tree, there are also loops, but we don't visualize those here)
    # print("\n-- Load RECURSIVELY --")
    # page_directory = {}
    # cat_page = WikiPage(page_directory, "Cat")
    # cat_page.load_links(links_per_article=4, recursion_count=1)
    # cat_page.display_tree()

    # # Reset the cat page
    # # Load recursively THREE level but fewer links:
    # # ...this will get further away from the original article
    # page_directory = {}
    # cat_page = WikiPage(page_directory, "Cat")
    # cat_page.load_links(links_per_article=2, recursion_count=3)
    # cat_page.display_tree()
    # print("All loaded pages ", sorted(page_directory.keys()))
    # assert (
    #     "Istanbul" in page_directory
    # ), "If it loaded the links 3 links deep from Cat, 'Istanbul' should be in the directory"

    # # ------------------------------------------------------------------
    # # Testing it more

    # # Play Six Degrees of Wikipedia using find_path
    # # You don't have to edit find_path, but read it to see
    # # how we can *recursively* search a tree or graph structure
    # # to build up a path between two nodes
    # # (https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia)
    # # https://www.sixdegreesofwikipedia.com/
    # # If you time out, you have made too many requests, so wait a minute and run it again
    # # Or reduce the number of pages you are loading

    # # Try loading different pages, and find unexpected paths between topics

    # # Make sure we have some cat pages loaded
    # cat_page = WikiPage(page_directory, "Cat")
    # cat_page.load_links(links_per_article=3, recursion_count=2)
    # cat_page.display_tree()

    # # Lets load two more sets of pages so we have more pages to play with
    # evanston_page = WikiPage(page_directory, "Evanston,_Illinois")
    # evanston_page.load_links(links_per_article=3, recursion_count=2)
    # evanston_page.display_tree()

    # cs_page = WikiPage(page_directory, "Computer_science")
    # cs_page.load_links(links_per_article=2, recursion_count=2)
    # cs_page.display_tree()

    # print("Total pages loaded", ", ".join(page_directory.keys()))

    # # What other paths can we find with only 80 or so pages loaded?
    # # Some of these have no path found, but can you find a path if you load more pages?
    # # What other connections can you find?

    # print("Path found from Cat to Evanston,_Illinois", page_directory["Cat"].find_path([], "Evanston,_Illinois"))
    # print("Path found from Cat to Dinosaur", page_directory["Cat"].find_path([], "Dinosaur"))
    # print("Path found from Cat to Computer_science", page_directory["Cat"].find_path([], "Computer_science"))
    # print(
    #     "Path found from Evanston,_Illinois to List_of_Illinois_townships",
    #     page_directory["Evanston,_Illinois"].find_path([], "List_of_Illinois_townships"),
    # )
    # print("Path found from Cat to Felidae", page_directory["Cat"].find_path([], "Felidae"))
    # print(
    #     "Path found from Computer_science to Half-Life_(series)",
    #     page_directory["Computer_science"].find_path([], "Half-Life_(series)"),
    # )
    # print("Path found from Computer_science to Chicago", page_directory["Computer_science"].find_path([], "Chicago"))
    # print(
    #     "Path found from Spatial_reference_system to Earth_radius",
    #     page_directory["Spatial_reference_system"].find_path([], "Earth_radius"),
    # )


if __name__ == "__main__":
    run_test_code()
