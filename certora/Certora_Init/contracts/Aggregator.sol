pragma solidity ^0.8.0;

// Import OpenZeppelin library for SafeMath
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Aggregator {
    using SafeMath for uint256;

    // Struct to store data from different sources
    struct Data {
        uint256[] values;
        uint256 latestValue;
    }

    mapping(address => bool) public authorizedSources;
    mapping(bytes32 => Data) public data;

    event DataUpdated(bytes32 indexed dataKey, uint256[] values);

    modifier onlyAuthorizedSource() {
        require(authorizedSources[msg.sender], "Sender is not authorized as a source");
        _;
    }

    constructor(address[] memory _initialSources) {
        for (uint256 i = 0; i < _initialSources.length; i++) {
            authorizedSources[_initialSources[i]] = true;
        }
    }

    function addAuthorizedSource(address _source) external {
        require(!authorizedSources[_source], "Source is already authorized");
        authorizedSources[_source] = true;
    }

    function removeAuthorizedSource(address _source) external {
        require(authorizedSources[_source], "Source is not authorized");
        authorizedSources[_source] = false;
    }

    function updateData(bytes32 _dataKey, uint256[] memory _values) external onlyAuthorizedSource {
        data[_dataKey].values = _values;
        data[_dataKey].latestValue = calculateAverage(_values);
        emit DataUpdated(_dataKey, _values);
    }

    function calculateAverage(uint256[] memory _values) internal pure returns (uint256) {
        uint256 sum = 0;
        for (uint256 i = 0; i < _values.length; i++) {
            sum = sum.add(_values[i]);
        }
        return _values.length > 0 ? sum.div(_values.length) : 0;
    }

    function getData(bytes32 _dataKey) external view returns (uint256[] memory values, uint256 latestValue) {
        values = data[_dataKey].values;
        latestValue = data[_dataKey].latestValue;
    }
}
