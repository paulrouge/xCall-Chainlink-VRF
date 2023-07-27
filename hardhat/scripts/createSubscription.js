const hre = require('hardhat');
const { ethers } = require('ethers'); 

async function main() {
    const VRF_CONTRACT_ADDRESS = '0xa2d23627bC0314f4Cbd08Ff54EcB89bb45685053'
    

    const testVRFCoordinatorContract = await hre.ethers.getContractFactory('VRFConsumerBase')
    const contract = await testVRFCoordinatorContract.attach(VRF_CONTRACT_ADDRESS)
        try {
        const obj = await contract.createSubscription()
        assert.isObject(obj, 'createSubscription failed')
        ethers.provider.on(
            {
            address: VRF_CONTRACT_ADDRESS,
            topics: [
                '0x464722b4166576d3dcbba877b999bc35cf911f4eaf434b7eba68fa113951d0bf',
            ],
            },
            (log) => {
            const subId = BigNumber.from(log.topics[1]).toNumber()
            const caller = BigNumber.from(log.data).toHexString()
            console.log(`subId: ${subId},caller: ${caller}`)
            },
        )
        } catch (e) {
        assert.fail('createSubscription failed')
        }

}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});