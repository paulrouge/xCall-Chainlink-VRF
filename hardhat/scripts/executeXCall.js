const hre = require('hardhat');

async function main() {
    const xCallAddress = "0x694C1f5Fb4b81e730428490a1cE3dE6e32428637"; // sepolia

    // ABI of the contract (assuming 'executeCall' takes uint and string as parameters)
    const contractABI = [
        // ... ABI for other functions (if any) ...
        {
            "name": "executeCall",
            "type": "function",
            "inputs": [
                {
                    "name": "_reqId",
                    "type": "uint256"
                },
                {
                    "name": "_data",
                    "type": "bytes"
                }
            ],
            "outputs": [] // Update this if 'executeCall' has any return values
        }
    ];

    const [signer] = await hre.ethers.getSigners();
    console.log(`Sending transaction from ${signer.address}`);

    // Create a contract instance using the ABI and address
    const contract = new hre.ethers.Contract(xCallAddress, contractABI, signer); // Using the signer to send a transaction
    

    const reqId = 304;
    const data = "0x13"; // Convert the string to bytes

    try {
        // Call the 'executeCall' function with the provided parameters
        const transaction = await contract.executeCall(reqId, data , { gasLimit: 800000 });
        const receipt = await transaction.wait()

        console.log(receipt);
    } catch (error) {
        console.error("Error executing the function:", error);
    }
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});