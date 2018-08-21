// Automatic Slideshow - change image every 4 seconds
var myIndex = 0;
function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";
    }
    myIndex++;
    if (myIndex > x.length) {myIndex = 1}
    x[myIndex-1].style.display = "block";
    setTimeout(carousel, 4000);
}

// Used to toggle the menu on small screens when clicking on the menu button
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

// When the user clicks anywhere outside of the modal, close it
var modal = document.getElementById('EmailModal');
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function display_model(record_id, amount, date){
    document.getElementById("record_id").value = record_id;
    document.getElementById('EmailModal').style.display='block';
    document.getElementById("amount_val").innerHTML = amount;
    document.getElementById("boli_date").innerHTML = date;
    document.getElementById("phone_number").value = document.getElementById("pNumber").value;
}

function close_update(){
    document.getElementById('EmailModal').style.display='none';
    var checkboxes = document.getElementsByTagName('input');
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].type == 'checkbox') {
            checkboxes[i].checked = false;
        }
    }
};

function payment_md(){
    var mode = document.getElementById("id_payment_mode").value;
    if (mode === 'Cash'){
        document.getElementById('id_id_details').style.display='none';
        document.getElementById("id_id_details").required = false;
    } else {
        document.getElementById('id_id_details').style.display='block';
        document.getElementById("id_id_details").required = true;
    }
}


var pNumber = document.getElementById("pNumber");
pNumber.addEventListener("keyup", function(event) {
  event.preventDefault();
  if (event.keyCode === 13) {
    var url = '/search/?phone_number='+pNumber.value+'#record'
    window.open(url, "_self");
  }
});


var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};


/* Function will fetch description based phone number */
function get_description() {
    var phone_number = $("#id_phone_number").val();
    var data = {
        phone_number: phone_number
    };

    if (phone_number.length >= 10){
        $('#id_description').focus();
        $.get('/get/description/', data, function(data){
               $('#id_description').val(data.description);
        }, 'json');
    }
}