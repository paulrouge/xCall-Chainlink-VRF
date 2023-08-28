# xCall Chainlink VRF

This repository contains the xCall Chainlink VRF smart contract, which is used to generate random numbers for the xCall protocol. It also contains a ICON SCORE (smart contract) that invokes the Chainlink VRF smart contract via xCall.

Read this article first on how to use this repository: https://medium.com/@0xpaulrouge/connecting-chainlink-to-icon-via-xcall-e28cc4e62917

## EVM
The contract to deploy on Sepolia is located in the `hardhat/contracts/VRFv2Consumer.sol` file.`

## ICON
The SCORE to deploy on Berlin (ICON's Testnet) is located in the `icon/vrf_score/vrf/src/main/java/com/paulrouge/chainlink/vrf/RandomNumber.java` file.
