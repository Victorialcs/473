/***
 * # AtomicSwap Specification
 *
 * This is a specification for the AtomicSwap contract which interacts with ERC20 tokens.
 */

methods {
    function allowance(address, address) external returns (uint) envfree;
    function transferFrom(address, address, uint256) external returns (bool) envfree;
    function transfer(address, uint256) external returns (bool) envfree;
}

//// ## Part 1: Atomic Swap Rules //////////////////////////////////////////////

/// Ensure swapTokens swaps the correct amounts between the user and the contract
rule swapTokensSpec {
    address sender; uint256 amount1; uint256 amount2;

    env e = env.setCaller(sender);
    require e.msg.sender == sender;

    // Balances before swap
    mathint balance_sender_token1_before = balanceOf(token1Address, sender);
    mathint balance_sender_token2_before = balanceOf(token2Address, sender);
    mathint balance_contract_token1_before = balanceOf(token1Address, address(this));
    mathint balance_contract_token2_before = balanceOf(token2Address, address(this));

    // Call swapTokens
    swapTokens(amount1, amount2);

    // Balances after swap
    mathint balance_sender_token1_after = balanceOf(token1Address, sender);
    mathint balance_sender_token2_after = balanceOf(token2Address, sender);
    mathint balance_contract_token1_after = balanceOf(token1Address, address(this));
    mathint balance_contract_token2_after = balanceOf(token2Address, address(this));

    // Assertions
    assert balance_sender_token1_after == balance_sender_token1_before - amount1 + amount2,
        "swapTokens must swap amount1 of token1 and amount2 of token2 correctly with sender";

    assert balance_sender_token2_after == balance_sender_token2_before - amount2 + amount1,
        "swapTokens must swap amount2 of token2 and amount1 of token1 correctly with sender";

    assert balance_contract_token1_after == balance_contract_token1_before + amount1 - amount2,
        "swapTokens must swap amount1 of token1 and amount2 of token2 correctly with contract";

    assert balance_contract_token2_after == balance_contract_token2_before + amount2 - amount1,
        "swapTokens must swap amount2 of token2 and amount1 of token1 correctly with contract";
}

//// ## Part 2: Helpers ////////////////////////////////////////////////////////

/// Helper function to get balance of a token at an address
function balanceOf(address token, address owner) returns (uint) {
    return IERC20(token).balanceOf(owner);
}

//// ## Part 3: Invariants //////////////////////////////////////////////////////

invariant ensureTokenBalanceConsistency {
    // Total tokens should not change
    mathint total_token1 = balanceOf(token1Address, address(this)) + balanceOf(token1Address, e.msg.sender);
    mathint total_token2 = balanceOf(token2Address, address(this)) + balanceOf(token2Address, e.msg.sender);

    preserved swapTokens(uint256 amount1, uint256 amount2) {
        assert total_token1 == sum_of_balances_token1,
            "Total amount of token1 must remain constant after swaps";

        assert total_token2 == sum_of_balances_token2,
            "Total amount of token2 must remain constant after swaps";
    }
}
