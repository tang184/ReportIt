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