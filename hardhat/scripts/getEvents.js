const hre = require('hardhat');
const abi = require('./xcallAbi.json');

async function main() {    
    // tx hash
    const hash = "0x227ac4cc33c877735370e5824bbdf2a9b3ede4d4208c30dc7951a6977f4e78cf"

    const receipt = await hre.ethers.provider.getTransactionReceipt(hash)
    // console.log(receipt);
   
    if (receipt.logs && receipt.logs.length > 0) {
        console.log("Event logs:");
        for (const log of receipt.logs) {
            // Get the event ABI based on the log's topic (event signature)
            const eventAbi = abi.find((a) => a.signature === log.topics[0]);
            console.log(eventAbi);
        }
    }
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});