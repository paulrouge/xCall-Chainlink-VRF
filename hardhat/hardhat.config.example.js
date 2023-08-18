require("@nomicfoundation/hardhat-toolbox");
const dotenv = require('dotenv');
dotenv.config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
          enabled: true,
          runs: 1000,
      },
      viaIR: true,
    },
  },
  networks: {
    localhost: {
      url: 'http://127.0.0.1:8545/',
      chainId: 31337,
      accounts: [],
    },
    ganache: {
        url: 'http://127.0.0.1:7545',
        chainId: 1337,
        accounts: [],
    },
    bscTestnet: {
        url: 'https://data-seed-prebsc-1-s1.binance.org:8545',
        chainId: 97,
        accounts: [
          process.env.PRIVATE_KEY_SEPOLIA_MM,
        ],
    },
    sepolia: {
      url: "https://ethereum-sepolia-rpc.allthatnode.com", 
      chainId: 11155111, 
      accounts: [process.env.PRIVATE_KEY_SEPOLIA_MM],
    },
  },
  etherscan: {
      apiKey: {
        mainnet: process.env.ETHERSCAN_API_KEY_BSC_MAIN,
        bscTestnet: process.env.ETHERSCAN_API_KEY_BSC_TEST,
        sepolia: process.env.ETHERSCAN_API_KEY_SEPOLIA,
      },
  },
};
