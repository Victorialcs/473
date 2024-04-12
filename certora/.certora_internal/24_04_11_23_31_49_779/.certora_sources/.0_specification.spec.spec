// Importing types and libraries if necessary
// (Certora might provide libraries for common contract types like ERC20)

// Specification for MyToken
specification MyTokenSpec {

    // External function declarations that map to your Solidity contract
    function balanceOf(address) external returns (uint);
    function totalSupply() external returns (uint);
    function transfer(address to, uint amount) external returns (bool);

    // Invariants and rules
    invariant TotalSupplyInvariant {
        totalSupply() == sum(balanceOf(a) for all a);
    }

    rule TransferDecreasesBalance(address from, address to, uint amount) {
        old uint fromBalance = balanceOf(from);
        old uint toBalance = balanceOf(to);

        require from != to;
        require fromBalance >= amount;

        transfer(to, amount);

        assert balanceOf(from) == fromBalance - amount;
        assert balanceOf(to) == toBalance + amount;
    }
}
