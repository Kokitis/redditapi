import requests
from typing import List, Union, Optional, Dict, Any
from pprint import pprint
from pytools.timetools import Timestamp
import api

COMMENT_ENDPOINT = ""
COMMENT_FIELDS = ["author", "body", "created_utc", "id", "score", "subreddit", "subreddit_id"]

def _aslist(value: Union[str, List[str]]) -> Optional[str]:
	""" Ensures that the passed value is converted to a comma-separated list"""
	if value:
		result = value if isinstance(value, str) else ",".join(value)
	else:
		result = None
	return result


def _parse_datetime(value: Any) -> Optional[int]:
	try:
		datetime = Timestamp(value)
		datetime = int(datetime.timestamp())
	except TypeError:
		datetime = None
	return datetime


def _parse_sort_type(value: str) -> str:
	if value not in {'created_utc', 'num_comments', 'score'}:
		value = 'created_utc'
	return value


def search_comments(q: str = None, ids: List[str] = None, size: int = 25, fields: List[str] = None,
		sort_type: str = "created_utc", author: str = None, subreddit: str = None, after: int = None, before: int = None):
	"""

	Parameters
	----------
	q: str
		Search term
	ids: List[str] or comma-separated string
		Get specific comments via their ids
	size: int [1,500]; default 25
		Number of results to return.
	fields: List[str] or comma-separated string
	sort_type: {'score', 'num_comments', 'created_utc']
	author: str
	subreddit: str
	after: int
		A utc timestamp
	before: int
		A utc timestamp

	Returns
	-------

	"""
	endpoint = "https://api.pushshift.io/reddit/comment/search"
	before = _parse_datetime(before)
	after = _parse_datetime(after)
	#if fields is None: fields = COMMENT_FIELDS
	parameters = {
		"q":         q,
		"ids":       _aslist(ids),
		"size":      size,
		"fields":    _aslist(fields),
		"sort_type": sort_type,
		"author":    author,
		"subreddit": subreddit,
		"after":     _parse_datetime(after),
		"before":    _parse_datetime(before)
	}
	result = api.get(endpoint, parameters)
	return result


def search_submissions(q: str = None, q_not: str = None, title: str = None, title_not: str = None, selftext: str = None, selftext_not: str = None,
		score: Union[str, int] = None, num_comments: Union[str, int] = None, over_18: bool = None, is_video: bool = None, locked: bool = None,
		stickied: bool = None, ids: List[str] = None, size: int = 25, fields: List[str] = None,
		sort_type: str = "created_utc", author: str = None, subreddit: str = None, after: int = None, before: int = None):
	"""

	Parameters
	----------
	q: str
		Search term
	q_not: str
		Exclude search term. Will exclude these terms
	title: str
	title_not: Exclude search term from title. Will exclude these terms
	selftext:str
	selftext_not: Exclude search term from selftext. Will exclude these terms

	ids: List[str] or comma-separated string
		Get specific comments via their ids
	size: int [1,500]; default 25
		Number of results to return.
	score: Integer or > x or < x (i.e. score=>100 or score=<25)
	num_comments: Integer or > x or < x (i.e. score=>100 or score=<25)
	fields: List[str] or comma-separated string
	sort_type: {'score', 'num_comments', 'created_utc']
	author: str
	subreddit: str
	after: int
		A utc timestamp
	before: int
		A utc timestamp

	Returns
	-------

	"""
	parameters = {
		"q":            q,
		"q:not":        q_not,
		"title":        title,
		"title:not":    title_not,
		"selftext":     selftext,
		"selftext:not": selftext_not,
		"score":        score,
		"num_comments": num_comments,
		"over_18":      over_18,
		"is_video":     is_video,
		"locked":       str(locked) if locked else locked,
		"stickied":     str(stickied) if stickied else stickied,
		"ids":          _aslist(ids),
		"size":         size,
		"fields":       _aslist(fields),
		"sort_type":    sort_type,
		"author":       author,
		"subreddit":    subreddit,
		"after":        _parse_datetime(after),
		"before":       _parse_datetime(before)
	}
	endpoint = "https://api.pushshift.io/reddit/search/submission/"
	response = api.get(endpoint, parameters)
	return response


def get_submission(submission_id: str) -> Dict:
	response = search_submissions(ids = submission_id)
	if response:
		result = response[0]
	else:
		result = None
	return result


def get_submission_comment_ids(submission_id: str) -> List[str]:
	url = f"https://api.pushshift.io/reddit/submission/comment_ids/{submission_id}"
	comment_ids = api.query(url)
	return comment_ids

def get_submission_comments(submission_id:str)->List[Dict]:
	comment_ids = get_submission_comment_ids(submission_id)
	comments = search_comments(ids = comment_ids)
	return comments


if __name__ == "__main__":
	comments = get_submission_comments("2d51fr")
	import pandas
	df = pandas.DataFrame(comments)
	pprint(comments[0])
	print(all(i in comments[0] for i in COMMENT_FIELDS))
