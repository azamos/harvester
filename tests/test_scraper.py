import pytest
from src.constants import (
    READ_MODE,UTF_8,STATIC_FILE_PATH,HTML_SUFFIX,TR,TR_CLASS_NAME,
    SPAN, TITLE_A_CLASS_NAME,START,POSTS_PER_PAGE,ONE,
    TITLE,URL,AUTHOR,POINTS,NUMBER_OF_COMMENTS,PAGE_NUMBER,EMPTY_STR,
    OUTPUT_FILE_PATH,ERR_MISSING_FIELDS,SOURCE_URL
    )
from src.scraper import parser,filter_posts,extract_from_soup,save_to_csv, fetch_page

def local_parser(file_path):
    #TODO: Switch to lxml parser instead of the default (suggested by BeautifulSoup documentation)
    with open(file_path,READ_MODE,encoding=UTF_8) as f:
        html = f.read()
    return parser(html)

def test_scrapper_locally_valid():
    soup = local_parser("./tests/data/hackernews/1.html")
    assert soup.find("body") is not None
    assert len(soup.find_all(TR, class_ = TR_CLASS_NAME))==POSTS_PER_PAGE
    assert len(soup.find_all(SPAN,class_ = TITLE_A_CLASS_NAME))==POSTS_PER_PAGE

def test_scrapper_invalid():
    invalid1 = "<<>><<invalid>><<malformed"
    soup1 = parser(invalid1)
    assert len(soup1.find_all()) == ONE
    assert soup1.find("invalid")!= None
    invalid2 = b'\x00\x01\x02\x03<html>mixed</html>\xff\xfe'
    soup2 = parser(invalid2)
    assert len(soup2.find_all())==0
    invalid3 = "<></><<>><html<body>content</body></html>"
    soup3 = parser(invalid3)
    assert len(soup3.find_all())==1

def test_filter_posts_valid():
    p1 = {
        TITLE:"title1",URL: "test1@test.com",AUTHOR: "author1",POINTS: 100,
        NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1
        }
    p2 = {
        TITLE:"title2",URL: "test2@test.com",AUTHOR: "author2",POINTS: 99,
        NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1
        }
    p3 = {
        TITLE:"title3",URL: "test3@test.com",AUTHOR: "author3",POINTS: 105,
        NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1
        }
    p4 = {
        TITLE:"title4",URL: "test4@test.com",AUTHOR: '',POINTS: '',
        NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1
        }
    posts = [p1,p2,p3,p4]
    res1 = filter_posts(posts,100,104)
    assert len(res1) == 1 and res1[0] == p1
    res2 = filter_posts(posts,99,105)
    assert len(res2) == 3 and p4 not in res2

def test_filter_posts_invalid():
    posts = [{
        TITLE:"title1",URL: "test1@test.com",AUTHOR: "author1",
        POINTS: 'Not a number',NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1}]
    with pytest.raises(TypeError):
        filter_posts(posts)

def test_extract_from_soup_valid():
    soup = local_parser(STATIC_FILE_PATH+"/"+str(START)+HTML_SUFFIX)
    result = extract_from_soup(soup=soup,p_num=START)
    expected_keys = {TITLE,URL,AUTHOR,POINTS,NUMBER_OF_COMMENTS,PAGE_NUMBER}
    for post_data in result:
        assert expected_keys.issubset(post_data.keys())
        assert isinstance(post_data[TITLE],str)
        assert isinstance(post_data[URL],str) and post_data[URL].startswith("http")
        assert isinstance(post_data[AUTHOR],str)
        if post_data[POINTS] != EMPTY_STR:
            assert isinstance(post_data[POINTS],int) and post_data[POINTS]>=0
        assert isinstance(post_data[NUMBER_OF_COMMENTS],int) and post_data[NUMBER_OF_COMMENTS]>=0
        assert isinstance(post_data[PAGE_NUMBER],int) and post_data[PAGE_NUMBER]>=1

def test_extract_from_soup_invalid():
    reddit_soup = local_parser("./tests/data/invalid/reddit.html")
    reddit_result = extract_from_soup(reddit_soup,1)
    assert len(reddit_result)==0
    slashdot_soup = local_parser("./tests/data/invalid/slashdot.html")
    slashdot_result = extract_from_soup(slashdot_soup,1)
    assert len(slashdot_result)==0

def test_save_to_csv_valid():
    p1 = {
        TITLE:"title1",URL: "test1@test.com",AUTHOR: "author1",POINTS: 100,
        NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1
        }
    p2 = {
        TITLE:"title2",URL: "test2@test.com",AUTHOR: "author2",POINTS: 99,
        NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1
        }
    p3 = {
        TITLE:"title3",URL: "test3@test.com",AUTHOR: "author3",POINTS: 105,
        NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1
        }
    p4 = {
        TITLE:"title4",URL: "test4@test.com",AUTHOR: '',POINTS: '',
        NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1
        }
    posts = [p1,p2,p3,p4]
    save_to_csv(posts) # saves to OUTPUT_FILE_PATH
    with open(OUTPUT_FILE_PATH,READ_MODE,encoding=UTF_8) as f:
        lines = f.readlines()
        assert len(lines) == 5
        assert lines[0].strip() == f"{TITLE},{URL},{AUTHOR},{POINTS},{NUMBER_OF_COMMENTS},{PAGE_NUMBER}"
    empty_posts = []
    save_to_csv(empty_posts) # saves to OUTPUT_FILE_PATH
    with open(OUTPUT_FILE_PATH,READ_MODE,encoding=UTF_8) as f:
        lines = f.readlines()
        assert len(lines) == 1
        assert lines[0].strip() == f"{TITLE},{URL},{AUTHOR},{POINTS},{NUMBER_OF_COMMENTS},{PAGE_NUMBER}"

def test_save_to_csv_invalid():
    malformed_post = {"Wrong Key":5,"Another Wrong Key":"test"}
    with pytest.raises(ValueError,match=ERR_MISSING_FIELDS):
        save_to_csv([malformed_post])

def test_fetch_page_valid():
    response = fetch_page(SOURCE_URL+"1")
    assert response !=None

def test_fetch_page_invalid():
    # Test that invalid URLs return None
    assert fetch_page("http://localhost:9999") is None
    assert fetch_page("https://this-domain-does-not-exist.com") is None
    assert fetch_page("not-a-url") is None