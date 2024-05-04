module spec

import solidity

contract MyToken:
    const name: string
    const symbol: string
    const decimals: uint8
    const totalSupply: uint256
    const balanceOf: (address, uint256)
    const allowance: ((address, address), uint256)
    event Transfer: (address, address, uint256)
    event Approval: (address, address, uint256)

specification:
    property initial_supply_assigned_correctly:
        forall (creator: address):
            balanceOf(creator, totalSupply) == totalSupply

    property transfer_function_correct:
        forall (from: address, to: address, value: uint256):
            if balanceOf(from, _) >= value:
                balanceOf(from, _) - value == balanceOf(from, _) &&
                balanceOf(to, _) + value == balanceOf(to, _) &&
                exists (event: Transfer): event.from == from && event.to == to && event.value == value

    property approve_function_correct:
        forall (owner: address, spender: address, value: uint256):
            allowance(owner, spender) == value &&
            exists (event: Approval): event.owner == owner && event.spender == spender && event.value == value

    property transferFrom_function_correct:
        forall (from: address, to: address, spender: address, value: uint256):
            if allowance(from, spender) >= value:
                balanceOf(from, _) - value == balanceOf(from, _) &&
                balanceOf(to, _) + value == balanceOf(to, _) &&
                allowance(from, spender) - value == allowance(from, spender) &&
                exists (event: Transfer): event.from == from && event.to == to && event.value == value
