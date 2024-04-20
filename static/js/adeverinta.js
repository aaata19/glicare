function showForm() {
    // apelata cand pacientul doreste sa genereze o adeverinta noua
    var form = document.getElementById('formGenerare');
    form.style.display = 'block';
}
function showFormDownload() {
    var form = document.getElementById('myForm');
    form.style.display = 'block';
}

function loadImage(event) {
    // Prevent the default action
    event.preventDefault();

    // Get the image source
    var src = event.target.src;

    // Get the canvas and its context
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');

    // Create a new image
    var img = new Image();
    img.onload = function() {
        // Set the canvas dimensions to the image dimensions
        canvas.width = img.width;
        canvas.height = img.height;

        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw the image onto the canvas
        ctx.drawImage(img, 0, 0, img.width, img.height);
        showFormDownload();
    };
    img.src = src;
}

function downloadDocument() {
    // PENTRU CA PACIENTUL SA DESCARCE ADEVERINTA
    var canvas = document.getElementById('imageCanvas');
    var imageUrl = canvas.toDataURL("image/png");
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", imageUrl);
    downloadAnchorNode.setAttribute("download", "adeverinta_medicala.png");
    document.body.appendChild(downloadAnchorNode); 
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}

function showSubmitButton() {
    // sa apara buton submit doctor
    var form = document.getElementById('submitDrawing');
    form.style.display = 'block';
}

function enableDrawing() {
    // PENTRU CA DOCTORU SA SEMNEZE
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');
    var drawing = false;
    var mousePos = { x:0, y:0 };
    showSubmitButton();
    canvas.onmousedown = function(e) {
        drawing = true;
        mousePos = getMousePos(canvas, e);
    };

    canvas.onmousemove = function(e) {
        if (!drawing) return;
        var newMousePos = getMousePos(canvas, e);
        ctx.beginPath();
        ctx.moveTo(mousePos.x, mousePos.y);
        ctx.lineTo(newMousePos.x, newMousePos.y);
        ctx.stroke();
        mousePos = newMousePos;
    };

    canvas.onmouseup = function(e) {
        drawing = false;
    };
}

function showForm() {
    var form = document.getElementById('formGenerare');
    form.style.display = 'block';
}
function showFormDownload() {
    var form = document.getElementById('myForm');
    form.style.display = 'block';
}

function loadImage(event) {
    // PENTRU A INCARCA IMAGINILE IN CANVAS
    // Prevent the default action
    event.preventDefault();

    // Get the image source
    var src = event.target.src;
    var imageId = event.target.id;
    document.getElementById('imageId').value = imageId;

    // Get the canvas and its context
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');

    // Create a new image
    var img = new Image();
    img.onload = function() {
        // Set the canvas dimensions to the image dimensions
        canvas.width = img.width;
        canvas.height = img.height;

        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw the image onto the canvas
        ctx.drawImage(img, 0, 0, img.width, img.height);
        showFormDownload();
    };
    img.src = src;
}

function downloadDocument() {
    var canvas = document.getElementById('imageCanvas');
    var imageUrl = canvas.toDataURL("image/png");
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", imageUrl);
    downloadAnchorNode.setAttribute("download", "adeverinta_medicala.png");
    document.body.appendChild(downloadAnchorNode); 
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}

function showSubmitButton() {
    var form = document.getElementById('submitDrawing');
    form.style.display = 'block';
}

function enableDrawing() {
    var canvas = document.getElementById('imageCanvas');
    var ctx = canvas.getContext('2d');
    var drawing = false;
    var mousePos = { x:0, y:0 };
    showSubmitButton();
    canvas.onmousedown = function(e) {
        drawing = true;
        mousePos = getMousePos(canvas, e);
    };

    canvas.onmousemove = function(e) {
        if (!drawing) return;
        var newMousePos = getMousePos(canvas, e);
        ctx.beginPath();
        ctx.moveTo(mousePos.x, mousePos.y);
        ctx.lineTo(newMousePos.x, newMousePos.y);
        ctx.stroke();
        mousePos = newMousePos;
    };

    canvas.onmouseup = function(e) {
        drawing = false;
    };
}

function getMousePos(canvas, e) {
    var rect = canvas.getBoundingClientRect();
    var scaleX = canvas.width / rect.width;    // relationship bitmap vs. element for X
    var scaleY = canvas.height / rect.height;  // relationship bitmap vs. element for Y
    return {
        x: (e.clientX - rect.left) * scaleX,
        y: (e.clientY - rect.top) * scaleY
    };
}

window.onload = function() {
    var canvas = document.getElementById('imageCanvas'); // replace 'imageCanvas' with the actual id of your canvas
    var form = document.getElementById('myForm'); // replace 'myForm' with the actual id of your form
    var imageIdInput = document.getElementById('imageId');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // prevent the form from submitting normally

        var dataURL = canvas.toDataURL();
        var imageId = imageIdInput.value; // replace 'yourImageId' with the actual image id

        fetch('/medicalCertificate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'imageData=' + encodeURIComponent(dataURL) + '&imageId=' + encodeURIComponent(imageId)
        });
    });
};