# This file is part of the TCAS Server. Do not redistribute.
# Creates class Secret with methods get_secret() and authenticate()
# for the authentification of the individual workers to the server.

import secrets
UPPER_BOUND = 1_000_000_000
class Secret:
    def __init__(self, n):
        self.n = n
        self.secrets = [secrets.randbelow(UPPER_BOUND) for _ in range(n)]

    def get_secret(self, i):
        try:
            secret = self.secrets[i]
        except IndexError:
            secret = None
        return secret

    def authenticate(self, secret, id):
        try:
            s = self.secrets[id]
        except IndexError:
            return False
        if s == secret:
            return True
        else:
            return False        
   
