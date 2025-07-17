import pytest
import argparse
from src.utils import build_skip_pages,validate_args,parse_args
from src.constants import (
    ERR_LIST_FORMAT,ERR_CONVERT_TO_INT, ERR_LIST_MISSING_NUMBER,
    DEFAULT_NUM_POST,DEAULT_MIN_SCORE,DEFAULT_MAX_SCORE,DEFAULT_SKIP_PAGES_STR)

INV_L_1 = " 12, 1-5, , 5" # Should raise ERR_LIST_MISSING_NUMBER ValueError
INV_L_2 = "12, 1-5, X, 3" # Should raise ERR_CONVERT_TO_INT ValueError
INV_L_3 = "NOT A VALID LIST FORMAT" # Should raise ERR_CONVERT_TO_INT ValueError
INV_L_4 = "1,2,-5,2" # Should raise ERR_CONVERT_TO_INT ValueError
INV_L_5 = "1.5" # Should raise ERR_CONVERT_TO_INT ValueError
INV_L_6 = "1,2,3-x,9" # Should raise ERR_CONVERT_TO_INT ValueError
INV_L_7 = "1,2,3-5-7,8"# Should raise ERR_LIST_FORMAT ValueError
INV_L_8 = ",1,2,3" # should raise ERR_LIST_MISSING_NUMBER

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
    # expected_5 = set([i+1 for i in range(1000)])
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
    input1 = INV_L_1
    input2 = INV_L_2
    input3 = INV_L_3
    input4 = INV_L_4
    input5 = INV_L_5
    input6 = INV_L_6
    input7 = INV_L_7
    input8 = INV_L_8

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

def test_validate_args_valid():
    args1 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string =""
    )
    args2 = argparse.Namespace(
        num_post = 0,
        min_score = 0,
        max_score = 0,
        list_string ="      "
    )
    args3 = argparse.Namespace(
        num_post = 1,
        min_score = 0,
        max_score = 1,
        list_string ="1,2,3"
    )
    args4 = argparse.Namespace(
        num_post = 100,
        min_score = 0,
        max_score = 100,
        list_string ="    15, 14  -       1,12,   16   "
    )
    assert validate_args(args=args1)==True
    assert validate_args(args=args2)==True
    assert validate_args(args=args3)==True
    assert validate_args(args=args4)==True

def test_validate_args_invalid():
    args1 = argparse.Namespace(
        num_post = -1,
        min_score = 15,
        max_score = 10000,
        list_string =""
    )
    args2 = argparse.Namespace(
        num_post = 150,
        min_score = -1,
        max_score = 10000,
        list_string =""
    )
    args3 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = -1,
        list_string =""
    )
    args4 = argparse.Namespace(
        num_post = 150,
        min_score = 1500,
        max_score = 0,
        list_string =""
    )
    args5 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string = INV_L_1
    )
    args6 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string = INV_L_2
    )
    args7 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string = INV_L_3
    )
    args8 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string = INV_L_4
    )
    args9 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string = INV_L_5
    )
    args10 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string = INV_L_6
    )
    args11 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string = INV_L_7
    )
    args12 = argparse.Namespace(
        num_post = 150,
        min_score = 15,
        max_score = 10000,
        list_string = INV_L_8
    )
    assert validate_args(args=args1)==False
    assert validate_args(args=args2)==False
    assert validate_args(args=args3)==False
    assert validate_args(args=args4)==False
    assert validate_args(args=args5)==False
    assert validate_args(args=args6)==False
    assert validate_args(args=args7)==False
    assert validate_args(args=args8)==False
    assert validate_args(args=args9)==False
    assert validate_args(args=args10)==False
    assert validate_args(args=args11)==False
    assert validate_args(args=args12)==False

def test_parse_args_valid():
    args1 = parse_args(["--num_post","100","--min_score","200","--max_score","300",
                       "--list_string","    5,5,6   ,6,1- 6",
                       "--offline",
                       "--debug"])
    assert args1.num_post == 100
    assert args1.min_score == 200
    assert args1.max_score == 300
    assert args1.list_string == "    5,5,6   ,6,1- 6"
    assert args1.offline == True
    assert args1.debug == True

    args2 = parse_args(["--num_post","0","--min_score","5","--max_score","3",
                       "--list_string","    "])
    assert args2.num_post == 0
    assert args2.min_score == 5
    assert args2.max_score == 3
    assert args2.list_string == "    "
    assert args2.offline == False
    assert args2.debug == False

    args3 = parse_args([])
    assert args3.num_post == DEFAULT_NUM_POST
    assert args3.min_score == DEAULT_MIN_SCORE
    assert args3.max_score == DEFAULT_MAX_SCORE
    assert args3.list_string == DEFAULT_SKIP_PAGES_STR
    assert args3.offline == False
    assert args3.debug == False

def test_parse_args_invalid():
    args1 = ["--num_post","3.5"]
    args2 = ["--num_post","NaN"]
    args3 = ["--num_posts","5"]
    args4 = ["--num_post"]
    with pytest.raises(SystemExit):
        parse_args(args1)
    with pytest.raises(SystemExit):
        parse_args(args2)
    with pytest.raises(SystemExit):
        parse_args(args3)
    with pytest.raises(SystemExit):
        parse_args(args4)