/**
 * # Arbitrage Specification
 *
 * This specification covers the key rules and properties for the Arbitrage contract.
 */

methods {
    function allowance(address,address) external returns(uint) envfree;
    function balanceOf(address)         external returns(uint) envfree;
    function totalSupply()              external returns(uint) envfree;
    function transfer(address,uint)     external returns(bool) envfree;
    function transferFrom(address,address,uint) external returns(bool) envfree;
    function withdrawToken(address,uint) external;
    function performArbitrage(uint)     external;
}

//// ## Part 1: Basic Rules ////////////////////////////////////////////////////

/// Check for a successful path through performArbitrage
rule reachabilityPerformArbitrage {
    env e;
    calldataarg args;
    performArbitrage(e, args);
    satisfy true, "A non-reverting path through performArbitrage was found";
}

/// Check for a successful path through withdrawToken
rule reachabilityWithdrawToken {
    env e;
    calldataarg args;
    withdrawToken(e, args);
    satisfy true, "A non-reverting path through withdrawToken was found";
}

//// ## Part 2: Security Rules /////////////////////////////////////////////////

/// `performArbitrage` must not revert if the sender has enough allowance and balance
rule arbitrageDoesntRevert {
    env e; uint256 amount1;

    require allowance(e.msg.sender, address(this)) >= amount1;
    require balanceOf(e.msg.sender) >= amount1;

    performArbitrage@withrevert(e, amount1);
    assert !lastReverted, "performArbitrage should not revert if the conditions are met";
}

/// `withdrawToken` must only be executed by the contract owner
rule onlyOwnerCanWithdraw {
    env e; address tokenAddress; uint256 amount;
    address contractOwner = owner();

    require e.msg.sender == contractOwner;

    withdrawToken(e, tokenAddress, amount);
    assert !lastReverted, "withdrawToken should not revert when called by the owner";
}

//// ## Part 3: Invariants /////////////////////////////////////////////////////

/// The sum of all balances must match the total supply for both tokens
invariant totalSupplyIsSumOfBalancesForTokens {
    address[] tokens = [token1Address, token2Address];
    mathint sumBalances;
    for (address token : tokens) {
        sumBalances += sumOfAllBalances(token);
    }

    to_mathint(totalSupply()) == sumBalances,
        "Total supply must match the sum of all balances";
}

//// ## Part 4: Ghosts and Hooks ///////////////////////////////////////////////

/// Helper ghost state to track the sum of balances
ghost mathint sumOfAllBalances(address token) {
    init_state axiom sumOfAllBalances(token) == 0;
}

/// Hook to update the sum of balances on token balance changes
hook Sstore _balances[KEY address a] uint new_value (uint old_value) {
    sumOfAllBalances(token1Address) = sumOfAllBalances(token1Address) + new_value - old_value;
    sumOfAllBalances(token2Address) = sumOfAllBalances(token2Address) + new_value - old_value;
}
