import pytest
from src.utils import build_skip_pages
from src.constants import ERR_LIST_FORMAT,ERR_CONVERT_TO_INT, ERR_LIST_MISSING_NUMBER

def test_build_skip_pages_valid():
    input1 = "1,2,3"
    input2 = "  5   -   10 ,4,3-10,11,12, 2,      13  "
    input3 = ""
    input4 = "5"
    input5 = "1000-1"
    input6 ="                       "

    expected_1 = set([1,2,3])
    expected_2 = set([i for i in range(2,14)])
    expected_3 = set()
    expected_4 = set([5])
    expected_5 = set([i+1 for i in range(1000)])
    expected_6 = set()

    # test case 1
    result1 = build_skip_pages(input1)
    assert result1 == expected_1

    # test case 2
    result2 = build_skip_pages(input2)
    assert result2 == expected_2

    # test case 3
    result3 = build_skip_pages(input3)
    assert result3 == expected_3

    # test case 4
    result4 = build_skip_pages(input4)
    assert result4 == expected_4

    # test case 5
    result5 = build_skip_pages(input5)
    assert len(result5) == 1000
    assert 1 in result5 and 1000 in result5

    # test case 6
    result6 = build_skip_pages(input6)
    assert result6 == expected_6

def test_build_skip_pages_invalid():
    input1 = " 12, 1-5, , 5" # Should raise ERR_LIST_MISSING_NUMBER ValueError
    input2 = "12, 1-5, X, 3" # Should raise ERR_CONVERT_TO_INT ValueError
    input3 = "NOT A VALID LIST FORMAT" # Should raise ERR_CONVERT_TO_INT ValueError
    input4 = "1,2,-5,2" # Should raise ERR_CONVERT_TO_INT ValueError
    input5 = "1.5" # Should raise ERR_CONVERT_TO_INT ValueError
    input6 = "1,2,3-x,9" # Should raise ERR_CONVERT_TO_INT ValueError
    input7 = "1,2,3-5-7,8"# Should raise ERR_LIST_FORMAT ValueError
    input8 = ",1,2,3" # should raise ERR_LIST_MISSING_NUMBER

    with pytest.raises(ValueError, match=ERR_LIST_MISSING_NUMBER):
        build_skip_pages(input1)
    with pytest.raises(ValueError, match=ERR_CONVERT_TO_INT):
        build_skip_pages(input2)
    with pytest.raises(ValueError, match=ERR_CONVERT_TO_INT):
        build_skip_pages(input3)
    with pytest.raises(ValueError,match=ERR_CONVERT_TO_INT):
        build_skip_pages(input4)
    with pytest.raises(ValueError,match=ERR_CONVERT_TO_INT):
        build_skip_pages(input5)
    with pytest.raises(ValueError,match=ERR_CONVERT_TO_INT):
        build_skip_pages(input6)
    with pytest.raises(ValueError,match=ERR_LIST_FORMAT):
        build_skip_pages(input7)
    with pytest.raises(ValueError, match=ERR_LIST_MISSING_NUMBER):
        build_skip_pages(input8)