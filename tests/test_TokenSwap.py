from brownie import web3

def test_balance_received(token, tokenSwap, accounts):
    assert token.balanceOf(accounts[0]) == 0
    assert token.balanceOf(tokenSwap.address) == '1000 ether'


def test_buyTokens_ethChange(tokenSwap, accounts):
    # test change in ETH
    old_contract_eth = tokenSwap.balance()
    old_buyer_eth = accounts[1].balance()

    tx = tokenSwap.buyTokens({'from':accounts[1], 'value':'1 ether'}) #Buying 100 TT for 1 ETH

    new_contract_eth = tokenSwap.balance()
    new_buyer_eth = accounts[1].balance()

    assert new_contract_eth - old_contract_eth == '1 ether'
    assert old_buyer_eth - new_buyer_eth == '1 ether'


def test_buyTokens_ttChange(token, tokenSwap, accounts):
    old_contract_tt = token.balanceOf(tokenSwap.address)
    old_buyer_tt = token.balanceOf(accounts[1])

    tx = tokenSwap.buyTokens({'from':accounts[1], 'value':'1 ether'}) #Buying 100 TT for 1 ETH

    new_contract_tt = token.balanceOf(tokenSwap.address)
    new_buyer_tt = token.balanceOf(accounts[1])

    # althoh it says ether the units are for TT since both use 18 decimals this is doable
    assert old_contract_tt - new_contract_tt == '100 ether' 
    assert new_buyer_tt - old_buyer_tt == '100 ether'


def test_sellTokens_eth(token, tokenSwap, accounts):
    old_contract_eth = tokenSwap.balance()
    old_buyer_eth = accounts[1].balance()

    tokenSwap.buyTokens({'from':accounts[1], 'value':'10 ether'})

    # we have to approve spender in TT units thereforee 1000
    token.approve(tokenSwap.address, '1000 ether', {'from':accounts[1]})

    # since rate = 100 to get 10 eth sell 1000 tt
    tokenSwap.sellTokens('1000 ether', {'from':accounts[1]}) 

    new_contract_eth = tokenSwap.balance()
    new_buyer_eth = accounts[1].balance()

    assert old_contract_eth == new_contract_eth
    assert old_buyer_eth == new_buyer_eth


def test_sellTokens_tt(token, tokenSwap, accounts):
    old_contract_tt = token.balanceOf(tokenSwap.address) #1k tokens
    old_buyer_tt = token.balanceOf(accounts[1]) # 0

    tokenSwap.buyTokens({'from':accounts[1], 'value':'10 ether'})

    # we have to approve spender in TT units thereforee 1000
    token.approve(tokenSwap.address, '1000 ether', {'from':accounts[1]})

    # since rate = 100 to get 10 eth sell 1000 tt
    tokenSwap.sellTokens('1000 ether', {'from':accounts[1]}) 

    new_contract_tt = token.balanceOf(tokenSwap.address)
    new_buyer_tt = token.balanceOf(accounts[1])

    assert old_contract_tt == new_contract_tt
    assert old_buyer_tt == new_buyer_tt