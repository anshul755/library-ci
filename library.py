class LibraryError(Exception):
    pass


class Library:
    """Book lending with a per-member loan limit and a FIFO waiting list."""

    def __init__(self, max_loans=3):
        self.max_loans = max_loans
        self.stock = {}      # isbn -> copies on the shelf
        self.loans = {}      # member -> set of isbns
        self.queues = {}     # isbn -> list of waiting members

    def add_book(self, isbn, copies=1):
        self.stock[isbn] = self.stock.get(isbn, 0) + copies
        self.queues.setdefault(isbn, [])

    def loans_of(self, member):
        return sorted(self.loans.get(member, set()))

    def waiting_list(self, isbn):
        return list(self.queues.get(isbn, []))

    def borrow(self, member, isbn):
        if isbn not in self.stock:
            raise LibraryError("unknown book")
        if isbn in self.loans.get(member, set()):
            raise LibraryError("already borrowed by this member")
        if len(self.loans.get(member, set())) >= self.max_loans:
            raise LibraryError("loan limit reached")

        if self.stock[isbn] > 0:
            self.stock[isbn] -= 1
            self.loans.setdefault(member, set()).add(isbn)
            return "BORROWED"

        if member in self.queues[isbn]:
            raise LibraryError("already on waiting list")
        self.queues[isbn].append(member)
        return "WAITLISTED"

    def return_book(self, member, isbn):
        if isbn not in self.loans.get(member, set()):
            raise LibraryError("book was not borrowed by this member")
        self.loans[member].remove(isbn)

        queue = self.queues[isbn]
        if queue:
            next_member = queue.pop(0)          # first come, first served
            self.loans.setdefault(next_member, set()).add(isbn)
            return next_member
        self.stock[isbn] += 1
        return None
