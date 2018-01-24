function create_post(pk) {
  console.log("create post is working!") // sanity check
  $.ajax({
    url: "wseventos/" + pk, // the endpoint
    type: "POST", // http method
    data: {
      Escuela: $('#id_Escuela').val(),
      Nombre: $('#id_Nombre').val(),
      Correo: $('#id_Correo').val()
    }, // data sent with the post request
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },

    // handle a successful response
    success: function(json) {
      $('#id_Correo').val('');
      $('#id_Nombre').val('');
      $('#id_Escuela').val('');// remove the value from the input
      console.log(json); // log the returned json to the console
      if (json.result == 'Registrado') {
        $("#talk").prepend('<li id="element_'+
                           json.pk +'" ><strong>' +
                           json.correo + '</strong> - <em> ' +
                           json.nombre + '</em> - <span> ' +
                           json.escuela + '</span>  - <span> <a onclick="del_asistente('+ 
                           json.pk +')" class="btn" href="javascript:history.go(0)"> X </a> </li>');

      } else {
        showalert("Usuario YA registrado","alert-warning")
      }
      console.log("success"); // another sanity check
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  })
}
function del_asistente(pk) {
  console.log("delete post is working!") // sanity check
  $.ajax({
    url: "delete/" + pk, // the endpoint
    type: "POST", // http method
    data: {
    }, // data sent with the post request
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    success:function(json){
        console.log(json);
    },
    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  })
}
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
function showalert(message,alerttype) {

    $('#alert_placeholder').append('<div id="alertdiv" class="alert ' +  alerttype +
                                   '"><a class="close" data-dismiss="alert"></a><span>'+message+'</span></div>')

    setTimeout(function() { // this will automatically close the alert and remove this if the users doesnt close it in 5 secs


      $("#alertdiv").remove();

    }, 3000);
  }
function show_asistentes(pk) {
    console.log("create post is working!") // sanity check
  $.ajax({
    url: "wsasistentes/" + pk, // the endpoint
    type: "GET", // http method
      success: function(json) {
          console.log(json);
          for (i = 0; i < json.length-1; i++) {
              console.log(json[i]);
               $("#talk").prepend('<li id="element_'+ 
                                  json[i].pk +'"><strong>' +
                                  json[i].fields.Correo + '</strong> - <em> ' +
                                  json[i].fields.Nombre + '</em> - <span> ' + 
                                  json[i].fields.Escuela + '</span> - <span> <a onclick="del_asistente('+ json[i].pk +
                                  ')" class="btn" href="javascript:history.go(0)"> X </a></span></li>');
          }
          
      }, 
  })}
 