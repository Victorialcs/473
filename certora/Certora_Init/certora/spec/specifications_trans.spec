/***
 * # TokenSwap Specification
 *
 * Specification for the TokenSwap contract which swaps tokens between two ERC20 contracts.
 */

methods {
    function allowance(address,address) external returns(uint) envfree;
    function balanceOf(address)         external returns(uint) envfree;
    function totalSupply()              external returns(uint) envfree;
    function transfer(address,uint256)  external returns(bool) envfree;
    function transferFrom(address,address,uint256) external returns(bool) envfree;
    function swapTokens(uint256,uint256) external;
    function withdrawToken(address,uint256) external;
}

//// ## Part 1: Basic rules ////////////////////////////////////////////////////

/* 
    Property: Find and show a path for each method.
*/
rule reachability(method f)
{
    env e;
    calldataarg args;
    f(e, args);
    satisfy true, "A non-reverting path through this method was found";
}

/// Swap tokens between two specified amounts, ensuring the swap logic
rule swapTokensSpec {
    address sender;
    env e;
    uint amount1;
    uint amount2;

    require amount1 > 0 && amount2 > 0, "Amounts must be greater than zero";

    // Pre-condition: The sender must have approved and have enough tokens for swap
    require IERC20(token1Address).allowance(sender, address(this)) >= amount1;
    require IERC20(token2Address).allowance(sender, address(this)) >= amount2;

    mathint balance_sender_token1_before = balanceOf(sender);
    mathint balance_sender_token2_before = balanceOf(sender);

    mathint balance_contract_token1_before = balanceOf(address(this));
    mathint balance_contract_token2_before = balanceOf(address(this));

    swapTokens(e, amount1, amount2);

    mathint balance_sender_token1_after = balanceOf(sender);
    mathint balance_sender_token2_after = balanceOf(sender);

    mathint balance_contract_token1_after = balanceOf(address(this));
    mathint balance_contract_token2_after = balanceOf(address(this));

    // Sender should have received `amount2` tokens and lost `amount1` tokens.
    assert balance_sender_token1_after == balance_sender_token1_before - amount1,
        "swapTokens must decrease sender's balance of Token1 by amount1";
    assert balance_sender_token2_after == balance_sender_token2_before - amount2,
        "swapTokens must decrease sender's balance of Token2 by amount2";

    // Contract should reflect the changes
    assert balance_contract_token1_after == balance_contract_token1_before + amount1,
        "swapTokens must increase the contract's balance of Token1 by amount1";
    assert balance_contract_token2_after == balance_contract_token2_before + amount2,
        "swapTokens must increase the contract's balance of Token2 by amount2";
}

/// Withdraw tokens only allowed by the owner of the contract
rule withdrawSpec {
    address tokenAddress;
    address owner;
    env e;
    uint amount;

    require e.msg.sender == owner, "Only the owner can withdraw tokens";

    mathint balance_contract_before = balanceOf(address(this));
    mathint balance_owner_before = balanceOf(owner);

    withdrawToken(e, tokenAddress, amount);

    mathint balance_contract_after = balanceOf(address(this));
    mathint balance_owner_after = balanceOf(owner);

    assert balance_contract_after == balance_contract_before - amount,
        "withdrawToken must decrease the contract's balance of the specified token";
    assert balance_owner_after == balance_owner_before + amount,
        "withdrawToken must increase the owner's balance of the specified token";
}

//// ## Part 2: Parametric rules ///////////////////////////////////////////////

/// Ensure that swapTokens should only proceed if both amounts are greater than zero
rule nonZeroAmounts {
    uint amount1;
    uint amount2;
    env e;

    swapTokens@withrevert(e, amount1, amount2);

    assert lastReverted == (amount1 <= 0 || amount2 <= 0),
        "swapTokens should revert if either amount is zero or less";
}

//// ## Part 3: Invariants /////////////////////////////////////////////////////

invariant totalSupplyIsConsistent() {
    to_mathint(totalSupply()) >= 0;
}
