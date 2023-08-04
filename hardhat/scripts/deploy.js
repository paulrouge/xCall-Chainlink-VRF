const hre = require('hardhat');

// npx hardhat run --network goerli scripts/deploy.js
async function main() {
    const subscriptionId = 3948
    const vrfCoordinator = "0x8103B0A8A00be2DDC778e6e7eaa21791Cd364625"; // denployed on Sepolia, registered on Chainlink.com
    const keyHash = "0x474e34a077df58807dbe9c96d3c009b23b3c6d0cce433e59bbf5b34f823bc56c"  
    
    const [deployer] = await hre.ethers.getSigners();
    console.log(`Deploying contracts with the account: ${deployer.address}`);
    
    const Contract = await hre.ethers.getContractFactory('RandomNumberConsumerV2');
    const contract = await Contract.deploy(subscriptionId, vrfCoordinator, keyHash);

    // await contract.deployed(); // this errors out!

    // console.log(`Deployed to ${contract.address}`);

    // await hre.run('verify:verify', {
    //     address: igo.address,
    //     // see: https://hardhat.org/hardhat-runner/plugins/nomiclabs-hardhat-etherscan#using-programmatically
    //     constructorArguments: [],
    // });
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});