import pytest
from src.constants import (
    READ_MODE,UTF_8,STATIC_FILE_PATH,HTML_SUFFIX,TR,TR_CLASS_NAME,
    SPAN, TITLE_A_CLASS_NAME,START,POSTS_PER_PAGE,ONE,
    TITLE,URL,AUTHOR,POINTS,NUMBER_OF_COMMENTS,PAGE_NUMBER
    )
from src.scraper import parser,filter_posts
def local_parser(file_path):
    #TODO: Switch to lxml parser instead of the default (suggested by BeautifulSoup documentation)
    with open(file_path,READ_MODE,encoding=UTF_8) as f:
        html = f.read()
    return parser(html)

def test_scrapper_locally_valid():
    soup = local_parser(STATIC_FILE_PATH+"/"+str(START)+HTML_SUFFIX)
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
    # filter only cares about the score value. Since I only cover 2 cases: number or empty string,
    # it should raise an error for other strings
    posts = [{
        TITLE:"title1",URL: "test1@test.com",AUTHOR: "author1",
        POINTS: 'Not a number',NUMBER_OF_COMMENTS: 25,PAGE_NUMBER: 1}]
    with pytest.raises(TypeError):
        filter_posts(posts)
    