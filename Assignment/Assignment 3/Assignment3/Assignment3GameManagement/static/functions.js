//AJAX for validating the user name in real time

function UsernameValidation(str) {
    if (str.length === 0) {
        document.getElementById("errormessageusername").innerHTML = "Please fill in the username.";
        return;
    }
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById("errormessageusername").innerHTML = this.responseText;
        }
    };
    xmlhttp.open("GET", "/check_username?q="+str, true);
    xmlhttp.send();
}
//AJAX for validating the email in real time
function EmailValidation(str) {
    if (str.length === 0) {
        document.getElementById("errormessageemail").innerHTML = "Please fill in the email.";
        return;
    }
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            document.getElementById("errormessageemail").innerHTML = this.responseText;
        }
    };
    xmlhttp.open("GET", "/check_email?q=" + str, true);
    xmlhttp.send();
}
//I didn't use AJAX to validate the password
function validate_register_form(){
    var form = document.getElementById("registrationForm");
    var password = form.elements["password"].value;
    var errormsg = document.getElementById("errormessage");
    // Clear the previous error message
    errormsg.innerHTML = "";

    // Check for empty fields
    for (var i = 0; i < form.elements.length - 1; i++) {
        if (form.elements[i].value.trim() === "") {
            errormsg.innerHTML = "Please fill all the fields.";
            return false;
        }
    }

    // Check for lowercase character
    if (!/[a-z]/.test(password)) {
        errormsg.innerHTML = "The password should contain at least one lowercase letter.";
        return false;
    }

    // Check for uppercase character
    if (!/[A-Z]/.test(password)) {
        errormsg.innerHTML = "The password should contain at least one uppercase letter.";
        return false;
    }

    // Check for at least one digit
    if (!/\d/.test(password)) {
        errormsg.innerHTML = "The password should contain at least one digit.";
        return false;
    }

    // Check password length
    if (password.length < 10) {
        errormsg.innerHTML = "The password length should be at least 10.";
        return false;
    }

    // If all checks pass, the form can be submitted
    return true;
}
//this function will be responsible for checking the input data from the user in the login form, and providing the appropriate message.
function loginvalidation(){
     var form = document.getElementById("loginform");
     var errormsessage=document.getElementById("errorloginmessage");
     if(form.elements["username"].value ===""){
         errormsessage.innerHTML="username field can not be empty";//just for debugging purposes.
     }
     if(form.elements["password"].value===""){
         errormsessage.innerHTML="password field can not be empty";//just for debugging purposes.
     }
     else if(form.elements["password"].value.length<10){
         errormsessage.innerHTML="password lenght should be at least 10";
     }


}
function Validateupdatedpassword(){

}