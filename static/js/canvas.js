window.addEventListener("load", () => {
    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext("2d");


    //Resizing
    var ph = window.innerHeight
    var pw = window.innerWidth
    canvas.height = ph
    canvas.width = pw

    var background = new Image();
    background.src = "../test_data/1.png";

    background.onload = function() {
        ctx.drawImage(background, 0, 0);
    }

    //variables
    let painting = false;

    function startPosition(e) {
        painting = true;
        draw(e)
    }

    function finishedPosition() {
        painting = false;
        ctx.beginPath()
    }

    function draw(e) {
        if (!painting) return;
        ctx.lineWidth = 20;
        ctx.lineCap = "round";
        ctx.strokeStyle = "white";

        ctx.lineTo(e.clientX, e.clientY)
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.clientX, e.clientY);
    }


    //Event listeners
    canvas.addEventListener("mousedown", startPosition)
    canvas.addEventListener("mouseup", finishedPosition)
    canvas.addEventListener("mousemove", draw)
});
// var canvas = document.getElementById("canvas"),
//     ctx = canvas.getContext("2d");

// canvas.width = 934;
// canvas.height = 622;


// var background = new Image();
// background.src = "../test_data/1.png";

// background.onload = function () {
//     ctx.drawImage(background, 0, 0);
// }
// canvas animation setup
// var backgroundImage = new Image();
// backgroundImage.src = 'http://www.samskirrow.com/images/main-bg.jpg';
// var canvas;
// var context;

// function init(c) {
//     canvas = document.getElementById(c);
//     context = canvas.getContext("2d");
//     soundManager.onready(function() {
//         initSound(clientID, playlistUrl);
//     });
//     aniloop();
// }

// function aniloop() {
//     requestAnimFrame(aniloop);
//     drawWave();
// }

// function drawWave() {

//     var step = 10;
//     var scale = 60;

//     // clear
//     context.drawImage(backgroundImage, 0, 0);
//     context.fillRect(0, 0, canvas.width, canvas.height);

//     // left wave
//     context.beginPath();

//     for (var i = 0; i < 256; i++) {

//         var l = (i / (256 - step)) * 1000;
//         var t = (scale + waveLeft[i] * -scale);

//         if (i == 0) {
//             context.moveTo(l, t);
//         } else {
//             context.lineTo(l, t); //change '128' to vary height of wave, change '256' to move wave up or down.
//         }
//     }

//     context.stroke();


//     // right wave
//     context.beginPath();
//     context.moveTo(0, 256);
//     for (var i = 0; i < 256; i++) {

//         context.lineTo(4 * i, 255 + waveRight[i] * 128.);
//     }
//     context.lineWidth = 0.5;
//     context.strokeStyle = "#ff19a7";
//     context.stroke();
// }

// function updateWave(sound) {
//     waveLeft = sound.waveformData.left;
// }

// return {
//     init: init
// };