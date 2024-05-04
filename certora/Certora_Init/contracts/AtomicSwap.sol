pragma solidity ^0.8.0;

import "contracts/IERC20.sol";

contract AtomicSwap {
    address public token1Address;
    address public token2Address;

    constructor(address _token1Address, address _token2Address) {
        token1Address = _token1Address;
        token2Address = _token2Address;
    }

    function swapTokens(uint256 amount1, uint256 amount2) external {
        // Ensure the contract has sufficient allowance from both parties to transfer tokens
        require(
            IERC20(token1Address).allowance(msg.sender, address(this)) >= amount1,
            "Token 1 allowance not set"
        );
        require(
            IERC20(token2Address).allowance(msg.sender, address(this)) >= amount2,
            "Token 2 allowance not set"
        );

        // Transfer tokens from sender to contract
        require(
            IERC20(token1Address).transferFrom(msg.sender, address(this), amount1),
            "Token 1 transfer failed"
        );
        require(
            IERC20(token2Address).transferFrom(msg.sender, address(this), amount2),
            "Token 2 transfer failed"
        );

        // Transfer tokens from contract to sender
        require(
            IERC20(token1Address).transfer(msg.sender, amount2),
            "Token 1 transfer failed"
        );
        require(
            IERC20(token2Address).transfer(msg.sender, amount1),
            "Token 2 transfer failed"
        );
    }
}
