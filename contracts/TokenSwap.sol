// SPDX-License-Identifier: MIT
pragma solidity ^0.8.1;

import "./Token.sol";

contract TokenSwap {

    Token public token;
    uint public rate = 100;

    event tokensBought(address _buyer, address _token, uint _amount, uint _rate);
    event tokensSold(address _seller, address _token, uint _amount, uint _rate);

    constructor(Token _token) {
        token = _token;
    }

    receive() external payable {
        
    }

    function buyTokens() external payable {
        uint tokenAmount = msg.value * rate;
        require(token.balanceOf(address(this)) >= tokenAmount);
        // here token object calls transfer i.e. ts.address = _from, msg.sender = _to
        token.transfer(msg.sender, tokenAmount);
        emit tokensBought(msg.sender, address(token), tokenAmount, rate);
    }

    function sellTokens(uint _amount) external payable {
        uint ethAmount = _amount / rate;
        require(token.balanceOf(msg.sender) >= _amount);
        require(address(this).balance >= ethAmount, "Contract does not have enough ETH");

        token.transferFrom(msg.sender, address(this), _amount);
        // Compiler will automatically understand ETH needs to go from "this" to msg.sender
        payable(msg.sender).transfer(ethAmount);
        emit tokensSold(msg.sender, address(token), ethAmount, rate);
    }
}