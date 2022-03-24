import datetime
import logging.config

from flask import Flask, request, Response, jsonify

from book import generate_first_four_books, Book


def is_valid_book_object(book_object):
    return "title" in book_object and \
           "type" in book_object and \
           "creation_date" in book_object


app = Flask(__name__)

"""Variable that contains a list of books in the catalog.
    Generates from test data every time when REST service starts"""
all_books = generate_first_four_books()

logging.basicConfig(filename="../logs/config2.log", level=logging.DEBUG)


# POST http://127.0.0.1:3030/v1/books/manipulation
# {
# 	"creation_date": "2020-01-05",
#   "title": "PRIDE AND PREJUDICE",
#   "type": "Drama"
# }
@app.route('/v1/books/manipulation', methods=['POST'])
def add_book():
    """Implementation of the POST request. Provides adding book to the catalog.
        The body should contain the book data in json format"""
    request_data = request.get_json()
    if is_valid_book_object(request_data):
        created_book = Book(request_data["type"], request_data["title"], request_data["creation_date"])
        all_books.insert(0, created_book)
        response = Response("Successfully added!", status=201, mimetype="application/json")
        new_book_id = [book.id for book in all_books if book.title == request_data["title"]]
        response.headers['Location'] = "/v1/books/info/" + new_book_id[0]
        app.logger.info("Book with id = {} was added".format(new_book_id[0]))
        return response
    else:
        error_message = "You passing an invalid book"
        response = Response(error_message, status=406, mimetype="application/json")
        app.logger.warning("Invalid book want to be passed: {}".format(str(request_data)))
        return response


# DELETE http://127.0.0.1:3030/v1/books/manipulation/some_id
@app.route("/v1/books/manipulation/<string:id>", methods=['DELETE'])
def delete_book(id):
    """Implementation of the DELETE request. Provides removing book from the catalog.

        Parameters
        ----------
        id : str
            The id of the book that we want to delete"""
    global all_books
    books_after_deletion = [book for book in all_books if book.id != id]
    if len(all_books) != len(books_after_deletion):
        response = Response(status=204, mimetype="application/json")
        all_books = books_after_deletion
        app.logger.info("The book was deleted")
        return response
    else:
        response = Response("ERROR! No book with such id!", status=404, mimetype="application/json")
        app.logger.info("No book was deleted")
        return response


# PUT http://127.0.0.1:3030/v1/books/manipulation/some_id
# {
# 	"title": "NEW BOOK"
# }
@app.route("/v1/books/manipulation/<string:id>", methods=['PUT'])
def update_book_name(id):
    """Implementation of the PUT request. Provides updating book title in the catalog.
        The body should contain the book title data in json format

        Parameters
        ----------
        id : str
            The id of the book that we want to update"""
    request_data = request.get_json()
    if "title" in request_data:

        for book in all_books:

            if book.id == id:
                book.title = request_data["title"]
                book.updated_date_time = datetime.datetime.now().replace(microsecond=0).isoformat()
                response = Response(status=204, mimetype="application/json")
                app.logger.info("The title of the book with id = {} was updated".format(book.id))
                return response

        response = Response(status=404, mimetype="application/json")
        app.logger.info("No book title was updated")
        return response

    else:
        response = Response("ERROR! Invalid request!", status=400, mimetype="application/json")
        app.logger.warning("Looks like a mistake in request: {}".format(str(request_data)))
        return response


# GET http://127.0.0.1:3030/v1/books/manipulation
@app.route("/v1/books/manipulation")
def get_books_not_implemented():
    """Implementation of the GET request. Provides showing no implementation of the method."""

    message = "No implementation for `GET` method"
    response = Response(message, status=501)
    app.logger.error("No implementation for `GET` method")
    return response


# GET http://127.0.0.1:3030/v1/books/latest/yyyy-mm-dd
@app.route("/v1/books/latest/<string:limit_date>")
def get_limited_books(limit_date):
    """Implementation of the GET request. Provides getting all the latest added books limited by date.

        Parameters
        ----------
        limit_date : str
            The limit for date added book in the catalog"""
    limit_date = datetime.datetime.strptime(limit_date, '%Y-%m-%d')
    limited_books = [book for book in all_books if book.updated_date_time >= limit_date]
    if len(limited_books) != 0:
        response_list_of_books = [vars(book) for book in limited_books]
        app.logger.info("Books limited by date: {}".format(str(response_list_of_books)))
        return jsonify({'books': response_list_of_books})
    else:
        app.logger.info("No books limited by the date: {}".format(str(limit_date)))
        return Response(status=404, mimetype="application/json")


# GET http://127.0.0.1:3030/v1/books/info/some_id
@app.route("/v1/books/info/<string:id>")
def get_book_info_by_id(id):
    """Implementation of the GET request. Provides getting book info by id.

        Parameters
        ----------
        id : str
            The id of the book in catalog"""
    for book in all_books:
        if book.id == id:
            app.logger.info("Book with id: {} was selected".format(id))
            return jsonify({'book': vars(book)})
    response = Response(status=404, mimetype="application/json")
    app.logger.info("No book with such id: {}".format(id))
    return response


# GET http://127.0.0.1:3030/v1/books/ids/some-title
@app.route("/v1/books/ids/<string:title>")
def get_all_id_by_title(title):
    """Implementation of the GET request. Provides getting all id of the book with the same title.

        Parameters
        ----------
        title : str
            The title of the book(s) in the catalog"""
    title = title.replace("-", " ")
    ids = [book.id for book in all_books if book.title == title]
    if len(ids) != 0:
        app.logger.info("Books with such id: {} relates to the title = {}".format(str(ids), title))
        return jsonify({'ids': ids})
    else:
        app.logger.info("No books with such title in: {}".format(title))
        return Response(status=404, mimetype="application/json")


def main(port=3030):
    app.run(port=port)


if __name__ == "__main__":
    main()
