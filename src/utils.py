from constants import (
    ERR_NUM_POST_VALUE,ERR_NON_POSITIVE_VALUE,ERR_MIN_MAX_VALUE,ERR_LIST_FORMAT,DEFAULT_NUM_POST,
    HELP_NUM_POST,DEAULT_MIN_SCORE,HELP_MIN_SCORE,DEFAULT_MAX_SCORE,HELP_MAX_SCORE,
    DEFAULT_SKIP_PAGES_STR,HELP_SKIP_PAGES,STORE_TRUE,HELP_DEBUG
    )
import argparse

def dbgprint(msg,debug_mode = False):
    if(debug_mode):
        print(f"[DEBUG] {msg}")

def errprint(msg):
    print(f"[ERROR] {msg}")

def build_skip_pages(list_string):
    return set([int(i.strip()) for i in list_string.split(",") if i.strip()])

def validate_args(args,debug_mode = False):
    num_post = args.num_post
    min_score = args.min_score
    max_score = args.max_score
    list_string = args.list_string
    if num_post < 0:
        raise ValueError(ERR_NUM_POST_VALUE)
    if(min_score < 0 or min_score <0):
        raise ValueError(ERR_NON_POSITIVE_VALUE)
    if(min_score>max_score):
        raise ValueError(ERR_MIN_MAX_VALUE)
    try:
        pages = build_skip_pages(list_string)
        dbgprint(pages,debug_mode)
    except Exception as e:
        raise ValueError(ERR_LIST_FORMAT)
    

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_post",type=int,default=DEFAULT_NUM_POST,help=HELP_NUM_POST)
    parser.add_argument("--min_score",type=int,default=DEAULT_MIN_SCORE,help=HELP_MIN_SCORE)
    parser.add_argument("--max_score",type=int,default=DEFAULT_MAX_SCORE,help=HELP_MAX_SCORE)
    parser.add_argument("--list_string",type=str,default=DEFAULT_SKIP_PAGES_STR,help=HELP_SKIP_PAGES)
    parser.add_argument("--debug",action=STORE_TRUE,help=HELP_DEBUG)
    return parser.parse_args()