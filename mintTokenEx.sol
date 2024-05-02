// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract FaultyERC20 is IERC20 {
    string public constant name = "FaultyToken";
    string public constant symbol = "FTK";
    uint8 public constant decimals = 18;

    mapping(address => uint256) public balances; // Should be private
    mapping(address => mapping(address => uint256)) public allowances; // Should be private

    uint256 public totalSupply_; // Naming inconsistency, should use totalSupply without underscore

    constructor(uint256 initialSupply) {
        balances[msg.sender] = initialSupply;
        totalSupply_ = initialSupply;
        // Missing event emission: Transfer(address(0), msg.sender, initialSupply);
    }

    function totalSupply() public override view returns (uint256) {
        return totalSupply_;
    }

    function increaseTotalSupply(uint newTokens) public { // Should be restricted to owner
        totalSupply_ += newTokens;
        balances[msg.sender] += newTokens;
        // Potential overflow, should check for overflows
        // Missing event emission: Transfer(address(0), msg.sender, newTokens);
    }

    function balanceOf(address tokenOwner) public override view returns (uint256) {
        return balances[tokenOwner];
    }

    function transfer(address receiver, uint256 numTokens) public override returns (bool) {
        require(numTokens <= balances[msg.sender], "Insufficient balance");
        balances[msg.sender] -= numTokens;
        balances[receiver] += numTokens;
        // Missing event emission: Transfer(msg.sender, receiver, numTokens);
        return true;
    }

    function approve(address delegate, uint256 numTokens) public override returns (bool) {
        allowances[msg.sender][delegate] = numTokens;
        // Missing event emission: Approval(msg.sender, delegate, numTokens);
        return true;
    }

    function allowance(address owner, address delegate) public override view returns (uint256) {
        return allowances[owner][delegate];
    }

    function transferFrom(address owner, address buyer, uint256 numTokens) public override returns (bool) {
        require(numTokens <= balances[owner], "Insufficient balance");
        require(numTokens <= allowances[owner][msg.sender], "Insufficient allowance");

        balances[owner] -= numTokens;
        allowances[owner][msg.sender] -= numTokens;
        balances[buyer] += numTokens;
        // Missing event emission: Transfer(owner, buyer, numTokens);
        return true;
    }
}
