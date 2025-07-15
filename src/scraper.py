import requests
from bs4 import BeautifulSoup
import csv
import argparse
import os
import sys

SOURCE_URL = "https://news.ycombinator.com/"
TR_CLASS_NAME = "athing submission"
TITLE_A_CLASS_NAME = "titleline"
USER_CLASS_NAME = "hnuser"

START = 1
EOF_MOCK = 6

debug_mode = False

NA = "NA"
DISCUSS = "discuss"

#HTML fields and elements
HREF="href"
TR="tr"
ID="id"
SPAN="span"
A="a"
COMMENTS_SPLITTER = "\xa0"

#fields/features names
TITLE = "Title"
URL = "URL"
POINTS = "Points"
AUTHOR = "Author"
NUMBER_OF_COMMENTS = "Number of comments"
PAGE_NUMBER = "Page number"

DEFAULT_NUM_POST = 50
DEAULT_MIN_SCORE = 0
DEFAULT_MAX_SCORE = 10000
DEFAULT_SKIP_PAGES = {}

STATIC_FILE_PATH = "./htmlTestPages"
OUTPUT_FILE_PATH = "./output/result.csv"
HTM_SUFFIX = ".htm"
HTML_SUFFIX = ".html"

HELP_NUM_POST = "Maximum numbers of posts to scrape"
HELP_MIN_SCORE = "Filter: score >= "
HELP_MAX_SCORE = "Filter: score <="
HELP_SKIP_PAGES = "Specify a list of pages to skip, in the format --pages = p1,p2,p3"
HELP_DEBUG = "Allows debug mode"

def dbgprint(msg):
    if(debug_mode):
        print(f"[DEBUG] {msg}")

def errprint(msg):
    print(f"[ERROR] {msg}")


#Temp: extract the data from locally downloaded html pages of the intended target site
#TODO 1: Switch to lxml parser instead (suggested by BeautifulSoup documentation)
#TODO 2: When working locally, swap to fetch from online and cache
def local_parser(file_path):
    dbgprint(f"Parsing for: {file_path}")
    with open(file_path,"r",encoding="utf-8") as f:
        html = f.read()
    return BeautifulSoup(html,"html.parser")

def filter(unfiltered_data,min_score,max_score):
    return [data_entry for data_entry in unfiltered_data if min_score <= data_entry[POINTS] <= max_score]

def extract_from_soup(soup,p_num):
    extracted_data = []
    for tr in soup.find_all(TR, class_ = TR_CLASS_NAME):
        id = tr[ID]
        title_td = tr.find(SPAN,class_ = TITLE_A_CLASS_NAME)
        title_a = title_td.find(A)
        title = title_a.get_text()
        url = title_a[HREF]
        # sibling = tr.next
        # print(sibling)

        #TODO: efficiency maybe can be improved by using parent or next
        score_sp = soup.find(SPAN,id = "score_"+id)
        score = 0#NA bad
        num_comments = NA#might change to something else
        author_name = NA
        author_link = NA
        #TODO: instead of checking for the missing score, it will be smarter to
        #check for missing "subline" class span(child of class="subtext" td - always present)
        if score_sp:# When score is missing, so is author and number of comments.
            score = int(score_sp.get_text().split("points")[0].strip())
            # print(f"score = {score}")
            score_parent = score_sp.parent
            user_a = score_parent.find(A,class_ = USER_CLASS_NAME)
            author_name = user_a.get_text()
            author_link = user_a[HREF]
            comments_str = score_parent.find_all("a")[-1].get_text()
            try:
                num_comments_str = comments_str.split(COMMENTS_SPLITTER)[0]#TODO: remove magic number
                num_comments = 0 if(num_comments_str == DISCUSS) else int(num_comments_str)
            except Exception as e:
                errprint(e)
            

        extracted_data.append(
            {
            TITLE:title,
            URL: url,
            AUTHOR:{"name":author_name,"url":author_link},
            POINTS: score,
            NUMBER_OF_COMMENTS: num_comments,
            PAGE_NUMBER: p_num
            })
    return extracted_data

def save_to_csv(posts_list):
    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH),exist_ok=True)
    fields = [TITLE,URL,AUTHOR,POINTS,NUMBER_OF_COMMENTS,PAGE_NUMBER]

    is_file_exists = os.path.exists(OUTPUT_FILE_PATH) and os.path.getsize(OUTPUT_FILE_PATH) > 0

    with open(OUTPUT_FILE_PATH,'a',newline='',encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fields)
        if not is_file_exists:
            writer.writeheader()
        for post_dict in posts_list:
            writer.writerow(post_dict)

def validate_args(args):
    num_post = args.num_post
    min_score = args.min_score
    max_score = args.max_score
    list_string = args.list_string
    if num_post < 0:
        raise ValueError("num_post must be >= 0 ")
    if(min_score < 0 or min_score <0):
        raise ValueError("scores must be at least 0")
    if(min_score>max_score):
        raise ValueError("min_score must be <= max_score")
    try:
        pages = set([int(i.strip()) for i in list_string.split(",") if i.strip()])
        print(pages)#using print, since debug mode isn't set yet...
    except Exception as e:
        raise ValueError("list must be in the format of int,int,...")
    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_post",type=int,default=DEFAULT_NUM_POST,help=HELP_NUM_POST)
    parser.add_argument("--min_score",type=int,default=DEAULT_MIN_SCORE,help=HELP_MIN_SCORE)
    parser.add_argument("--max_score",type=int,default=DEFAULT_MAX_SCORE,help=HELP_MAX_SCORE)
    parser.add_argument("--list_string",type=str,default="",help=HELP_SKIP_PAGES)
    parser.add_argument("--debug",action="store_true",help=HELP_DEBUG)
    return parser.parse_args()



if __name__ == "__main__":
    print("Trying to prase arguments...")
    args = parse_args()
    try:
        validate_args(args)
        debug_mode = args.debug
        dbgprint("DEBUG MODE ON!")
        s = args.list_string
        skip_pages = set([int(i.strip()) for i in s.split(",") if i.strip()])
        dbgprint(f"The skip list is: {skip_pages}")
    except Exception as e:
        errprint(f"something went wrong with argument parsing: {e}")
        sys.exit(1)

    dbgprint("After argument parsing...")
    extracted_data = []
    filtered_post_count = 0
    try:#TODO: need to add skipping the pages specified in skip_pages
        i = START
        while  i < EOF_MOCK:
            i_soup = local_parser(STATIC_FILE_PATH+"/"+str(i)+HTM_SUFFIX)
            remaining = args.num_post - filtered_post_count
            filtered_data = filter(extract_from_soup(i_soup,i),args.min_score,args.max_score)
            limited_data = filtered_data[:remaining]
            filtered_post_count += len(limited_data)
            extracted_data.extend(limited_data)
            i+=1
    except Exception as e:
        errprint(f"Error during scraping: {e}")
        sys.exit(1)

    # dbgprint(f"Extracted data: {extracted_data}")
    print("Writing data to csv...")
    try:
        save_to_csv(extracted_data)
    except Exception as e:
        errprint(f"Saving to CSV failed: {e}")
        sys.exit(1)
    print("DONE")