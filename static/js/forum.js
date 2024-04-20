document.getElementById('searchBar').addEventListener('input', function(e) {
    var searchKeyword = e.target.value.toLowerCase();
    var posts = document.querySelectorAll('.panel-activity__list li');

    posts.forEach(function(post) {
        var title = post.querySelector('.activity__list__header a').textContent.toLowerCase();
        var text = post.querySelector('.activity__list__body p').textContent.toLowerCase();

        if (title.includes(searchKeyword) || text.includes(searchKeyword)) {
            post.style.display = '';
        } else {
            post.style.display = 'none';
        }
    });
});

function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.getElementById('preview');
        output.src = reader.result;
        output.style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);}

// functia pentru a vedea comentariile
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    document.addEventListener('click', function(e) {
        console.log('Element clicked');

        var target = e.target;
        while (target && !target.classList.contains('comments-button')) {
            target = target.parentElement;
        }

        if(target) {
            console.log('Comments button clicked');

            // Prevent the default action
            e.preventDefault();

            // Find the related comment area
            var commentArea = target.closest('li').querySelector('.add-comment-section');
            console.log('Comment area:', commentArea);

            // Show the comment area
            if (commentArea) {
                commentArea.style.display = 'flex';
            }
        }
    });

    var textareas = document.querySelectorAll('textarea');

    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
});
 

document.addEventListener('DOMContentLoaded', function() {
    var textareas = document.querySelectorAll('textarea');

    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
});


// document.getElementById('addPost').addEventListener('submit', function(e) {
//     e.preventDefault();

//     var preview = document.getElementById('preview');
//     var canvas = document.createElement('canvas');
//     var context = canvas.getContext('2d');

//     canvas.width = preview.width;
//     canvas.height = preview.height;
//     context.drawImage(preview, 0, 0, preview.width, preview.height);

//     var imageDataUrl = canvas.toDataURL('image/jpeg');

//     var formData = new FormData(this);
//     formData.append('imageDataUrl', imageDataUrl);

//     fetch('/Users/alinaatanasiu/PycharmProjects/LicentaP1/server.py', {
//         method: 'POST',
//         body: formData
//     }).then(function(response) {
//         // Handle the response from the server
//     });
// });