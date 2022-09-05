// SPDX-License-Identifier: MIT

pragma solidity ^0.8.1;

import "OpenZeppelin/openzeppelin-contracts@4.7.3/contracts/utils/math/SafeMath.sol";

contract Token {

    using SafeMath for uint;

    address owner;

    string public name;
    string public symbol;

    uint public totalSupply;
    uint public decimal = 18;

    mapping(address => uint) public balanceOf;
    mapping(address => mapping(address => uint)) public allowance;

    event Transfer(address indexed _from, address indexed _to, uint _value);
    event Approval(address indexed _owner, address indexed _spender, uint _value);


    constructor(string memory _name, string memory _symbol, uint _totalSupply) {
        owner = msg.sender;
        name = _name;
        symbol = _symbol;
        totalSupply = _totalSupply;
        balanceOf[owner] = _totalSupply;
    }

    function approve(address _spender, uint _value) public returns(bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient Funds");
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    

    // common transfer logic for transfer and transferFrom
    function _transfer(address _from, address _to, uint _value) internal {
        require(balanceOf[_from] >= _value, "Insufficient Funds");
        balanceOf[_from] = balanceOf[_from].sub(_value);
        balanceOf[_to] = balanceOf[_to].add(_value);
        emit Transfer(_from, _to, _value);
    }

    function transfer(address _to, uint _value) public returns(bool success) {
        _transfer(msg.sender, _to, _value);
        return true;
    }

    event debug(address indexed _owner, address indexed _spender);

    function transferFrom(address _from, address _to, uint _value) public returns(bool success) {
        emit debug(_from, msg.sender);
        require(allowance[_from][msg.sender] >= _value, "Spender not authorized to spend this value");
        allowance[_from][msg.sender] = allowance[_from][msg.sender].sub(_value);
        _transfer(_from, _to, _value);
        return true;
    }
}