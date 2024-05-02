import subprocess
import tempfile
import sys

def run_slither_on_contract(contract_code):
    slither_output = None  # Initialize slither_output variable

    # Write the contract code to a temporary file with a '.sol' extension
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".sol") as temp_file:
        temp_file.write(contract_code)
        temp_file_path = temp_file.name

    command = f"slither {temp_file_path}"

    # Run the command and capture the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        print("Slither executed successfully.")
        slither_output = result.stdout
        print("Output:")
        print(slither_output)
    else:
        print("Error executing Slither.")
        print("Error message:")
        print(result.stderr)

    # Clean up the temporary file
    temp_file.close()

    return slither_output

def main():
    contract_code = """
       pragma solidity ^0.8.0;

contract MyToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(string memory _name, string memory _symbol, uint8 _decimals, uint256 _initialSupply) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= balanceOf[_from], "Insufficient balance");
        require(_value <= allowance[_from][msg.sender], "Allowance exceeded");
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
}
        """

    print(run_slither_on_contract(contract_code))

if __name__ == "__main__":
    main()


