const { expect } = require("chai");
const { BigNumber } = require("ethers");
const { ethers } = require("hardhat");

describe("ExampleContract", function () {
  let owner;
  let hardhatOurNFTContract, hardhatVrfCoordinatorV2Mock;

  beforeEach(async () => {
    [owner] = await ethers.getSigners();
    let ourContract = await ethers.getContractFactory("ExampleContract");
    let vrfCoordinatorV2Mock = await ethers.getContractFactory("VRFCoordinatorV2Mock");

    hardhatVrfCoordinatorV2Mock = await vrfCoordinatorV2Mock.deploy(0, 0);

    await hardhatVrfCoordinatorV2Mock.createSubscription();

    await hardhatVrfCoordinatorV2Mock.fundSubscription(1, ethers.utils.parseEther("7"))

    hardhatOurContract = await ourContract.deploy(1, hardhatVrfCoordinatorV2Mock.address);
  })

  it("Contract should request Random numbers successfully", async () => {
    await expect(hardhatOurContract.requestRandomNumber).to.emit(
      hardhatOurContract,
      "RequestedRandomness"
    ).withArgs( );
  });
  
//   it("Coordinator should successfully receive the request", async function () {
//     await expect(hardhatOurNFTContract.safeMint("Halley")).to.emit(
//       hardhatVrfCoordinatorV2Mock,
//       "RandomWordsRequested"
//     );
//   })

//   it("Coordinator should fulfill Random Number request", async () => {
//     let tx = await hardhatOurNFTContract.safeMint("Halley");
//     let { events } = await tx.wait();

//     let [reqId, invoker] = events.filter( x => x.event === 'RequestedRandomness')[0].args;

//     await expect(
//       hardhatVrfCoordinatorV2Mock.fulfillRandomWords(reqId, hardhatOurNFTContract.address)
//     ).to.emit(hardhatVrfCoordinatorV2Mock, "RandomWordsFulfilled")

//   });

//   it("Contract should receive Random Numbers", async () => {

//     let tx = await hardhatOurNFTContract.safeMint("Halley");
//     let { events } = await tx.wait();

//     let [reqId] = events.filter( x => x.event === 'RequestedRandomness')[0].args;

//     await expect(
//       hardhatVrfCoordinatorV2Mock.fulfillRandomWords(reqId, hardhatOurNFTContract.address)
//     ).to.emit(hardhatOurNFTContract, "ReceivedRandomness")


//     expect(await hardhatOurNFTContract.getCharacter(0))
//     .to.include(owner.address.toString(), "Halley");

//   });
});