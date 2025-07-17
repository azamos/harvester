from src.constants import (
    READ_MODE,UTF_8,STATIC_FILE_PATH,HTML_SUFFIX,TR,TR_CLASS_NAME,
    SPAN, TITLE_A_CLASS_NAME,START,POSTS_PER_PAGE,ONE
    )
from src.scraper import parser
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