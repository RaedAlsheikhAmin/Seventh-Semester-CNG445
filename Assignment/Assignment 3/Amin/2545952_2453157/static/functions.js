function validate_advertisement_form() {
        var msg = "";
        var check = false;
        var form = document.getElementsByName("advertisement_form")[0];


        // Check for empty fields
        if (form.title.value === "") {
            msg += "Please write a title!\n";
            check = true;
        }
        if (form.description.value === "") {
            msg += "Please write a description!";
            check = true;
        }

        if (check) {
            document.getElementById("error_message").innerText = msg;
            return false;
        }

        return true;
    }

 function applyFilters() {
    var selectedCategoryId = document.getElementsByName("category")[0].value;
    var selectedCategoryName = document.getElementsByName("category")[0].selectedOptions[0].text;
    var searchText = document.getElementsByName("search")[0].value;
    var rows = document.getElementById("advertisement_table").rows;
    var check = false;
    document.getElementById("Category_name").innerText = selectedCategoryName;

    for (var i = 1; i < rows.length; i++) {
        var row = rows[i];
        var cid = row.dataset.cid;
        var title = row.cells[0].innerText;
        var description = row.cells[1].innerText;
        var fullname = row.cells[2].innerText;

        var categoryMatch = (selectedCategoryId === cid || selectedCategoryId === "0");
        var searchMatch = (title.includes(searchText) || description.includes(searchText) || fullname.includes(searchText));

        if (categoryMatch && searchMatch) {
            row.style.display = "";
            check = true;
        } else {
            row.style.display = "none";
        }
    }
    if (check == false)
    {
        rows[0].style.display="none";
        document.getElementById("No_advertisement").innerText="No advertisement!";
    }
    else
    {
        rows[0].style.display="";
        document.getElementById("No_advertisement").innerText="";
    }
}


function validate_register_form()
    {
        var form = document.getElementsByName("register_form")[0]
        var password = form.elements["password"].value;
        var error_message = document.getElementById("error_message")


        // Check for empty fields
        for (var i = 0; i < form.elements.length - 1; i++) {
            if (form.elements[i].value === "") {
                error_message.innerText = "Please fill in every column!";
                return false;
            }
        }


        // Check for lowercase character
        if (!/[a-z]/.test(password)) {
            error_message.innerText = "The password must contain at least one lowercase character!";
            return false;
        }

        // Check for uppercase character
        if (!/[A-Z]/.test(password)) {
            error_message.innerText = "The password must contain at least one uppercase character!";
            return false;
        }

        // Check password length
        if (password.length < 10) {
            if (form.elements[0].value === "") {
                check=true
            } "The password must be at least 10 characters long!";
            return false;
        }

        // Check for special symbols
        if (!/[+!*\-]/.test(password)) {
            error_message.innerText = "The password must contain one of the following symbols: +, -, !, *";
            return false;
        }

        // If all checks pass, you can submit the form
        return true;
    }

function validate_login_form() {
    var msg = "";
    var check = false;
    var form = document.getElementsByName("login_form")[0];

    console.log("Function called!");

    // Check for empty fields
    if (form.username.value === "") {
        msg += "Please write your username!\n";
        check = true;
    }
    if (form.password.value === "") {
        msg += "Please write your password!";
        check = true;
    }

    if (check) {
        document.getElementById("error_message").innerText = msg;
        return false;
    }

    // If all checks pass, you can submit the form
    console.log("Form submitted!");
    return true;
}

function validate_profile_form()
    {
        var form = document.getElementsByName("register_form")[0]
        var password = form.elements["password"].value;
        var error_message = document.getElementById("error_message")


        // Check for empty fields
        for (var i = 0; i < form.elements.length - 1; i++) {
            if (form.elements[i].value === "") {
                error_message.innerText = "Please fill in every column!";
                return false;
            }
        }


        // Check for lowercase character
        if (!/[a-z]/.test(password)) {
            error_message.innerText = "The password must contain at least one lowercase character!";
            return false;
        }

        // Check for uppercase character
        if (!/[A-Z]/.test(password)) {
            error_message.innerText = "The password must contain at least one uppercase character!";
            return false;
        }

        // Check password length
        if (password.length < 10) {
            if (form.elements[0].value === "") {
                check=true
            } "The password must be at least 10 characters long!";
            return false;
        }

        // Check for special symbols
        if (!/[+!*\-]/.test(password)) {
            error_message.innerText = "The password must contain one of the following symbols: +, -, !, *";
            return false;
        }

        // If all checks pass, you can submit the form
        return true;
    }