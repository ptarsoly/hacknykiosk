
const authNetCreds = require('./config-authnet.json');
//require authorize.net stuff
var ApiContracts = require('authorizenet').APIContracts;
var ApiControllers = require('authorizenet').APIControllers;

const HIDStream = require('node-hid-stream').KeyboardLines;
var bodyParser = require('body-parser');
const EventEmitter = require('events');

const axios = require('axios');

const input = require('./arduino.js');
var express = require('express');
var cors = require('cors');
var app = express();

const cardInfo = new EventEmitter();

let device;
let paySuccessful = false;

try {
    device = new HIDStream({ vendorId: 2049, productId: 1 }); // reader init
} catch (error) {
    console.log(error);
    return;
}

device.on('data', (data) => {
    cardInfo.emit('number','5424000000000015');
    paySuccessful = true;
});

cardInfo.on('number', (data) =>{
    authorize(data,25, (response)=>{
        console.log(response.messages.resultCode);
    });
});



let mostRecentData;
let prevData;
let event = false;
app.use(cors());

input.on('test', (data) => {
    if(data == "Peter") {
        cardInfo.emit('number','4111111111111111');
        paySuccessful = true;
    }
    if(data.length == 10) {
        axios.post('muntasers twilio endpoint', {
            phoneNumber : "+1"+data.substring(0,9)
        })
    }
    event = true;
    mostRecentData = data;
    console.log(data);
});

app.listen(3001);

app.get('/data', (req, res) => {
    res.send({
        data: mostRecentData,
        new: event,
        paid: paySuccessful
    });
    paySuccessful = false;
    event = false;
    prevData = mostRecentData;

});

app.get('/rash', (req, res) => {

    res.send({
        "results": "likely",

    });
});

function authorize(cardInfo, amount, cb) {

    // Initiate the credit card authentication
    var merchantAuthenticationType = new ApiContracts.MerchantAuthenticationType();
    merchantAuthenticationType.setName(authNetCreds.apiLoginKey);
    merchantAuthenticationType.setTransactionKey(authNetCreds.transactionKey);

    var creditCard = new ApiContracts.CreditCardType();
    // Card-specific info
    creditCard.setCardNumber(cardInfo);
    creditCard.setExpirationDate('2022-10');
    creditCard.setCardCode('000');

    var paymentType = new ApiContracts.PaymentType();
    paymentType.setCreditCard(creditCard);

    var orderDetails = new ApiContracts.OrderType();

    //orderDetails.setInvoiceNumber('INV-0');
    orderDetails.setDescription('Donation');

    var transactionRequestType = new ApiContracts.TransactionRequestType();
    transactionRequestType.setTransactionType(ApiContracts.TransactionTypeEnum.AUTHONLYTRANSACTION);
    transactionRequestType.setPayment(paymentType);
    transactionRequestType.setAmount(25); //TODO: fix this
    transactionRequestType.setOrder(orderDetails);

    var createRequest = new ApiContracts.CreateTransactionRequest();
    createRequest.setMerchantAuthentication(merchantAuthenticationType);
    createRequest.setTransactionRequest(transactionRequestType);

    //pretty print request
    //console.log(JSON.stringify(createRequest.getJSON(), null, 2));

    var ctrl = new ApiControllers.CreateTransactionController(createRequest.getJSON());

    console.log('request sent');
    let response;

    ctrl.execute(function () {

        var apiResponse = ctrl.getResponse();

        response = new ApiContracts.CreateTransactionResponse(apiResponse);

        return cb(response);
    });
}