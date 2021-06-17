const express = require('express');
const app = express();

app.use('/public', express.static('public'));

app.get('/server', (request, response) => {
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.sendFile('/templates/GET.html', {root: __dirname});
    //.send('HELLO, AJAX');
});

app.get('/home', (request, response) => {
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.sendFile(__dirname + '/templates/home.html');
});

app.get('/sayhello', (request, response) => {
    response.send("HELLO JS!");
})

app.listen(8000, () => {
    console.log("server started, 8000 port is listening");
});