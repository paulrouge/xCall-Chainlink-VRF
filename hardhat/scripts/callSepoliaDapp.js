const hre = require('hardhat');

async function main() {
    // const dappAddress = "0x47BA564d36eF1B5c9B51b015c32a9bF79D0aAff6"; // one of first succesufl chainlink call
    const dappAddress = "0x3D80794f07f3585f7eD0CF6c6e180C64762d80a6"
    const Contract = await hre.ethers.getContractFactory('RandomNumberConsumerV2');
    const contract = await Contract.attach(dappAddress);
    
    // const s_requestId = await contract.s_requestId();
    // const s_randomWords = await contract.s_randomWords(1);
    // console.log("s_randomWords:", s_randomWords);
    
    const btpAddressBerlinDapp = "btp://0x7.icon/cx6a60548cbceb3c3491c47e0ce934ca7cf14f05c1"
    const setBtpAddressBerlinDapp = await contract.setDappAddressBerlin(btpAddressBerlinDapp, { gasLimit: 20000000 })
    const receipt = await setBtpAddressBerlinDapp.wait()
    console.log(receipt);

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