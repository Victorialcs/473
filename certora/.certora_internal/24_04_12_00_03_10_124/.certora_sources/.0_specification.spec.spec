// Specification for the ERC20 token MyToken

// Declarations of external functions
extern function allowance(address, address) returns (uint256) envfree;
extern function balanceOf(address) returns (uint256) envfree;
extern function totalSupply() returns (uint256) envfree;
extern function transfer(address, uint256) returns (bool);
extern function approve(address, uint256) returns (bool);

// Basic accessibility rule for non-reverting paths
rule eachMethodIsReachable() {
    env e;
    calldataarg args;

    assert exists (function f in {allowance, balanceOf, totalSupply, transfer, approve}) {
        f(e, args);
        !lastReverted;
    } "Each method should have a non-reverting path.";
}

// Rule for transfer behavior
rule transferSpec(address sender, address recipient, uint256 amount) {
    require sender != recipient, "Sender and recipient cannot be the same.";
    require balanceOf(sender) >= amount, "Sender does not have enough balance.";

    old uint256 senderOldBalance = balanceOf(sender);
    old uint256 recipientOldBalance = balanceOf(recipient);

    bool success = transfer(recipient, amount);
    assert success, "Transfer should succeed";

    assert balanceOf(sender) == senderOldBalance - amount, "Sender's balance should decrease by the transferred amount.";
    assert balanceOf(recipient) == recipientOldBalance + amount, "Recipient's balance should increase by the transferred amount.";
}

// More rules and invariants can be added similarly...

