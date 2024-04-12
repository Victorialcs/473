/**
 * @title Specification for MyToken ERC20 Token
 */

/// Define externs to model the smart contract functions as envfree
extern balanceOf(address): uint256 envfree;
extern allowance(owner: address, spender: address): uint256 envfree;
extern totalSupply(): uint256 envfree;

/// Property: Balances should never be negative
invariant nonNegativeBalances(address user)
    balanceOf(user) >= 0;

/// Property: Total supply should be equal to the sum of all balances
ghost uint256 totalBalances;
hook Sstore balanceOf[KEY address a] uint newValue (uint oldValue) {
    totalBalances = totalBalances - oldValue + newValue;
}
invariant totalSupplyEqualsTotalBalances()
    totalSupply() == totalBalances;
