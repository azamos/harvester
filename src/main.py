import sys
from .utils import parse_args,validate_args,dbgprint,errprint,build_skip_pages
from .scraper import local_parser,extract_from_soup,save_to_csv,filter_posts
from .constants import (
    MSG_SCRAPING,START,EOF_MOCK,STATIC_FILE_PATH,
    HTML_SUFFIX,MSG_WRITING_TO_CSV,MSG_DONE,ZERO_VALUE
    )
debug_mode = False

if __name__ == "__main__":
    args = parse_args()
    if args.debug:
        debug_mode = args.debug
    try:
        validate_args(args)
        dbgprint("DEBUG MODE ON!",debug_mode=debug_mode)
        s = args.list_string
        skip_pages = pages = build_skip_pages(args.list_string)
        dbgprint(f"The skip_pages are: {skip_pages}",debug_mode=debug_mode)
    except Exception as e:
        errprint(f"something went wrong with argument parsing: {e}")
        sys.exit(1)

    dbgprint("After argument parsing...",debug_mode=debug_mode)
    print(MSG_SCRAPING)
    extracted_data = []
    filtered_post_count = ZERO_VALUE
    try:
        i = START
        while  i < EOF_MOCK:
            if i not in skip_pages:
                i_soup = local_parser(STATIC_FILE_PATH+"/"+str(i)+HTML_SUFFIX)
                remaining = args.num_post - filtered_post_count
                filtered_data = filter_posts(extract_from_soup(i_soup,i),args.min_score,args.max_score)
                limited_data = filtered_data[:remaining]
                filtered_post_count += len(limited_data)
                extracted_data.extend(limited_data)
            i+=1
    except Exception as e:
        errprint(f"Error during scraping: {e}")
        sys.exit(1)

    print(MSG_WRITING_TO_CSV)
    try:
        save_to_csv(extracted_data)
    except Exception as e:
        errprint(f"Saving to CSV failed: {e}")
        sys.exit(1)
    print(MSG_DONE)