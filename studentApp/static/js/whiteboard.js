const canvas = document.getElementById('canvas');
const eraser = document.getElementById('eraser');
const ctx = canvas.getContext('2d');
const form = document.querySelector('form');

ctx.canvas.width  = window.innerWidth;
ctx.canvas.height = window.innerHeight;
let drawing = false;
let lastX = 0;
let lastY = 0;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

function toggleEraser(){
    if (eraser.checked){
        ctx.strokeStyle = "#ffffff";
    }
    else{
        ctx.strokeStyle = "#000000";
    }

}

eraser.addEventListener("change", toggleEraser)


function load_image_on_canvas(){
    const image_url = document.querySelector('#jsonData').getAttribute('data-json')
    const img = new Image();
    img.onload = () =>{
        ctx.drawImage(img,0,0);
    }

    img.src = image_url;

}

function startDrawing(e) {
    drawing = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
}

function draw(e) {
    if (!drawing) return;
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    lastX = e.offsetX;
    lastY = e.offsetY;
}

function stopDrawing() {
    drawing = false;
}

form.addEventListener('submit', function (e) {
    e.preventDefault();
    const image_data = canvas.toDataURL('image/png');
    document.getElementById('image_data').value = image_data;
    form.submit();
});

load_image_on_canvas();