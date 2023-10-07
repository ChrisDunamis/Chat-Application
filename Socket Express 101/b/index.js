const express = require('express')
const app = express()
const port = 8000

// app.get('/', (req, res) => res.send('Hello World!'));
// app.get('/chris', (req, res) => res.send('Hello to CHRIS World!'));

app.use(express.static(__dirname + '/public'));

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`));

//