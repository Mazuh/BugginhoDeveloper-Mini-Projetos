
import hashlib

class User(object):
    """ Bank user. Can log in and do stuff or just act as a passive object.
    Another class must be used to persist these instances in local storage. """

    agency = ''
    account = ''
    password = '' # md5
    balance = 0
    history = []

    is_logged_in = False

    def __init__(self, agency, account, password, balance=None, history=None):
        """ Constructor. Highly limited actions while it's not logged in.

        Args:
            agency   (str): Agency identification code.
            account  (str): Account identification code.
            password (str): Password MD5 hash, put None if it's unknown.
            balance  (num): Balance in R$, put None if it's unknown.
            history (list): A list of balance transaction records, put None if it's unknown.
        """
        self.agency = agency
        self.account = account
        self.password = password

        if balance is not None:
            self.balance = balance

        if history is not None:
            self.history = history



    def log_in(self, password_str):
        """ TODO
        Access this existent bank account, authenticating by this password string.

        Args:
            password_str (str): A password in natural language.

        Returns:
            bool: True if it was successfully authenticated, False otherwise.

        """
        self.is_logged_in = self.password == self.str_to_hash(password_str)
        return self.is_logged_in



    def transfer_to(self, amount, another_user):
        """ Transfer an amount of cash from this user to another one.
        This instance must have enough balance to do so.

        Args:
            amount       (num): Cash in R$ to discount from this instance user
                                and to increase in another user account.
            another_use (User): Another use to receive this transfering amount of cash.

        Returns:
            bool: True if cash has been transfered from this instance to another, False otherwise.

        """
        if self.balance >= amount:
            self.balance -= amount
            another_user.balance += amount
            return True

        return False



    def withdraw_cash(self, qtt_100s, qtt_50s, qtt_20s):
        """ Withdraw cash. Those args should be obtained throught options_to_withdraw function.
        Also, there are two limits: R$1000,00 or the balance (the lower one).

        Args:
            qtt_100s (int): quantity of 100-real bills
            qtt_50s  (int): quantity of 50-real bills
            qtt_20s  (int): quantity of 20-real bills

        Returns:
            bool: True if the cash has been withdraw, False otherwise.

        """
        amount = PaperMoneyCounter().cash(qtt_100s, qtt_50s, qtt_20s)
        if amount <= self.balance and amount <= 1000:
            self.balance -= amount
            return True

        return False



    def options_to_withdraw(self, amount):
        """ Check options to withdraw an amount of cash. Can't be more than R$1000,00 and
        should be 'printed' in 20, 50 and/or 100-real bills.

        Args:
            amount (num): Desired amount of cash to withdraw.

        Returns:
            None: If the requirements to withdraw weren't accomplished.
            list: If the requeriments to withdraw were accomplished, a list in format
                  [[a, b, c], ...], where each sublist is an option to withdraw cash,
                  and reading as a: quantity of 100s, b: quantity of 50s
                  and c: quantity of 20-real bills available.

        """
        counter = PaperMoneyCounter() # aux class
        options = [] # options to withdraw
        remaining_cash = 0 # aux var

        if (amount % 20 == 0 or amount % 50 == 0) and (amount <= 1000): # is it allowed to withdraw?
            # prioritizing 100-real bills
            qtt_100s = counter.how_many_100s(amount)
            remaining_cash = counter.remaining_cash_without_100s(amount)

            qtt_50s = counter.how_many_50s(remaining_cash)
            remaining_cash = counter.remaining_cash_without_50s(remaining_cash)

            qtt_20s = counter.how_many_20s(remaining_cash)
            remaining_cash = counter.remaining_cash_without_20s(remaining_cash)

            if counter.cash(qtt_100s, qtt_50s, qtt_20s) == amount:
                options.append([qtt_100s, qtt_50s, qtt_20s])

            # prioritizing 50-real bills
            qtt_100s = 0

            qtt_50s = counter.how_many_50s(amount)
            remaining_cash = counter.remaining_cash_without_50s(amount)

            qtt_20s = counter.how_many_20s(remaining_cash)
            remaining_cash = counter.remaining_cash_without_20s(remaining_cash)

            if counter.cash(qtt_100s, qtt_50s, qtt_20s) == amount:
                if not(options[0] == [qtt_100s, qtt_50s, qtt_20s]):
                    options.append([qtt_100s, qtt_50s, qtt_20s])

            # prioritizing 20-real bills
            qtt_100s = 0

            qtt_50s = 0

            qtt_20s = counter.how_many_20s(amount)

            if counter.cash(qtt_100s, qtt_50s, qtt_20s) == amount:
                if not(options[0] == [qtt_100s, qtt_50s, qtt_20s]):
                    if not(options[1] == [qtt_100s, qtt_50s, qtt_20s]):
                        options.append([qtt_100s, qtt_50s, qtt_20s])

            return options

        return None # it wasn't allowed to withdraw



    def str_to_hash(self, param):
        """ Generate a hash of a string param using md5 algorithm

        Args:
            param (str): The content string for hashing.

        Returns:
            str: A hash, generated by a md5 algorithm, using the parameter.

        """
        param = param.encode('utf-8')
        my_hash = hashlib.md5(param)
        return my_hash.hexdigest()



    def hash_password(self):
        """ Hashes the password of this instance
        (it's supposed to be already hashed, but this function is nice in test environment). """
        self.password = self.str_to_hash(self.password)


# ..............................................................


class PaperMoneyCounter(object):
    """ Can do some counts about paper money. Aux class. """

    def cash(self, qtt_100s, qtt_50s, qtt_20s):
        """ Return how much money there is by assembling 100s, 50s and 20-real bills quantities.
        """
        return (qtt_100s * 100) + (qtt_50s * 50) + (qtt_20s * 20)



    def how_many_100s(self, amount):
        """ Return how many 100-real bill can be printed from this amount of cash.
        """
        return amount // 100



    def remaining_cash_without_100s(self, amount):
        """ Return how much cash remains after using a maximum quantity of 100-real bills.
        """
        return amount % 100



    def how_many_50s(self, amount):
        """ Return how many 50-real bill can be printed from this amount of cash.
        """
        return amount // 50



    def remaining_cash_without_50s(self, amount):
        """ Return how much cash remains after using a maximum quantity of 50-real bills.
        """
        return amount % 50



    def how_many_20s(self, amount):
        """ Return how many 20-real bill can be printed from this amount of cash.
        """
        return amount // 20



    def remaining_cash_without_20s(self, amount):
        """ Return how much cash remains after using a maximum quantity of 20-real bills.
        """
        return amount % 20