function fileElement() {
	// Find label
	// var labels = document.getElementsByTagName('LABEL');
	// for (var i = 0; i < labels.length; i++) {
	// 	if (labels[i].htmlFor == "id_agentverifile") {
	// 		var the_label = labels[i];
	// 		the_label.style.display = 'none';
	// 		break;
	// 	}
	// }

	// var text = document.getElementById("id_agentverifile");
	// text.style.display = 'none';


	var text = document.getElementById("id_agentverifile");
	text.disabled = true;
}

function register_submit() {
	var reg_form = document.getElementById("register_form");
// function submit_register_form(reg_form) {
	var token = document.getElementsByName("csrfmiddlewaretoken");
	var file_url = document.getElementById('id_agentverifile').value;
	alert(file_url);


	var files = document.getElementById("file_input").files;
	var file = files[0];
	if (!file) {
		return alert("Please upload your verification file!");
	}	

	alert(reg_form['agentverifile']);
	console.log(reg_form['agentverifile']);

	reg_form.submit();
}



(function() {
	document.getElementById("file_input").onchange = function() {
		var files = document.getElementById("file_input").files;
		var file = files[0];
		if (!file) {
			return alert("File has not been selected.");
		}
		getSignedRequest(file);
	};
})();

function getSignedRequest(file){
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "/account/sign_s3?file_name=" + file.name + "&file_type=" + file.type);
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
	file.disabled = false;
}