# Book catalog

Simple pyhton app provides storing books and getting them using REST API

## Getting Started

To use the app python 3 should be installed on you computer.

### Installing

To install and run app:

```
python3 -m virtualenv venv

source venv/bin/activate

pip3 install -r requirements.txt

python3 catalog.py
```

## Running the tests

```
pytest tests/test_catalog.py
```

## Built With

* [Flask](https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3) - The web framework used
* [PyTest](https://docs.pytest.org/en/latest/) - Test framework
* [PyHamcrest](https://github.com/hamcrest/PyHamcrest) - Matcher objects framework
