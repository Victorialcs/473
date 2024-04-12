// Specification for MyToken

// Define external functions as they are used in the Solidity contract
extern balanceOf(address) returns (uint256) envfree;
extern totalSupply() returns (uint256) envfree;
extern transfer(address recipient, uint256 amount) returns (bool);
extern approve(address spender, uint256 amount) returns (bool);
extern allowance(address owner, address spender) returns (uint256) envfree;

// Ghost state to track the computed sum of all balances
ghost mathint sum_of_balances;

// Initialize ghost variable
rule init() {
    onInit {
        sum_of_balances = 0;
    }
}

// Hook to track changes in balances
hook balanceOf[address a] on Sstore(uint256 newValue, uint256 oldValue) {
    sum_of_balances = sum_of_balances - oldValue + newValue;
}

// Invariant to check if the total supply matches the sum of all balances
invariant totalSupplyMatches() {
    assert totalSupply() == sum_of_balances, "Total supply should match the sum of all balances";
}

// Rule to ensure transfer functionality behaves correctly
rule transferCorrectness(address sender, address recipient, uint256 amount) {
    assume sender != recipient;
    assume balanceOf(sender) >= amount;

    old uint256 senderOldBalance = balanceOf(sender);
    old uint256 recipientOldBalance = balanceOf(recipient);

    bool success = transfer(recipient, amount);
    assert success == true, "Transfer should succeed";

    assert balanceOf(sender) == senderOldBalance - amount, "Sender's balance should decrease by the amount";
    assert balanceOf(recipient) == recipientOldBalance + amount, "Recipient's balance should increase by the amount";
}

// Rule to verify transfer reverts correctly
rule transferShouldRevertIfInsufficientBalance(address sender, address recipient, uint256 amount) {
    assume balanceOf(sender) < amount;

    bool result = transfer(recipient, amount);
    assert result == false, "Transfer should fail if balance is insufficient";
}

// Rule for checking approval
rule approvalCheck(address owner, address spender, uint256 amount) {
    bool success = approve(spender, amount);
    assert success == true, "Approval should succeed";

    assert allowance(owner, spender) == amount, "Allowance should match the approved amount";
}
