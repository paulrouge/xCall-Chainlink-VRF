# xCall Chainlink VRF

__IMPORTANT: This repository is only for showcasing purposes, it is not meant to be used in production. Do not use it in production!__

This repository contains the xCall Chainlink VRF smart contract, which is used to generate random numbers for the xCall protocol. It also contains a ICON SCORE (smart contract) that invokes the Chainlink VRF smart contract via xCall.

Read this article first on how to use this repository: https://medium.com/@0xpaulrouge/connecting-chainlink-to-icon-via-xcall-e28cc4e62917

## EVM
The contract to deploy on Sepolia is located in the `hardhat/contracts/VRFv2Consumer.sol` file.

## ICON
The SCORE to deploy on Berlin (ICON's Testnet) is located in the `icon/vrf_score/vrf/src/main/java/com/paulrouge/chainlink/vrf/RandomNumber.java` file.

## How to use
1. Clone this repository
2. Deploy the EVM contract with the correct parameters (check the deploy script in `hardhat/scripts/deploy.js`*)
3. Deploy the ICON SCORE with the correct parameters, if you want you can use the python script in `icon/main.py` to deploy the SCORE and interacting with it.*
4. make sure that on the Sepolia contract, the correct Berlin address is set (use `hardhat/scripts/callSepoliaDapp.js` for that)
5. make sure that on the Berlin SCORE, the correct Sepolia address is set (use `icon/main.py`*)
6. call the `requestRandomNumber` function on the Berlin SCORE (use `icon/main.py`*)

* = you can ofcourse use your own ways to deploy and interact with the contracts, this is just an example. If you want to use the example scripts from this repo you might run into some dependency issues, so make sure to install all dependencies in that case.