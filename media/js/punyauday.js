// Automatic Slideshow - change image every 4 seconds
var myIndex = 0;
var running_total = 0;
var paid_ids = [];

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
var confirm_modal = document.getElementById('customConfirmation');
window.onclick = function(event) {
  if (event.target == modal) {
    close_update();
  }
  if (event.target == confirm_modal){
    closeConfirmationModel();
  }
}

function display_model(record_id, amount, date, partial, pan_card){
    document.getElementById("record_id").value = record_id;
    document.getElementById('EmailModal').style.display='block';

    if (partial=="PP"){
        document.getElementById("Original_amount").style.display='block';
        document.getElementById("id_partial_payment").style.display='block';
        document.getElementById("id_partial_payment").required = true;
        document.getElementById("amount_val").innerHTML = "0.00";
    } else {
        document.getElementById("id_partial_payment").style.display='none';
        document.getElementById("Original_amount").style.display='none';
        document.getElementById("id_partial_payment").required = false;
        document.getElementById("amount_val").innerHTML = amount + '.00';
    }
    document.getElementById("org_amount_val").innerHTML = amount + '.00';
    document.getElementById("boli_date").innerHTML = date;
    document.getElementById("phone_number").value = document.getElementById("pNumber").value;

    if (pan_card !== "None"){
        document.getElementById("id_pan_card").value = pan_card;
        document.getElementById("id_pan_card").readOnly = true;
    }
}

function close_update(){
    document.getElementById('EmailModal').style.display='none';
    var checkboxes = document.getElementsByTagName('input');
    paid_ids = [];
    running_total = 0;
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].type == 'checkbox') {
            checkboxes[i].checked = false;
        }
    document.getElementById('chk_total').textContent = running_total;
    document.getElementById("chb_amt").disabled = true;
    }
};

function payment_cal(){
    var paid_amount = parseInt(document.getElementById("id_partial_payment").value);
    var original_amount = parseInt(document.getElementById("org_amount_val").innerText);
    if (original_amount < paid_amount){
        document.getElementById("amount_val").innerHTML = "Amount greater than Original amount not allowed!";
        document.getElementById("amount_val").style.color = "red";
        document.getElementById("id_partial_payment").value = ''
    } else {
        document.getElementById("amount_val").style.color = "black";
        document.getElementById("amount_val").innerHTML = paid_amount + '.00';
    }
}

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

function Openwhatsapp(phone_number) {
   var url = "https://api.whatsapp.com/send?phone=" + phone_number
    window.open(url,"","toolbar=no,status=no,menubar=no,location=center,scrollbars=no,resizable=no,height=500,width=657");
}

function update(mandir) {
    document.getElementById("chb_amt").disabled = false;
    // Check
    if(mandir.checked == true){
        // Add value to running_total
        running_total += parseInt(mandir.value);
        document.getElementById('chk_total').textContent = running_total;
        paid_ids.push(mandir.id);
        document.getElementById('smtArrId').value = paid_ids;
    }
    // Uncheck
    if(mandir.checked == false){
        // Subtract value from running_total
        running_total -= parseInt(mandir.value);
        document.getElementById('chk_total').textContent = running_total;
        paid_ids.removeByValue(mandir.id)
        document.getElementById('smtArrId').value = paid_ids;
        if (running_total == 0){
            document.getElementById("chb_amt").disabled = true;
        }
    }
}

function openGooglePay(amount) {
    if (amount != "0"){
        const googlePayDeepLink = "upi://pay?pa=8799928255@mahb&pn=susdigamberjainmadir&am="+amount+"&cu=INR";
        window.open(googlePayDeepLink, '_blank');
    } else {
        alert("Please select at least one record.")
    }
}

function confirmationUserAction(amount){
    document.getElementById("confirm_val").innerHTML = amount + '.00';
    document.getElementById('customConfirmation').style.display='block';
}

function openModelBox(record_id, amount, date, partial, pan_card) {
        document.getElementById('customConfirmation').style.display='None';
        display_model(record_id, amount, date, partial, pan_card)
}

function closeConfirmationModel(){
    document.getElementById('customConfirmation').style.display='none';
    document.getElementById("paid_chk").checked = false;
};