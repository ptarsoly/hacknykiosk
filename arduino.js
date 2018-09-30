var SerialPort = require('serialport');
const Readline = require('@serialport/parser-readline');
var port = new SerialPort('/dev/cu.usbmodemFD121', {
    baudRate: 115200
});

const EventEmitter = require('events');

// For use on the dragonboard:
// var port = new SerialPort('/dev/ttyACM0', {
//     baudRate: 9600
// });

const serialRec = new EventEmitter();
const parser = port.pipe(new Readline({ delimiter: '\r\n' }));


parser.on('data', (data)=>{
    serialRec.emit('test', data);
});

port.on('error', function(err) {
    console.log('Error: ', err.message);
    serialRec.emit('test','data');
});

module.exports = serialRec;