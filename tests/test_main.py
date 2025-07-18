import argparse
import pytest
from src.main import run_scraper
from src.utils import build_skip_pages
from src.constants import TITLE,URL,AUTHOR,POINTS,NUMBER_OF_COMMENTS,PAGE_NUMBER,EMPTY_STR
def test_run_scraper_valid():
    expected_keys = {TITLE,URL,AUTHOR,POINTS,NUMBER_OF_COMMENTS,PAGE_NUMBER}
    args1 = argparse.Namespace(
        num_post = 50,
        min_score = 15,
        max_score = 10000,
        list_string ="",
        offline = True,
        debug = True
    )
    extracted_data1 = run_scraper(args1, skip_pages=build_skip_pages(args1.list_string))
    assert len(extracted_data1) > 0
    assert len(extracted_data1) <= args1.num_post
    
    for post_data in extracted_data1:
        assert expected_keys.issubset(post_data.keys())
        assert isinstance(post_data[TITLE],str)
        assert isinstance(post_data[URL],str)
        assert isinstance(post_data[AUTHOR],str)
        if post_data[POINTS] != EMPTY_STR:
            assert isinstance(post_data[POINTS],int) and post_data[POINTS]>=0
        assert isinstance(post_data[NUMBER_OF_COMMENTS],int) and post_data[NUMBER_OF_COMMENTS]>=0
        assert isinstance(post_data[PAGE_NUMBER],int) and post_data[PAGE_NUMBER]>=1

def test_run_scraper_invalid():
    args = argparse.Namespace(
        num_post=None,
        min_score=15,
        max_score=10000,
        list_string="",
        offline=True
    )
    
    with pytest.raises(SystemExit) as excinfo:
        run_scraper(args, skip_pages=[])
    
    assert excinfo.value.code == 1
