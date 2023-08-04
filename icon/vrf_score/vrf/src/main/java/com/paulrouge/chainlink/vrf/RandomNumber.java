package com.paulrouge.chainlink.vrf;


/** 
 * This is a example of how to use the xCall Berlin VRF Random Number Generator
 * Do not use this in production, this is just an example to showcase xCall.
 * 
 * 
 * Note to self: maybe add a restriction to reqeustRandom number that only allows for calls 
 * when the current randomNumrequestId has been fulfilled.
 * 
*/


import score.Context;
import score.annotation.External;
import score.annotation.Optional;
import score.annotation.Payable;
import score.annotation.EventLog;
// import score.annotation.Payable;
import score.Address;
import score.VarDB;

import java.math.BigInteger;
import com.paulrouge.chainlink.vrf.mapping.EnumerableMap;



public class RandomNumber {
    public String name = "xCall - Chainlink VRF Random Number Generator";
    private BigInteger randomNumrequestId = BigInteger.ZERO;
    public Address xCallAddress = Address.fromString("cxf4958b242a264fc11d7d8d95f79035e35b21c1bb");

    // map [randomNumrequestId => vrf id]
    EnumerableMap <BigInteger, BigInteger> vrfIds = new EnumerableMap<BigInteger, BigInteger>("vrfIds", BigInteger.class, BigInteger.class);

    // map [randomNumrequestId => vrf result]
    EnumerableMap <BigInteger, BigInteger> vrfResults = new EnumerableMap<BigInteger, BigInteger>("vrfResults", BigInteger.class, BigInteger.class);

    // map [randomNumrequestId => address]
    EnumerableMap <BigInteger, Address> randomNumrequestIdToAddress = new EnumerableMap<BigInteger, Address>("randomNumrequestIdToAddress", BigInteger.class, Address.class);

    public String btpAddressSepoliaDapp = "test";

    // @External(readonly=true)
    // public String getTest() {
    //     return this.test;
    // }

    // @External
    // public void setTest(String _test) {
    //     this.test = _test;
    // }


    // constructor
    public RandomNumber() {
        Context.println("contract deployed!");
    }

    @External
    public void setBtpAddressSepoliaDapp(String _btpAddressSepoliaDapp) {
        // Context.require(Context.getCaller().equals(Context.getOwner()), "Only owner can set btpAddressSepoliaDapp");
        this.btpAddressSepoliaDapp = _btpAddressSepoliaDapp;
    }

    @External(readonly=true)
    public String getBtpAddressSepoliaDapp() {
        return this.btpAddressSepoliaDapp;
    }


    // returns the vrfId of the given randomNumrequestId
    @External(readonly=true)
    public BigInteger getVrfId(BigInteger _randomNumrequestId) {
        return vrfIds.getOrDefault(_randomNumrequestId, BigInteger.ZERO);
    }

    // returns the vrf result of the given randomNumrequestId
    @External(readonly=true)
    public BigInteger getVrfResult(BigInteger _randomNumrequestId) {
        return vrfResults.getOrDefault(_randomNumrequestId, BigInteger.ZERO);
    }

    // returns the address of the given randomNumrequestId
    // @External(readonly=true)
    // public Address getAddress(BigInteger _randomNumrequestId) {
    //     return randomNumrequestIdToAddress.get(_randomNumrequestId);
    // }

    @External(readonly=true)
    public BigInteger getSepoliaFee() {
        return Context.call(BigInteger.class, xCallAddress, "getFee", "0xaa36a7.eth2", "0x0");
    }


    private BigInteger _sendCallMessage(byte[] _data, @Optional byte[] _rollback) {
        Address xcallSourceAddress = Address.fromString("cxf4958b242a264fc11d7d8d95f79035e35b21c1bb");
        String _to = "btp://0xaa36a7.eth2/0x5F326A7Cecb9510355324977901942bf5018d14F";
        return Context.call(BigInteger.class, Context.getValue(), xcallSourceAddress, "sendCallMessage", _to, _data, _rollback);
    }

    // make a request for a random number
    @External
    @Payable
    public void requestRandomNumber() {
        // BigInteger fee = new BigInteger("6089463169230770176");
        
        // check if contract has enough balance
        // Context.require(Context.getBalance(Context.getAddress()).compareTo(fee) >= 0, "Not enough balance");
        
        // call sendMessage on xCall Berlin address with fee as value, dapp address and data as param
        BigInteger id =Context.call(BigInteger.class, Context.getValue(), Address.fromString("cxf4958b242a264fc11d7d8d95f79035e35b21c1bb"), "sendCallMessage", "btp://0xaa36a7.eth2/0x5F326A7Cecb9510355324977901942bf5018d14F", "0x".getBytes());
        // BigInteger id = _sendCallMessage("0x".getBytes(), "0x".getBytes());
        // Context.call(BigInteger.class, Context.getValue(), xcallSourceAddress, "sendCallMessage", _to, _data);
        TestCall(id);

        // emit event with randomNumrequestId
        // RandomNumberRequestReceived(Context.getAddress().toString(), this.randomNumrequestId);
        
        // // increment randomNumrequestId
        // randomNumrequestId = randomNumrequestId.add(BigInteger.ONE);

        // // map randomNumrequestId to address
        // randomNumrequestIdToAddress.set(randomNumrequestId, Context.getAddress());
        // Context.transfer(Context.getCaller(), Context.getValue());
    }

    // callback function for xCall Berlin
    void receiveRandomNumber(BigInteger _vrfResult) {
        // only xCall Berlin can call this function
        Context.require(Context.getCaller().equals(xCallAddress), "Only xCall can call this function");
        
        // map result to previous randomNumrequestId
        // BigInteger _randomNumrequestId = randomNumrequestId.subtract(BigInteger.ONE);
        
        // map randomNumrequestId to vrf result
        // vrfResults.set(_randomNumrequestId, _vrfResult);
    }

    // xCall func    
    @External 
    public void handleCallMessage(String _from, byte[] _data) {
        Context.require(Context.getCaller().equals(xCallAddress), "Only xCall can call this function");
        receiveRandomNumber(new BigInteger(_data));
    }


    @Payable
    public void fallback(){};

    @EventLog
    public void RandomNumberRequestReceived(String _from, BigInteger _randomNumberRequestId) {}

    @EventLog
    public void TestCall(BigInteger _resp) {}
}