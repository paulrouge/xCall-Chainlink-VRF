package com.paulrouge.chainlink.vrf;

/** 
 * This is a example of how to use the xCall Berlin VRF Random Number Generator
 * Do not use this in production, this is just an example to showcase xCall.
*/

import score.Context;
import score.annotation.External;
import score.annotation.Payable;
import score.Address;

import java.math.BigInteger;
import com.paulrouge.chainlink.vrf.mapping.EnumerableMap;
import java.util.Arrays;


public class RandomNumber {
    public String contractname = "xCall - Chainlink VRF Random Number Generator";
    
    // used to keep track of the random number requests
    private BigInteger COUNTER = BigInteger.ZERO;
    public final Address xCallAddress = Address.fromString("cxf4958b242a264fc11d7d8d95f79035e35b21c1bb");

    // map [randomNumrequestId => vrf result]
    EnumerableMap <BigInteger, BigInteger> VRFResults = new EnumerableMap<BigInteger, BigInteger>("vrfResults", BigInteger.class, BigInteger.class);

    // map [randomNumrequestId => address]
    EnumerableMap <BigInteger, Address> requestIdToAddress = new EnumerableMap<BigInteger, Address>("randomNumrequestIdToAddress", BigInteger.class, Address.class);

    public String btpAddressSepoliaDapp = "test";

    @External(readonly=true)
    public String name() {
        return this.contractname;
    }

    @External
    public void setBtpAddressSepoliaDapp(String _btpAddressSepoliaDapp) {
        Context.require(Context.getCaller().equals(Context.getOwner()), "Only owner can set btpAddressSepoliaDapp");
        this.btpAddressSepoliaDapp = _btpAddressSepoliaDapp;
    }

    @External(readonly=true)
    public String getBtpAddressSepoliaDapp() {
        return this.btpAddressSepoliaDapp;
    }

    // returns the vrf result of the given randomNumrequestId
    @External(readonly=true)
    public BigInteger getVRFResult(BigInteger _randomNumrequestId) {
        return VRFResults.getOrDefault(_randomNumrequestId, BigInteger.ZERO);
    }

    // returns the address of the given randomNumrequestId
    @External(readonly=true)
    public Address getAddress(BigInteger _randomNumrequestId) {
        return requestIdToAddress.get(_randomNumrequestId);
    }


    @External(readonly = true)
    public BigInteger getCounter() {
        return this.COUNTER;
    }


    // get xcall address
    @External(readonly=true)
    public Address getXcallAddress() {
        return xCallAddress;
    }

    // make a request for a random number, user should pay for the xCall fee while calling this function
    @External
    @Payable
    public void requestRandomNumber() {
        // counter to bytes
        byte[] _COUNTER = this.COUNTER.toByteArray();
        
        // call sendMessage on xCall Berlin address with fee as value, dapp address and data as param
        Context.call(BigInteger.class, Context.getValue(), Address.fromString("cxf4958b242a264fc11d7d8d95f79035e35b21c1bb"), "sendCallMessage", this.btpAddressSepoliaDapp, _COUNTER);
        
        // map randomNumrequestId to address
        requestIdToAddress.set(COUNTER, Context.getCaller());

        // increment randomNumrequestId
        this.COUNTER = this.COUNTER.add(BigInteger.ONE);
    }

    // callback function for xCall Berlin
    void receiveRandomNumber(BigInteger _reqId, BigInteger _vrfResult) {
        // only xCall Berlin can call this function - comment out during testing
        // Context.require(Context.getCaller().equals(xCallAddress), "Only xCall can call this function");
        
        // map randomNumrequestId to vrf result
        VRFResults.set(_reqId, _vrfResult);
    }

    // xCall func    
    @External 
    public void handleCallMessage(String _from, byte[] _data) {
        // only xCall Berlin can call this function - comment out during testing
        // Context.require(Context.getCaller().equals(xCallAddress), "Only xCall can call this function");
    
        // split the data into the randomNumrequestId and the vrf result
        byte[] _randomNumrequestId = Arrays.copyOfRange(_data, 0, 32);
        byte[] _vrfResult = Arrays.copyOfRange(_data, 32, _data.length);

        BigInteger reqId = new BigInteger(_randomNumrequestId); 
        BigInteger res = new BigInteger(1, _vrfResult); // >128b so set sign to positive with 1

        // store the vrf result
        receiveRandomNumber(reqId, res);
    }


    @Payable
    public void fallback(){};

}