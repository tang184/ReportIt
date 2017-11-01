function fileElement() {
	var text = document.getElementById("id_agentverifile");
	text.disabled = true;
}

function register_submit() {
	var reg_form = document.getElementById("register_form");
	var token = document.getElementsByName("csrfmiddlewaretoken");
	var file_url = document.getElementById('id_agentverifile').value;

	var files = document.getElementById("file_input").files;
	var file = files[0];
	if (!file) {
		return alert("Please upload your verification file!");
	}

	document.getElementById('id_agentverifile').disabled = false;
	reg_form.submit();
}



(function() {
	document.getElementById("file_input").onchange = function() {
		var files = document.getElementById("file_input").files;
		var file = files[0];
		if (!file) {
			var file = document.getElementById('id_agentverifile');
			file.value = "";

			return alert("File has not been selected.");
		}
		getSignedRequest(file);
	};
})();

function getSignedRequest(file){
	var allowFileType = ["image/png", "image/tiff", "image/jpeg", "image/gif", "application/pdf"];

	var re = allowFileType.indexOf(file.type);

	if (re === -1) {
		alert("Uploaded image type not supported! PNG format is preferred!");
	} else {

		var xhr = new XMLHttpRequest();
		xhr.open("GET", "/account/signup_s3?file_name=" + file.name + "&file_type=" + file.type);
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

	var file = document.getElementById('id_agentverifile');
	file.value = url.replace(" ", "+");
}