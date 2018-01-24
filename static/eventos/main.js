function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
function ws_like(pk) {
  console.log("Like!") // sanity check
  $.ajax({
    url: "/wsevento/like/" + pk, // the endpoint
    type: "POST", // http method
    data: {
    }, // data sent with the post request
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    success:function(json){
        console.log(json);
        if (json.result == 'Like'){
            showalert("Has dado like","alert-warning");
        }
        else{
            showalert("DisLike:(","alert-warning");

        }
    },
    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  })
}

function showalert(message,alerttype) {

    $('#like_placeholder').append('<div id="alertdiv" class="alert ' +  alerttype +
                                   '"><a class="close" data-dismiss="alert"></a><span>'+message+'</span></div>')

    setTimeout(function() { // this will automatically close the alert and remove this if the users doesnt close it in 5 secs


      $("#alertdiv").remove();

    }, 3000);
  }