// Specification for the ERC20 token MyToken

// External method declarations
method allowance(address owner, address spender) returns (uint256) envfree;
method balanceOf(address owner) returns (uint256) envfree;
method totalSupply() returns (uint256) envfree;
method transfer(address recipient, uint256 amount) returns (bool);
method approve(address spender, uint256 amount) returns (bool);

// Basic accessibility rule to ensure all methods are reachable
rule reachability() {
    env e;
    calldataarg args;

    assert exists(method f) {
        f(e, args);
        !lastReverted;
    } satisfy true, "All methods must have at least one non-reverting path.";
}

// Rule to verify transfer functionality
rule transferSpec(address sender, address recipient, uint256 amount) {
    require sender != recipient;
    require balanceOf(sender) >= amount, "Sender must have enough balance";

    old uint256 senderOldBalance = balanceOf(sender);
    old uint256 recipientOldBalance = balanceOf(recipient);

    bool success = transfer(recipient, amount);
    assert success, "Transfer must succeed";

    assert balanceOf(sender) == senderOldBalance - amount, "Sender's balance should decrease by amount";
    assert balanceOf(recipient) == recipientOldBalance + amount, "Recipient's balance should increase by amount";
}

// Rule to verify transfer reverts under correct conditions
rule transferReverts(address sender, address recipient, uint256 amount) {
    require balanceOf(sender) < amount, "Sender does not have sufficient balance";

    bool success = transfer(recipient, amount);
    assert !success, "Transfer should fail";
}

// Rule to check that transfer does not revert under specified conditions
rule transferDoesntRevert(address sender, address recipient, uint256 amount) {
    require balanceOf(sender) >= amount;
    require recipient != address(0);

    bool success = transfer(recipient, amount);
    assert success, "Transfer should not revert under valid conditions";
}

// Rule ensuring that approvals are managed correctly
rule onlyHolderCanChangeAllowance(address holder, address spender, uint256 amount) {
    old uint256 oldAllowance = allowance(holder, spender);
    
    bool success = approve(spender, amount);
    assert success, "Approval must succeed";

    uint256 newAllowance = allowance(holder, spender);
    assert newAllowance == amount, "New allowance must match the approved amount";
}

// Invariant checking that the balance at address zero remains zero
invariant BalanceOfZeroAddress() {
    assert balanceOf(address(0)) == 0, "Balance of the zero address should always be zero";
}

// Ghost state and hook for tracking total balances
ghost uint256 totalBalances;
hook after Sstore balanceOf[address a] uint256 newValue (uint256 oldValue) {
    totalBalances = totalBalances - oldValue + newValue;
}

// Invariant that the total supply matches the sum of all balances
invariant TotalSupplyMatchesSumOfBalances() {
    assert totalSupply() == totalBalances, "Total supply must match the sum of all balances";
}
