import pytest
from library import Library, LibraryError


@pytest.fixture
def lib():
    library = Library(max_loans=2)
    library.add_book("B1", copies=1)
    library.add_book("B2")
    library.add_book("B3")
    return library


def test_borrow_available_book(lib):
    assert lib.borrow("asha", "B1") == "BORROWED"
    assert lib.loans_of("asha") == ["B1"]


def test_borrow_unknown_book_rejected(lib):
    with pytest.raises(LibraryError):
        lib.borrow("asha", "XYZ")


def test_no_copy_left_goes_to_waiting_list(lib):
    lib.borrow("asha", "B1")
    assert lib.borrow("ravi", "B1") == "WAITLISTED"
    assert lib.waiting_list("B1") == ["ravi"]


def test_loan_limit_enforced(lib):
    lib.borrow("asha", "B1")
    lib.borrow("asha", "B2")
    with pytest.raises(LibraryError):
        lib.borrow("asha", "B3")


def test_same_book_cannot_be_borrowed_twice(lib):
    lib.add_book("B1")  # two copies now
    lib.borrow("asha", "B1")
    with pytest.raises(LibraryError):
        lib.borrow("asha", "B1")


def test_return_hands_book_to_first_in_queue(lib):
    lib.borrow("asha", "B1")
    lib.borrow("ravi", "B1")
    lib.borrow("meera", "B1")
    assert lib.return_book("asha", "B1") == "ravi"   # FIFO
    assert lib.loans_of("ravi") == ["B1"]
    assert lib.waiting_list("B1") == ["meera"]


def test_return_without_queue_restocks_shelf(lib):
    lib.borrow("asha", "B2")
    assert lib.return_book("asha", "B2") is None
    assert lib.borrow("ravi", "B2") == "BORROWED"


def test_cannot_return_book_not_borrowed(lib):
    with pytest.raises(LibraryError):
        lib.return_book("asha", "B1")
