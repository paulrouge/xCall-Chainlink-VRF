const hre = require('hardhat');

// sepolia VRF Coordinator
const vrfCoordinator = '0x8103B0A8A00be2DDC778e6e7eaa21791Cd364625';
// sepolia VRF key hash
const vrfKeyHash = "0x474e34a077df58807dbe9c96d3c009b23b3c6d0cce433e59bbf5b34f823bc56c"


// npx hardhat run --network goerli scripts/deploy.js
async function main() {
    const [deployer] = await hre.ethers.getSigners();
    console.log(`Deploying contracts with the account: ${deployer.address}`);
    
    const Contract = await hre.ethers.getContractFactory('MyToken');
    const contract = await Contract.deploy();

    // await igo.deployed();

    // console.log(`Deployed to ${igo.address}`);

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