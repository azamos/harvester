import requests
from bs4 import BeautifulSoup
import csv
import os
from .constants import (
    UTF_8,READ_MODE,HTML_PARSER,POINTS,TR_CLASS_NAME,TR,TR_CLASS_NAME,ID,SPAN,
    TITLE_A_CLASS_NAME,A,HREF,NA,USER_CLASS_NAME,LAST_INDEX,COMMENTS_SPLITTER,
    DISCUSS,TITLE,URL,AUTHOR,NUMBER_OF_COMMENTS,PAGE_NUMBER,OUTPUT_FILE_PATH,
    WRITE_MODE,CSV_NEWLINE,LIST_START,ZERO_VALUE,HTML_TEXT_POINTS
    )
from utils import dbgprint, errprint

#Temp: extract the data from locally downloaded html pages of the intended target site
def local_parser(file_path):
    #TODO: Switch to lxml parser instead of the default (suggested by BeautifulSoup documentation)
    dbgprint(f"Parsing for: {file_path}")
    with open(file_path,READ_MODE,encoding=UTF_8) as f:
        html = f.read()
    return BeautifulSoup(html,HTML_PARSER)

def filter_posts(unfiltered_data,min_score,max_score):
    return [data_entry for data_entry in unfiltered_data if min_score <= data_entry[POINTS] <= max_score]

def extract_from_soup(soup,p_num):
    extracted_data = []
    for tr in soup.find_all(TR, class_ = TR_CLASS_NAME):
        id = tr[ID]
        title_td = tr.find(SPAN,class_ = TITLE_A_CLASS_NAME)
        title_a = title_td.find(A)
        title = title_a.get_text()
        url = title_a[HREF]

        score_sp = soup.find(SPAN,id = "score_"+id)
        score = 0
        num_comments = NA
        author_name = NA
        # author_link = NA

        #TODO: instead of checking for the missing score, it will be smarter to
        #check for missing "subline" class span(child of class="subtext" td - always present)

        if score_sp:# When score is missing, so is author and number of comments.
            score = int(score_sp.get_text().split(HTML_TEXT_POINTS)[LIST_START].strip())
            score_parent = score_sp.parent
            user_a = score_parent.find(A,class_ = USER_CLASS_NAME)
            author_name = user_a.get_text()
            # author_link = user_a[HREF]
            comments_str = score_parent.find_all(A)[LAST_INDEX].get_text()
            try:
                num_comments_str = comments_str.split(COMMENTS_SPLITTER)[LIST_START]
                num_comments = ZERO_VALUE if(num_comments_str == DISCUSS) else int(num_comments_str)
            except Exception as e:
                errprint(e)
            

        extracted_data.append(
            {
            TITLE:title,
            URL: url,
            AUTHOR: author_name,
            # AUTHOR:{"name":author_name,"url":author_link},
            POINTS: score,
            NUMBER_OF_COMMENTS: num_comments,
            PAGE_NUMBER: p_num
            })
    return extracted_data

def save_to_csv(posts_list):
    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH),exist_ok=True)
    fields = [TITLE,URL,AUTHOR,POINTS,NUMBER_OF_COMMENTS,PAGE_NUMBER]

    with open(OUTPUT_FILE_PATH,WRITE_MODE,newline=CSV_NEWLINE,encoding=UTF_8) as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fields)
        writer.writeheader()
        for post_dict in posts_list:
            writer.writerow(post_dict)