const ewelink = require('ewelink-api');
const Net = require('net');
const port = 10000;
const host = 'localhost';
// TCP Client
const client = new Net.Socket();
const connection = new ewelink({
    email: '',
    password: '',
    region: 'eu',
  });
// Status variables
var hotfloor;

client.connect({ port: port, host: host }), function() {

    console.log('TCP connection established with the server.');
    client.write('Hello, server.');
};

client.on('data', function(chunk) {
    console.log(`Data received from the server: ${chunk.toString()}`);
    if(chunk.toString() == 'Hotfloor ON')
    {
        hotfloor = true;
        connection.setDevicePowerState('1000c419d1', 'on');
        console.log('Hotfloor ON= ', hotfloor);
    }
    else if(chunk.toString() == 'Hotfloor OFF')
    {
        hotfloor = false;
        connection.setDevicePowerState('1000c419d1', 'off');
        console.log('Hotfloor OFF = ', hotfloor);
    }
    client.end();
});

client.on('end', function() {
    console.log('Requested an end to the TCP connection');
});
