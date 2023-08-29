// SPDX-License-Identifier: MIT
// An example of a consumer contract that relies on a subscription for funding.
pragma solidity ^0.8.7;

import "@iconfoundation/btp2-solidity-library/contracts/interfaces/ICallService.sol";
import "@chainlink/contracts/src/v0.8/interfaces/VRFCoordinatorV2Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";
import "./interfaces/ICallServiceReceiver.sol";

/**
* THIS IS AN EXAMPLE CONTRACT THAT USES HARDCODED VALUES FOR CLARITY.
* THIS IS AN EXAMPLE CONTRACT THAT USES UN-AUDITED CODE.
* DO NOT USE THIS CODE IN PRODUCTION.
*/

/**
* @title The RandomNumberConsumerV2 contract
* @notice A contract that gets random values from Chainlink VRF V2
*/
contract RandomNumberConsumerV2 is VRFConsumerBaseV2, ICallServiceReceiver {
    VRFCoordinatorV2Interface immutable COORDINATOR;

    // Your subscription ID.
    uint64 immutable s_subscriptionId;

    // The gas lane to use, which specifies the maximum gas price to bump to.
    // For a list of available gas lanes on each network,
    // see https://docs.chain.link/docs/vrf-contracts/#configurations
    bytes32 immutable s_keyHash;

    // Depends on the number of requested values that you want sent to the
    // fulfillRandomWords() function. Storing each word costs about 20,000 gas,
    // so 100,000 is a safe default for this example contract. Test and adjust
    // this limit based on the network that you select, the size of the request,
    // and the processing of the callback request in the fulfillRandomWords()
    // function.
    uint32 constant CALLBACK_GAS_LIMIT = 400000;

    // The default is 3, but you can set this higher.
    uint16 constant REQUEST_CONFIRMATIONS = 3;

    // For this example, retrieve 1 random value in one request.
    uint32 constant NUM_WORDS = 1;

    // The xCall address on Sepolia
    address constant xCallAddressSepolia = 0x694C1f5Fb4b81e730428490a1cE3dE6e32428637;

    // the btp address of the dapp on Berlin
    string public dappAddressBerlin = "btp://0x7.icon/cx3723d8cb8d8ac7da29f692ce2abc8156423631be";

    // owner can set the dapp address on Berlin
    function setDappAddressBerlin(string calldata _dappAddressBerlin) external onlyOwner {
        dappAddressBerlin = _dappAddressBerlin;
    }

    uint256 public s_requestId;
    address s_owner;

    // map berlinReqId to VRF requestId
    mapping(uint256 => uint256) public VRFReqIdtoBerlinReqId;

    event ReturnedRandomness(uint256[] randomWords);
    event My_Event_randomWordRequested(string from, uint256 requestId);
    event My_Event_xCallExecuted(string from, uint256 requestId);


    /**
    * @notice Constructor inherits VRFConsumerBaseV2
    *
    * @param subscriptionId - the subscription ID that this contract uses for funding requests
    * @param vrfCoordinator - coordinator, check https://docs.chain.link/docs/vrf-contracts/#configurations
    * @param keyHash - the gas lane to use, which specifies the maximum gas price to bump to
    */
    constructor(
        uint64 subscriptionId,
        address vrfCoordinator,
        bytes32 keyHash
    ) VRFConsumerBaseV2(vrfCoordinator) {
        COORDINATOR = VRFCoordinatorV2Interface(vrfCoordinator);
        s_keyHash = keyHash;
        s_owner = msg.sender;
        s_subscriptionId = subscriptionId;
    }


    modifier onlyOwner() {
        require(msg.sender == s_owner);
        _;
    } 


    function setBTPAddressBerlinDapp(string calldata _dappAddressBerlin) external onlyOwner {
        dappAddressBerlin = _dappAddressBerlin;
    }

    /**
    * @notice Requests randomness
    * Assumes the subscription is funded sufficiently; "Words" refers to unit of data in Computer Science
    */
    function _requestRandomWords(uint256 _berlinReqId) internal {
        // Will revert if subscription is not set and funded.
        s_requestId = COORDINATOR.requestRandomWords(
            s_keyHash,
            s_subscriptionId,
            REQUEST_CONFIRMATIONS,
            CALLBACK_GAS_LIMIT,
            NUM_WORDS
        );

        // map berlinReqId to VRF requestId
        VRFReqIdtoBerlinReqId[s_requestId] = _berlinReqId;
    }

    // for testing
    event RandomWordReceived(uint256 _value);

    // the contract will have to have funds to pay the xcall fee
    function sendXCallMessage(uint256 _berlinReqId, uint256 _randomWords) internal {
        
        uint256 xCallFee = getXCallFee("0x7.icon", false); 
        
        // ensure the contract has enough funds to pay the xcall fee
        require(address(this).balance >= xCallFee, "Not enough funds to pay the xcall fee");

        // convert to bytes
        bytes memory _berlinReqIdBytes = abi.encode(_berlinReqId);
        bytes memory _randomWordsBytes = abi.encode(_randomWords);
        bytes memory _data = abi.encodePacked(_berlinReqIdBytes, _randomWordsBytes);

        ICallService(xCallAddressSepolia).sendCallMessage{value:xCallFee}(
            dappAddressBerlin,
            _data,
            "" 
        );
    }

    /**
    * @notice Callback function used by VRF Coordinator
    *
    * @param requestId - id of the request
    * @param randomWords - array of random results from VRF Coordinator
    */
    function fulfillRandomWords(
        uint256 requestId,
        uint256[] memory randomWords
    ) internal override {

        uint256 randomWord = randomWords[0];
        emit RandomWordReceived(randomWord);
        
        sendXCallMessage(VRFReqIdtoBerlinReqId[requestId], randomWord);
    }


    function getXCallFee(string memory _to, bool _response) public view returns (uint) {
        bytes4 functionSelector = bytes4(keccak256("getFee(string,bool)"));
        (bool success, bytes memory result) = xCallAddressSepolia.staticcall(abi.encodeWithSelector(functionSelector, _to, _response));
        require(success, "getFee failed");
        return abi.decode(result, (uint256));
    }


    function bytesToUint256(bytes memory input) internal pure returns (uint256) {
        require(input.length <= 32, "Input length exceeds 32 bytes");
        uint256 result = 0;
        for (uint256 i = 0; i < input.length; i++) {
            result = result * 256 + uint256(uint8(input[i]));
        }
        return result;
    }


    /**
    @notice Handles the call message received from the source chain.
    @dev Only called from the Call Message Service.
    @param _from The BTP address of the caller on the source chain
    @param _data The calldata delivered from the caller
    */
    function handleCallMessage(
        string calldata _from,
        bytes calldata _data
    ) external override onlyCallService {
        // the reqId on the randomword contract, not to be confused with the xCall reqId
        uint256 _berlinReqId = bytesToUint256(_data);
        _requestRandomWords(_berlinReqId);
    }

    modifier onlyCallService() {
        require(msg.sender == xCallAddressSepolia);
        _;
    }

    // for testing call requestRandomWords
    function requestRandomWords(uint256 _berlinReqId) external {
        _requestRandomWords(_berlinReqId);
    }

    // receive ether - contract needs to be able to hold funds to pay xcall fee
    receive() external payable {}
}
