$(document).ready(function() {
    $('#selectagent').select2();


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    $("#concern_submit_button").click(function(){ 

        var title = $("#id_title").val()
        var selectagent = $("#selectagent").val();
        var image = $("#image").val()
        var content = $("#id_content").val();

        var csrftoken = getCookie('csrftoken');
        
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });


        var context = {
            'title': title,
            'selectagent':selectagent,
            'content':content,
            'image':image        
        }
        

        $.ajax({
            type: "POST",
            url: '/account/submitConcern/',
            dataType: "json",
            data: JSON.stringify(context),
            success: function(response) {
                console.log(response)
                window.location.replace("/account/dashboard");
                
            }
        });
        
    });
});


(function() {
    document.getElementById("file_input").onchange = function() {
        var files = document.getElementById("file_input").files;
        var file = files[0];
        if (!file) {
            var file = document.getElementById('image');
            file.value = "";

            return alert("File has not been selected.");
        }
        getSignedRequest(file);
    };
})();

function getSignedRequest(file){
    var allowFileType = ["image/png", "image/tiff", "image/jpeg", "image/gif"];

    var re = allowFileType.indexOf(file.type);

    if (re === -1) {
        alert("Uploaded image type not supported! PNG format is preferred!");
    } else {

        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/account/signpicture_s3?file_name=" + file.name + "&file_type=" + file.type);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    uploadFile(file, response.data, response.url);

                } else {
                    alert("Testing mode or invalid security key!");
                }
            }
        }
        xhr.send();
    }
}

function uploadFile(file, s3Data, url) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", s3Data.url);

    var postData = new FormData();
    for (key in s3Data.fields) {
        postData.append(key, s3Data.fields[key]);
    }
    postData.append('file', file);

    xhr.send(postData);

    var file = document.getElementById('image');
    file.value = url.replace(" ", "+");
}