pragma solidity ^0.8.0;

import "IERC20.sol";

contract TokenSwap {
    address public token1Address;
    address public token2Address;
    address public owner;

    event Swap(address indexed _from, uint256 _amount1, address indexed _to, uint256 _amount2);

    constructor(address _token1Address, address _token2Address) {
        token1Address = _token1Address;
        token2Address = _token2Address;
        owner = msg.sender;
    }

    function swapTokens(uint256 amount1, uint256 amount2) external {
        require(amount1 > 0 && amount2 > 0, "Amounts must be greater than zero");

        // Transfer tokens from sender to contract
        require(
            IERC20(token1Address).transferFrom(msg.sender, address(this), amount1),
            "Token 1 transfer failed"
        );
        require(
            IERC20(token2Address).transferFrom(msg.sender, address(this), amount2),
            "Token 2 transfer failed"
        );

        // Transfer swapped tokens to sender
        require(
            IERC20(token1Address).transfer(msg.sender, amount2),
            "Token 1 transfer failed"
        );
        require(
            IERC20(token2Address).transfer(msg.sender, amount1),
            "Token 2 transfer failed"
        );

        emit Swap(msg.sender, amount1, msg.sender, amount2);
    }

    function withdrawToken(address tokenAddress, uint256 amount) external {
        require(msg.sender == owner, "Only the owner can withdraw tokens");
        require(
            IERC20(tokenAddress).transfer(owner, amount),
            "Token transfer failed"
        );
    }
}
