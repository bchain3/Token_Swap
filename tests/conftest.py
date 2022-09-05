#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html#isolation-fixtures
    pass


@pytest.fixture(scope="module")
def token(Token, accounts):
    return Token.deploy("TestToken", "TST", '1000 ether', {'from': accounts[0]})

@pytest.fixture(scope="module")
def tokenSwap(TokenSwap, accounts, token):
    ts = TokenSwap.deploy(token.address, {'from':accounts[0]})
    accounts[0].transfer(to=ts.address, amount='10 ether')
    token.transfer(ts.address, '1000 ether', {'from':accounts[0]})
    return ts