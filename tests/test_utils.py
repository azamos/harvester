import pytest
from src.utils import build_skip_pages
from src.constants import ERR_LIST_FORMAT,ERR_CONVERT_TO_INT, ERR_LIST_MISSING_NUMBER

def test_build_skip_pages():
    # valid
    simple_valid_str = "1,2,3"
    whitespaced_valid_str ="   1,   2, 3,4,5   , 6  ,7,8  ,9, 10"
    duplicated_whitespaced = " 3  , 4,  , 12,   5,4 ,  3    ,2,   1"
    set1 = set([1,2,3])
    result1 = build_skip_pages(simple_valid_str)
    assert result1 == set1
    set2 = set([i+1 for i in range(10)])
    result2 = build_skip_pages(whitespaced_valid_str)
    assert result2 == set2
    set3 = set([1,2,3,4,5,12])
    # result3 = build_skip_pages(duplicated_whitespaced)
    # should fail with error message
    # invalid1 = "1, 2 3" # not comma-seperated
    # invalid2 = "\n"
    # invalid3 = "NOT NUMBER AT ALL"
    # with pytest.raises(ValueError, match=ERR_CONVERT_TO_INT):
    #     build_skip_pages(invalid1)
    # with pytest.raises(ValueError, match=ERR_LIST_MISSING_NUMBER):
    #     build_skip_pages(invalid2)
    # with pytest.raises(ValueError, match=ERR_CONVERT_TO_INT):
    #     build_skip_pages(invalid3)