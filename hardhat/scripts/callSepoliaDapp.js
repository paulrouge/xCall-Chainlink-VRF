const hre = require('hardhat');

async function main() {
    // const dappAddress = "0x47BA564d36eF1B5c9B51b015c32a9bF79D0aAff6"; // one of first succesufl chainlink call
    const dappAddress = "0x3D80794f07f3585f7eD0CF6c6e180C64762d80a6"
    const Contract = await hre.ethers.getContractFactory('RandomNumberConsumerV2');
    const contract = await Contract.attach(dappAddress);
    
    const berlinAdr = "cx3723d8cb8d8ac7da29f692ce2abc8156423631be" // Berlin contract address

    if (berlindAdr == "") {
        console.log("Please set the Berlin address")
        return
    }

    const btpAddressBerlinDapp = "btp://0x7.icon/" + berlinAdr
    const setBtpAddressBerlinDapp = await contract.setDappAddressBerlin(btpAddressBerlinDapp, { gasLimit: 20000000 })
    const receipt = await setBtpAddressBerlinDapp.wait()
    console.log(receipt);

}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});