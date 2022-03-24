import datetime

from hamcrest import *
import json
import pytest
import catalog

from book import generate_first_four_books


@pytest.fixture()
def client():
    with catalog.app.test_client() as client:
        catalog.all_books = generate_first_four_books()
        yield client


test_add_book_data = [
    ({"creation_date": "2020-02-03", "title": "NEW BOOK TITLE", "type": "Satire"}, "201 CREATED"),
    ({"creation_date_mistake": "2020-02-03", "title": "NEW BOOK TITLE", "type": "Satire"}, "406 NOT ACCEPTABLE"),
    ({"creation_date": "2020-02-03", "title": "NEW BOOK TITLE", "type": "Satire", "some": "data"}, "201 CREATED"),
]


@pytest.mark.parametrize("new_book, expected", test_add_book_data)
def test_add_book(client, new_book, expected):
    url = 'http://127.0.0.1:3030/v1/books/manipulation'

    response = client.post(url, json=new_book)

    assert response.status == expected

    if response.status == "201 CREATED":
        url = "http://127.0.0.1:3030/v1/books/ids/" + new_book["title"].replace(" ", "-")
        response = client.get(url)
        got_book_id = response.json['ids']

        url = "http://127.0.0.1:3030/v1/books/info/"
        response = client.get(url + got_book_id[0])
        got_book = response.json['book']

        new_book_redundant_keys = list(new_book.keys())[3:]

        excluded_keys = ["id", "updated_date_time"]
        for key in excluded_keys:
            del got_book[key]
        new_book["creation_date"] = new_book["creation_date"] + " 00:00:00"
        for key in new_book_redundant_keys:
            del new_book[key]

        assert_that(got_book, equal_to(new_book))


def test_delete_book(client):
    book = {"creation_date": "2020-02-03", "title": "NEW BOOK TITLE", "type": "Satire"}
    expected = "204 NO CONTENT"

    url = "http://127.0.0.1:3030/v1/books/manipulation"
    client.post(url, json=book)

    response = client.get("http://127.0.0.1:3030/v1/books/ids/" + book["title"].replace(" ", "-"))
    book_id = response.json["ids"]

    response = client.delete(url + "/" + book_id[0])

    assert response.status == expected


def test_delete_book_with_invalid_id(client):
    invalid_id = "None"
    expected = "404 NOT FOUND"

    url = "http://127.0.0.1:3030/v1/books/manipulation"

    response = client.delete(url + "/" + invalid_id)

    assert response.status == expected


test_get_book_ids_data = [
    ("THE-GREAT-GATSBY", ["some_id", "some_id"]),
    ("STARS AND PLANETS", ["some_id"]),
    ("INVALID-BOOK-TITLE", "404 NOT FOUND")
]


@pytest.mark.parametrize("title, expected", test_get_book_ids_data)
def test_get_all_ids_by_title(client, title, expected):
    url = "http://127.0.0.1:3030/v1/books/ids/" + title

    response = client.get(url)

    if response.status != "404 NOT FOUND":
        response_data = json.loads(response.data.decode("UTF-8"))
        assert len(response_data["ids"]) == len(expected)
    else:
        assert response.status == expected


test_update_book_name_data = [
    ("THE GREAT GATSBY", {"title": "THE GREAT UPDATED GATSBY"}, "204 NO CONTENT"),
    ("NOT EXISTED BOOK NAME", {"title": "THE GREAT UPDATED GATSBY"}, "404 NOT FOUND"),
    ("THE GREAT GATSBY", {"title_mistake": "THE GREAT UPDATED GATSBY"}, "400 BAD REQUEST"),
    ("THE GREAT GATSBY", {"title": "THE GREAT UPDATED GATSBY", "some_more": "data"}, "204 NO CONTENT"),
]


@pytest.mark.parametrize("book_name, request_body, expected", test_update_book_name_data)
def test_update_book_name(client, book_name, request_body, expected):
    url = "http://127.0.0.1:3030/v1/books/manipulation/"

    response = client.get("http://127.0.0.1:3030/v1/books/ids/" + book_name.replace(" ", "-"))
    if len(response.data) != 0:
        book_id = json.loads(response.data.decode("UTF-8"))["ids"]
    else:
        book_id = "None"

    response = client.put(url + book_id[0], json=request_body)

    if response.status == "204 NO CONTENT":
        response = client.get("http://127.0.0.1:3030/v1/books/info/" + book_id[0])
        updated_book = response.json['book']
        # assert_that(updated_book, has_property("title", request_data["title"]))
        assert updated_book['title'] == request_body['title']
    else:
        assert response.status == expected


def test_get_books_not_implemented(client):
    url = "http://127.0.0.1:3030/v1/books/manipulation"

    response = client.get(url)

    assert response.data.decode("UTF-8") == "No implementation for `GET` method"

    assert response.status == "501 NOT IMPLEMENTED"


test_get_limited_books_data = [
    ("2020-01-01", "200 OK", 4),
    (str(datetime.datetime.now().date()), "404 NOT FOUND", 0)
]


@pytest.mark.parametrize("date_limit, expected_status, expected_length", test_get_limited_books_data)
def test_get_limited_books(client, date_limit, expected_status, expected_length):
    url = "http://127.0.0.1:3030/v1/books/latest/"

    response = client.get(url + date_limit)

    assert response.status == expected_status

    if len(response.data) != 0:
        assert len(response.json['books']) == expected_length
    else:
        assert len(response.data) == expected_length


def test_get_book_info_by_id(client):
    book = {"creation_date": "2020-02-03", "title": "NEW BOOK TITLE", "type": "Satire"}

    url = "http://127.0.0.1:3030/v1/books/manipulation"
    client.post(url, json=book)

    response = client.get("http://127.0.0.1:3030/v1/books/ids/" + book["title"].replace(" ", "-"))
    book_id = response.json["ids"]

    url = "http://127.0.0.1:3030/v1/books/info/"
    response = client.get(url + book_id[0])

    assert response.status == "200 OK"

    got_book = response.json['book']
    got_cleared_book = {k: got_book[k] for k in book.keys()}
    book["creation_date"] = book["creation_date"] + " 00:00:00"

    assert_that(got_cleared_book, equal_to(book))


def test_get_book_info_by_not_existing_id(client):
    book_id = "None"
    url = "http://127.0.0.1:3030/v1/books/info/"

    response = client.get(url + book_id)

    assert response.status == "404 NOT FOUND"
