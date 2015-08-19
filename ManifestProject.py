# Allows for the user to have options when calling the script in the command line
from optparse import OptionParser

# Import library for arguments to be able to pass in the file name in the command line
from sys import argv
import sys

# Import in order to read from the tab spaced values file
import csv

# To Extract numbers from strings
import re


# My friend suggested this, but I guess it might not be needed
from collections import defaultdict

# To print a dictionary looking nice and sorted
import operator

# Prints with every item on a new line
import pprint





# defines the list (array) to read from 
listFromFeed = []


# The way to open the file to read from. It parses through the rows to get the values
def write_file_to_list(filename):
    listFromFeed = []
    with open(filename, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            listFromFeed.append(row)

    # Set up dict
    # h = dict()
    # for index, header in enum(headers(listFromFeed))
    #	h[header] = index

    return listFromFeed


# Checks for a certain column. Returns the place number if present, False if not
def find_column_number(column_name, listToCheck):
    for i in range(0, len(listToCheck[0])):
        if column_name == listToCheck[0][i]:
            return i

    if column_name not in listToCheck[0]:
        return False


# How many products in the feed? Moreover, len(value) translates to value.length() in java
def number_of_products(listToCheck):
    print "Number of products in the feed: " \
          '\033[1m', '\033[4m' + " %d" % (len(listToCheck) - 1), '\033[0m \n'


# Lists out the headers in the file passed in
def headers(listToCheck):
    print "The feed headers are: \n", listToCheck[0], "\n"


# count the number of unique IDs by adding them to a set then printing the length of set
def amount_of_IDs(listToCheck):
    set_of_IDs = set()
    for item in listToCheck:
        set_of_IDs.add(item[0])

    print "The number of ID's in the feed is:" \
          '\033[1m', '\033[4m' + " %d" % len(set_of_IDs), '\033[0m \n'


# count the number of unique brands

# A function to be used in the following function
# Counts the number of unique values in a given row
def count_unique_in_row(listToCheck2, row_num):
    set_of_uniques = set()
    for item in listToCheck2:
        set_of_uniques.add(item[row_num])
    # print len(set_of_uniques)
    return len(set_of_uniques)


def count_uniques_in_all_rows(listToCheck):
    """Counts and prints the unique values in each row for all the rows"""
    for i in range(0, len(listToCheck[0])):
        print "The number of unique values in %r column:" % listToCheck[0][i]
        print count_unique_in_row(listToCheck, i)


def check_required_fields(listToCheck):
    """Function that checks whether the required fields are present in the file"""
    # The list of headers to compare the file being passed with
    list_of_required_fields = ['id', 'title', 'description', 'google_product_category',
                               'link', 'image_link', 'price', 'sale_price', 'available',
                               'item_group_id', 'inventory']

    # loop through the required fields list
    for item in list_of_required_fields:
        # check if each field from the required list is present in the feed's headers
        # required[i] in listFromFeed[0]
        if item in listToCheck[0]:
            # this code only runs if above is true
            print "Required field is in feed: ", item, "\n"
        else:
            print '\033[1m', '\033[4m' + "Required field is missing from feed: ", \
                item, '\033[0m\n'

        # ***Big lesson! If the for loop does not have range(x, y), then the variable
        # is an object and not a number!


def check_missing_in_column(listToCheck, column):
    """Function to check for missing values in 1 column"""
    # Counter that keeps track of the number of missing fields
    emptyCount = 0
    # Loops through the number of rows
    for i in range(0, len(listToCheck)):
        # If the string in a field has length 0 or if it's null, it counts an empty field
        if len(listToCheck[i][column]) == 0 or listToCheck[i][column] == None:
            emptyCount += 1

    # Informs the user if there are any empty fields in a given column
    if emptyCount == 0:
        print "There are no empty fields in the '%s' column. \n" % (listToCheck[0][column])
    else:
        print "There are %d fields missing in the '%s' column. \n" % (
            emptyCount, listToCheck[0][column])

    # Function to check for missing values in ALL the columns


def missing_fields_per_column(listToCheck):
    # Loops through all the columns to check how many empty fields per column
    for i in range(0, len(listToCheck[0])):
        check_missing_in_column(listToCheck, i)


# Function to check for empty values in the columns and prints the number of empty fields		
def total_empty_values(listToCheck):
    emptyCount = 0
    for i in range(0, len(listToCheck[0])):
        for j in range(0, len(listToCheck)):
            if len(listToCheck[j][i]) == 0:
                emptyCount += 1
    print emptyCount
    if emptyCount == 0:
        print "There are no empty fields. \n"


# Function to count the number of products per category
def products_per_category(listToCheck):
    # keeps track of the number of products
    product_counter = 0
    product_categories = set()

    # Checks to see what number the 'category' column is
    column = find_column_number('category', listToCheck)
    if column == False:
        print "The category column is missing. Please add it and run the script again."
        sys.exit()

    # loops through the 'categories' column
    for i in range(0, len(listToCheck)):
        product_categories.add(listToCheck[i][column])
    print "The product names are: '%s' \n" % product_categories

    # prompts the user for a category to count
    print "Which category's product would you like to count?"
    answer1 = raw_input(">>")

    # compares desired category name to the feed's and counts every time there's a match
    for i in range(0, len(listToCheck)):
        if answer1 == listToCheck[i][3]:
            product_counter += 1

    # Prints the number of products missing in bold and underlined
    # ***BIG LESSON: You can continue a long line by putting a magical backslash (\)
    # Also, to write in bold: '\033[1m' and to underline: '\033[4m' and normal: '\033[0m]
    print "\nNumber of products in the '%s' category:" % answer1, \
        '\033[1m', '\033[4m' + " %d" % product_counter, '\033[0m \n'


# Helper function (method) to aid in the price range function
# Determines whether a string is a number (either int or float) and returns True/False
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def product_in_price_range(listToCheck):
    """Function that counts the number of products that fall within a given price range"""
    # Boolean to ensure user inputs a number and not a word/letter
    trollDetector = False
    # Keeps track of the number of products
    product_counter = 0

    # Checks to see what number the 'price' column is
    column = find_column_number('price', listToCheck)

    if column == False:
        print "The price column is missing. Please add it and run the script again."
        sys.exit()

    # Amazing function that extracts float into a list
    # a = re.findall(r'[\d\.\d]+', listToCheck[1][price])

    # Prompts the user for a lower bound to compare in the price range
    print "Enter a lower bound for the desired price range."
    lower_bound = raw_input(">>")

    # loop that ensures user inputs a number
    while trollDetector == False:
        if is_number(lower_bound) == True:
            break
        else:
            print "Please enter a number."
            lower_bound = raw_input(">>")

    # Prompts user for upper limit
    print "Now enter an upper bound for the desired price range."
    upper_bound = raw_input(">>")

    # loop that ensures user inputs a number
    while trollDetector == False:
        if is_number(upper_bound) == True:
            break
        else:
            print "Please enter a number."
            upper_bound = raw_input(">>")

    # Loops through the 'prices' column to check products within the desired price range
    for i in range(1, len(listToCheck)):
        if listToCheck[i][column] == None:
            toAdd = 0
            sum = sum + toAdd

        if any(char.isdigit() for char in listToCheck[i][column]) == True:
            a = re.findall(r'[\d\.\d]+', listToCheck[i][column])

            # Compares the prices to the inputted price range to count the products
            # Have to convert everything to floats, just in case they are strings or ints
            if float(a[0]) >= float(lower_bound) and float(a[0]) <= float(upper_bound):
                product_counter += 1
        else:
            product_counter += 0

    print "\nNumber of products within the price range $%s and $%s:" % (
        lower_bound, upper_bound), '\033[1m', '\033[4m' + " %d" \
                                                          % product_counter, '\033[0m \n'


def average_price(listToCheck):
    """Calculates the average price of the products from the feed passed in"""
    # Amazing function that extracts float into a list
    # Dictionary where key is column name, value is column number

    # Checks to see what number the 'price' column is
    column = find_column_number('price', listToCheck)
    if column == False:
        print "The price column is missing. Please add it and run the script again.\n"
        sys.exit()

    # a = re.findall(r'[\d\.\d]+', listToCheck[1][price])

    # Variable that keeps track of the sum of prices
    sum = 0
    toAdd = 0

    # Loops through the 'prices' column to add the prices together
    for i in range(1, len(listToCheck)):
        if listToCheck[i][column] == None:
            toAdd = 0
            sum = sum + toAdd

        if any(char.isdigit() for char in listToCheck[i][column]):
            a = re.findall(r'[\d\.\d]+', listToCheck[i][column])

            if is_number(a[0]) == True:
                if a[0] != None:
                    toAdd = float(a[0])
                    sum = sum + toAdd

        else:
            toAdd = 0
            sum = sum + toAdd

    # Divides the sum by the number of products to calculate the average
    average = sum / (len(listToCheck) - 1)  # -1 because the 1st position is the header

    print "The average price of the products in the feed is:", '\033[1m', '\033[4m' + \
                                                                          " $%d" % average, '\033[0m \n'
    """for i in range(0, len(listToCheck)):
		print listToCheck[i][7]"""


def most_common_keyword(listToCheck):
    """Parses the feed and checks what word appears most"""
    title_column = find_column_number('title', listToCheck)
    description_column = find_column_number('description', listToCheck)

    # Ensures that the columns are present in the feed before running the function
    if description_column == False and title_column == False:
        print "The 'description' column and the 'title' column are missing. \
		Please add them to the feed."
        sys.exit()
    """if title_column == False:
		print "The 'title' column is missing. Please add it to the feed."
		sys.exit()"""
    if description_column == False:
        print "The 'description' column is missing. Please add it to the feed."
        sys.exit()

    d = {}

    bad_words = ['a', 'to', 'and', 'of', 'the', 'or', 'for', 'your', 'these', 'with',
				'\xa9', 'at', 'are', 'in', '', '-', 'on', 'is', 'this', 'them']


    for row in listToCheck:
        for column in row[description_column].split(" "):
            if column in d.keys():
                if column != 'a' and column != 'to' and column != 'and' \
                        and column != 'of' and column != 'the' and column != 'or' \
                        and column != 'for' and column != 'your' and column != 'these' \
                        and column != 'with' and column != '\xa9' and column != 'at' \
                        and column != 'are' and column != 'in' and column != '' \
                        and column != '-' and column != 'on' and column != 'is' \
                        and column != 'this' and column != 'them':
                    d[column] += 1
            else:
                d[column] = 1

    for row in listToCheck:
        for column in row[title_column].split(" "):
            if column in d.keys():
                if column != 'a' and column != 'to' and column != 'and' \
                        and column != 'of' and column != 'the' and column != 'or' \
                        and column != 'for' and column != 'your' and column != 'these' \
                        and column != 'with' and column != '\xa9' and column != 'at' \
                        and column != 'are' and column != 'in' and column != '' \
                        and column != '-' and column != 'on' and column != 'is' \
                        and column != 'this' and column != 'them':
                    d[column] += 1
            else:
                d[column] = 1

    # To remove punctuation from strings
    # d = [''.join(c for c in s if c not in string.punctuation) for s in d]
    # print d

    # Ignores "a", "to", "and", "of", "the", "or", "for", "your", "These", "with"
    print "The top 10 most common words in the feed:"
    sorted_dict = sorted(d.items(), key=operator.itemgetter(1))
    for q in range((len(sorted_dict) - 10), len(sorted_dict)):
        pprint.pprint(sorted_dict[q])


# The main function that decides which functions(methods) to call
def main():
    # Variables that enable the script to differentiate valid and invalid user input
    yes = 'y'
    no = 'n'
    validAnswer = False

    parser = OptionParser()

    parser.add_option("-f", "--file_name", help="what's the file name of the feed")
    parser.add_option("-t", "--headersList", help="Would you like to see the headers?")
    parser.add_option("-p", "--products", help="Number of products in the feed?")
    parser.add_option("-i", "--IDs", help="Number of ID's in the feed?")
    parser.add_option("-u", "--uniques", help="Number of unique values per column")
    parser.add_option("-m", "--missing", help="Number of missing fields in the feed")
    parser.add_option("-c", "--categories", help="Number of products per category")
    parser.add_option("-r", "--priceRange", help="Number of products in price range")
    parser.add_option("-F", "--requiredFields", help= \
        "Check if required fields are missing from the feed")
    parser.add_option("-a", "--averagePrice", help= \
        "Average price of the products in the feed")
    parser.add_option("-w", "--commonWords", help="Most common keywords")
    options, remainder = parser.parse_args()

    file_name = options.file_name
    headersList = options.headersList
    products = options.products
    IDs = options.IDs
    uniques = options.uniques
    missing = options.missing
    categories = options.categories
    priceRange = options.priceRange
    requiredFields = options.requiredFields
    averagePrice = options.averagePrice
    commonWords = options.commonWords

    # Line that pauses the script and let's you alter it in the command line
    # import pdb; pdb.set_trace()

    # Informs the user of the file they selected for analysis
    if file_name:
        list = []
        list = write_file_to_list(file_name)
        print "\nList selected:", '\033[1m', '\033[4m', file_name, '\033[0m \n\n'
    else:
        # Tells the user to input a file name when calling the script. Then exits.
        print """No file was passed in. Please run the script again and enter a file name.
		\n"""
        sys.exit()


    # Shows the list of headers in the file
    if headersList:
        headers(list)

    # Show number of ID's in the feed
    if IDs:
        amount_of_IDs(list)

    # Executes the function when the -p flag is passed in to the command line
    if options.products:
        number_of_products(list)

    # Count the number of unique values per row
    if uniques:
        count_uniques_in_all_rows(list)

    # Show missing values
    if missing:
        missing_fields_per_column(list)

    # Counts products per category and lets the user pick which category to count
    if categories:
        products_per_category(list)

    # Counts products within a user-inputted price range
    if priceRange:
        product_in_price_range(list)

    # Checks which required fields are missing in the feed
    if requiredFields:
        check_required_fields(list)

    # Checks the average price of all the products in the feed
    if averagePrice:
        average_price(list)

    # Prints the 5 words that appear most in the feed
    if commonWords:
        most_common_keyword(list)

    """print "Do you want to know the number of products in the file? Y/N"
	answer1 = raw_input()
		
	while validAnswer == False: 
		if answer1 == yes:
			break
		if answer1 == yes.upper():
			break
		if answer1 == no:
			break
		if answer1 == no.upper():
			break
		else:
			print "Please enter a valid answer. 'Y' for yes or 'N' for no. Thank you"
			answer1 = raw_input()
		
	if answer1 == yes or answer1 == yes.upper():
		number_of_products()
		
	print "Do you want to see the list of headers in the file? Y/N"
	answer2 = raw_input()
	while validAnswer == False: 
		if answer2 == yes:
			break
		if answer2 == yes.upper():
			break
		if answer2 == no:
			break
		if answer2 == no.upper():
			break
		else:
			print "Please enter a valid answer. 'Y' for yes or 'N' for no. Thank you"
			answer2 = raw_input()
			
	if answer2 == yes or answer2 == yes.upper():
		headers()
		
	print '''Do you want to know which required fields are present and 
	which ones are missing? Y/N'''
	answer3 = raw_input()
	while validAnswer == False: 
		if answer3 == yes:
			break
		if answer3 == yes.upper():
			break
		if answer3 == no:
			break
		if answer3 == no.upper():
			break
		else:
			print "Please enter a valid answer. 'Y' for yes or 'N' for no. Thank you"
			answer3 = raw_input()
			
	if answer3 == yes or answer3 == yes.upper():
		check_required_fields(listFromFeed[0],list_of_required_fields)
		
	print "Would you like to know if there are any empty fields? Y/N"
	answer4 = raw_input()
	while validAnswer == False: 
		if answer4 == yes:
			break
		if answer4 == yes.upper():
			break
		if answer4 == no:
			break
		if answer4 == no.upper():
			break
		else:
			print "Please enter a valid answer. 'Y' for yes or 'N' for no. Thank you"
			answer4 = raw_input()
			
	if answer4 == yes or answer4 == yes.upper():
		missing_fields_per_column(listFromFeed)"""


if __name__ == '__main__':
    main()

    # Questions for the parser: 1 for every function there is
    # Add options for the parser when running it in the command line instead of asking q's
