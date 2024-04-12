// Specification for MyToken ERC20 Contract

// External method declarations to interact with the smart contract
method allowance(address, address) returns (uint) envfree;
method balanceOf(address) returns (uint) envfree;
method totalSupply() returns (uint) envfree;
method transfer(address, uint, env) returns (bool);
method approve(address, uint, env) returns (bool);

//// ## Basic reachability rules for each method
rule reachability() {
    forall (method f in {allowance, balanceOf, totalSupply, transfer, approve}) {
        env e;
        calldataarg args;
        assert f(e, args), "a non-reverting path through this method was found";
    }
}

//// ## Transfer rules
rule transferSpec(address sender, address recipient, uint amount) {
    require sender != recipient;
    require balanceOf(sender) >= amount;

    old uint senderOldBalance = balanceOf(sender);
    old uint recipientOldBalance = balanceOf(recipient);

    assert transfer(recipient, amount, env with msg.sender = sender), "Transfer must succeed";

    assert balanceOf(sender) == senderOldBalance - amount,
        "Sender's balance should decrease by amount";
    assert balanceOf(recipient) == recipientOldBalance + amount,
        "Recipient's balance should increase by amount";
}

rule transferReverts(address sender, address recipient, uint amount) {
    require balanceOf(sender) < amount;
    assert !transfer(recipient, amount, env with msg.sender = sender),
        "Transfer should revert if sender's balance is less than amount";
}

rule transferDoesntRevert(address sender, address recipient, uint amount) {
    require balanceOf(sender) >= amount;
    require recipient != address(0);

    assert transfer(recipient, amount, env with msg.sender = sender), "Transfer should not revert under valid conditions";
}

//// ## Approval rules
rule onlyHolderCanChangeAllowance(address holder, address spender, uint amount) {
    old uint oldAllowance = allowance(holder, spender);
    assert approve(spender, amount, env with msg.sender = holder), "Approval must succeed";
    assert allowance(holder, spender) == amount, "Allowance must be correctly set";
}

//// ## Invariants
invariant balanceAddressZero() {
    assert balanceOf(address(0)) == 0, "Balance of address zero must always be zero";
}

//// ## Ghosts and hooks to maintain the total supply correctly
ghost uint sum_of_balances = 0;

hook Sstore balanceOf[address a] uint new_value (uint old_value) {
    sum_of_balances = sum_of_balances - old_value + new_value;
}

invariant totalSupplyIsSumOfBalances() {
    assert totalSupply() == sum_of_balances, "Total supply must be equal to the sum of all balances";
}
