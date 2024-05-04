/***
 * # Aggregator Specification
 *
 * This specification defines the behavior for the Aggregator contract.
 */

methods {
    function addAuthorizedSource(address) external;
    function removeAuthorizedSource(address) external;
    function updateData(bytes32, uint256[]) external;
    function getData(bytes32) external view returns(uint256[], uint256) envfree;
    function authorizedSources(address) external view returns(bool) envfree;
    function data(bytes32) external view returns(uint256[], uint256) envfree;
}

//// ## Part 1: Basic Rules ////////////////////////////////////////////////////
/*
    Property: Ensure all methods are reachable.
*/
rule reachability(method f) {
    env e;
    calldataarg args;
    f(e, args);
    satisfy true, "A non-reverting path through this method was found";
}

/// Adding a source should authorize it for data updates.
rule addSourceSpec {
    address newSource;

    require !authorizedSources(newSource);

    env e;
    addAuthorizedSource(e, newSource);

    assert authorizedSources(newSource), "New source should be authorized";
}

/// Removing a source should de-authorize it for data updates.
rule removeSourceSpec {
    address existingSource;

    require authorizedSources(existingSource);

    env e;
    removeAuthorizedSource(e, existingSource);

    assert !authorizedSources(existingSource), "Source should no longer be authorized";
}

/// Ensure that only authorized sources can update data.
rule onlyAuthorizedCanUpdate {
    bytes32 dataKey;
    uint256[] newValues;

    env e;
    require !authorizedSources(e.msg.sender);

    updateData@withrevert(e, dataKey, newValues);

    assert lastReverted, "Only authorized sources should be able to update data";
}

/// Data updates should emit the DataUpdated event.
rule dataUpdateEvent {
    bytes32 dataKey;
    uint256[] newValues;

    env e;
    require authorizedSources(e.msg.sender);

    updateData(e, dataKey, newValues);

    assert emitted(DataUpdated(dataKey, newValues)), "DataUpdated event should be emitted";
}

/// The latestValue should reflect the average of the values array.
rule latestValueIsAverage {
    bytes32 dataKey;
    uint256[] values;
    uint256 expectedAverage = calculateAverage(values);

    env e;
    require authorizedSources(e.msg.sender);

    updateData(e, dataKey, values);

    (uint256[] memory storedValues, uint256 latestValue) = getData(dataKey);

    assert latestValue == expectedAverage, "latestValue should match the calculated average";
}

//// ## Part 2: Invariants /////////////////////////////////////////////////////

/// The `authorizedSources` mapping should be consistent.
invariant allSourcesConsistent {
    address source;
    bool authorized = authorizedSources(source);

    preserved addAuthorizedSource(source) with (env e) {
        require e.msg.sender != source;
    }

    preserved removeAuthorizedSource(source) with (env e) {
        require e.msg.sender != source;
    }
}
