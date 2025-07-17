import sys
import math
from .utils import parse_args,validate_args,dbgprint,errprint,build_skip_pages
from .scraper import local_parser,extract_from_soup,save_to_csv,filter_posts,parser,fetch_page
from .constants import (
    MSG_SCRAPING,START,EOF_MOCK,STATIC_FILE_PATH,
    HTML_SUFFIX,MSG_WRITING_TO_CSV,MSG_DONE,ZERO_VALUE,
    MAX_SAFES_POSTS, POSTS_PER_PAGE,SOURCE_URL
    )
debug_mode = False
offline_mode = False

def run_scraper(args,skip_pages):
    extracted_data = []
    filtered_post_count = ZERO_VALUE
    MAX_PAGES_TO_FETCH = math.ceil(MAX_SAFES_POSTS/POSTS_PER_PAGE) + len(skip_pages)
    upper_range_exclusive = MAX_PAGES_TO_FETCH if not offline_mode else EOF_MOCK
    try:
        i = START
        while  i < upper_range_exclusive:
            if i not in skip_pages:
                i_soup = None
                if offline_mode:
                    i_soup = local_parser(STATIC_FILE_PATH+"/"+str(i)+HTML_SUFFIX)
                else:
                    html = fetch_page(SOURCE_URL+str(i))
                    i_soup = parser(html)
                remaining = args.num_post - filtered_post_count
                filtered_data = filter_posts(extract_from_soup(i_soup,i),args.min_score,args.max_score)
                limited_data = filtered_data[:remaining]
                filtered_post_count += len(limited_data)
                extracted_data.extend(limited_data)
                if filtered_post_count >= args.num_post:
                    break
            i+=1
        dbgprint(f"From run scraper: fetched {i-1} pages",args.debug)
    except Exception as e:
        errprint(f"Error during scraping: {e}")
        sys.exit(1)
    return extracted_data

if __name__ == "__main__":
    args = parse_args()
    if args.debug:
        debug_mode = args.debug
    if args.offline:
        offline_mode = args.offline
    skip_pages = set()
    try:
        validate_args(args)
        dbgprint("DEBUG MODE ON!",debug_mode=debug_mode)
        s = args.list_string
        skip_pages = build_skip_pages(args.list_string)
        dbgprint(f"The skip_pages are: {skip_pages}",debug_mode=debug_mode)
        # NOTE: I know I should probably put it inside validate_args, but got no more time right now.
        if args.num_post > MAX_SAFES_POSTS:
            print(f"[WARNING] Requested {args.num_post} posts, capping to ${MAX_SAFES_POSTS}.")
            args.num_post = MAX_SAFES_POSTS
    except Exception as e:
        errprint(f"something went wrong with argument parsing: {e}")
        sys.exit(1)

    dbgprint("After argument parsing...",debug_mode=debug_mode)
    print(MSG_SCRAPING)

    extracted_data = run_scraper(args,skip_pages)

    print(MSG_WRITING_TO_CSV)
    try:
        save_to_csv(extracted_data)
    except Exception as e:
        errprint(f"Saving to CSV failed: {e}")
        sys.exit(1)
    print(MSG_DONE)