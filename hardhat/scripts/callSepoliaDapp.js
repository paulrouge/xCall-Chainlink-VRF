const hre = require('hardhat');

async function main() {
    // const dappAddress = "0x47BA564d36eF1B5c9B51b015c32a9bF79D0aAff6"; // one of first succesufl chainlink call
    const dappAddress = "0xD314dA9Ff68b07746fF2cA67554D3F3fEe778a97"
    const Contract = await hre.ethers.getContractFactory('RandomNumberConsumerV2');
    const contract = await Contract.attach(dappAddress);

    // const s_requestId = await contract.s_requestId();
    // const s_randomWords = await contract.s_randomWords(1);

    // console.log(`s_requestId: ${s_requestId}`);
    // console.log(`s_randomWords: ${s_randomWords}`);
    
    // const btpAddressBerlinDapp = "btp://0x7.icon/cxf1b0808f09138fffdb890772315aeabb37072a8a"
    // const setBtpAddressBerlinDapp = await contract.setDappAddressBerlin(btpAddressBerlinDapp, { gasLimit: 20000000 })
    // const receipt = await setBtpAddressBerlinDapp.wait()
    // console.log(receipt);

    // const getBtpAddressBerlinDapp = await contract.dappAddressBerlin()
    // console.log(getBtpAddressBerlinDapp);

    // const getXCallFee = await contract.getXCallFee("0x7.icon", true)
    // console.log(getXCallFee.toString());

    // 8449437287748447 bsctest
    // 871649011063830 sepolia

    // const sendCallMsg = await contract.sendXCallMessage(6900, { gasLimit: 20000000, value: 871649011063830 })
    // const receipt = await sendCallMsg.wait()
    // console.log(receipt);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});