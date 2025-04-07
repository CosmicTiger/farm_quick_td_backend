from slowapi import Limiter
from slowapi.util import get_remote_address

"""
    This implementations considers the following statements:
    It will help to limit the number of requests to the API.
    It will help to prevent abuse and protect the API from malicious users.
    It will help to improve the performance of the API.
    It will help to reduce the load on the server.
    It will help to improve the user experience.
    It will help to prevent DoS attacks.
    It will help to prevent brute force attacks.

"""
limiter = Limiter(key_func=get_remote_address)
