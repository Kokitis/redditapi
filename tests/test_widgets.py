import pytest
import pushift
@pytest.mark.parametrize(
	"string,expected",
	[
		("dlrezc8,dlrawgw,dlrhbkq","dlrezc8,dlrawgw,dlrhbkq"),
		(["dlrezc8", "dlrawgw", "dlrhbkq"], "dlrezc8,dlrawgw,dlrhbkq"),
		(("dlrezc8", "dlrawgw", "dlrhbkq"), "dlrezc8,dlrawgw,dlrhbkq")
	]
)
def test_aslist(string, expected):

	assert expected == pushift._aslist(string)

def test_parse_datetime(value, expected):
	pass

def test_clean_parameters():
	data = {
		"abc": 123,
		"bcd": None,
		"def": ""
	}

	assert {"abc":'123'} == pushift._clean_parameters(data)