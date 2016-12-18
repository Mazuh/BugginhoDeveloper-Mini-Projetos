
import hashlib

class User:
    """ Bank user. Can log in and do stuff or just act as a passive object. """

    agency = ''
    account = ''
    password = '' # md5
    balance = 0

    isLoggedIn = False

    def __init__(self, agency, account, password=None):
        """ Constructor. Highly limited actions while it's not logged in.
        
        Args:
            agency   (str): Agency identification code.
            account  (str): Account identification code.
            password (str): Password in natural language.

        """
        self.agency   = agency
        self.account  = account
        self.password = hashStr(password)



    def login():
        """ TODO """
        pass



    def isLoggedIn():
        """ Check if this user has been successfuly authenticated.
        
        Returns:
            bool: True if has logged in, otherwise False.
        """
        return isLoggedIn



    def hashStr(param):
        """ Generate a hash of a string param using md5 algorithm
        
        Args:
            param (str): The content string for hashing.

        Returns:
            str: A hash, generated by a md5 algorithm, using the parameter.

        """
        param = param.encode('utf-8')
        m = m.update(param)
        return m.hexdigest()