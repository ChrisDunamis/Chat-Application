
console.log('I am a javascript backend engine !!!');

// function addOne (xyz) {
//     console.log(xyz+1);
// }

// const addOne = (xyz, bb) => {
//     console.log(xyz+1+bb);
//     return xyz+bb;
// }

// const addOne = (xyz, bb) => (xyz+bb+100);
// let myVar = addOne(200, 10);
// console.log(myVar);

// setInterval(()=>{
//     console.log("1 second has passed");
//     const addOne = 1;
//     addOne = 2;
// }, 1000);


const http = require('http');

const server = http.createServer((req, res)=>{
    console.log('Hey Buddy, what are you doing here ?');
    // console.log(req.headers);
    res.end('{"my":1}');
});

server.listen(8000);

// following all will give response {"my":1} ; because we are not listening to the path , we are just listening for '/'
// http://localhoost:8000/index.html
// http://localhoost:8000/a/b/c
// http://localhoost:8000/
