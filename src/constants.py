# Hackernews specific attributes
SOURCE_URL = "https://news.ycombinator.com/"
TR_CLASS_NAME = "athing submission"
TITLE_A_CLASS_NAME = "titleline"
USER_CLASS_NAME = "hnuser"
DISCUSS = "discuss"

# Iteration constants
LIST_START = 0
START = 1
EOF_MOCK = 21 # Locally downloaded 20 pages
LAST_INDEX = -1

# HTML fields and elements
HREF="href"
TR="tr"
ID="id"
SPAN="span"
A="a"
COMMENTS_SPLITTER = "\xa0"
HTML_TEXT_POINTS = "points"

# CSV field names
TITLE = "Title"
URL = "URL"
POINTS = "Points"
AUTHOR = "Author"
NUMBER_OF_COMMENTS = "Number of comments"
PAGE_NUMBER = "Page number"

# Defailt field values
ZERO_VALUE = 0
NA = "NA"

# Default values for program arguments
DEFAULT_NUM_POST = 150
DEAULT_MIN_SCORE = 0
DEFAULT_MAX_SCORE = 1000000
DEFAULT_SKIP_PAGES_STR = ""

# Relative paths, files and extentions
STATIC_FILE_PATH = "./htmlTestPages"
OUTPUT_FILE_PATH = "./output/result.csv"
HTM_SUFFIX = ".htm"
HTML_SUFFIX = ".html"

# Messages for the -h and --help flags
HELP_NUM_POST = "Maximum numbers of posts to scrape"
HELP_MIN_SCORE = "Minimal score(for filtering). Must be >= 0"
HELP_MAX_SCORE = "Maximal score(for filtering). Must be >= max(0, min_score)"
HELP_SKIP_PAGES = "Specify a list of pages to skip, in the format --pages = int,int,int,..."
HELP_DEBUG = "Allows debug mode printing"

# User messages
MSG_SCRAPING = "Scraping"
MSG_WRITING_TO_CSV = "Writing data to csv..."
MSG_DONE = "Done."

# Error messages
ERR_NUM_POST_VALUE = "num_post must be >= 0 "
ERR_NON_POSITIVE_VALUE = "scores must be at least 0"
ERR_MIN_MAX_VALUE = "min_score must be <= max_score"
ERR_LIST_FORMAT = "list must be in the format of int,int,..."
ERR_LIST_MISSING_NUMBER = "Empty string where number should be"
ERR_CONVERT_TO_INT = "invalid literal for int"

# Encoding and Writing Modes
UTF_8 = "utf-8"
READ_MODE = "r"
WRITE_MODE = "w"
CSV_NEWLINE = ''

# Characters
COMMA = ","
DASH = "-"

# Symbolic Numbers and Strings
NOT_FOUND = -1

# Other magic numbers and strings
STORE_TRUE = "store_true"
HTML_PARSER = "html.parser"
LENGTH_RANGE_STR = 2
BOTTOM_INDEX = 0
TOP_INDEX = 1
OP_IS_SUCCESSUL = 'op_is_successful'
RESULT_KEY = "result"
POSTS_PER_PAGE = 30