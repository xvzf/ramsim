var exampleCode =
`INPUT 0..1
OUTPUT 2
  0: a <- s[0]
  1: a <- a + s[1]
  2: s[2] <- a
  3: HALT`


// Rezizes 
var rezizeCodeInput = function() {
    document.getElementById("code").rows = document.getElementById("code").value.split("\n").length
}


// Adds a s[i] to the right area
var initialVarCount = 0

var addInitialVar = function() {
    document.getElementById("initial_vars").innerHTML = "<div><label>s[" + initialVarCount + "]</label>" +
                                                        "<input id=\"s" + initialVarCount + "\"></div>\n" +
                                                        document.getElementById("initial_vars").innerHTML;
    initialVarCount++;
}

var removeInitialVar = function() {
    if(initialVarCount > 0) {
        // Remove first line -> s[initialVarCount]
        document.getElementById("initial_vars").innerHTML = document.getElementById("initial_vars").innerHTML.replace(/[\w\W]+?\n+?/,"");
        initialVarCount--;
    }
}

// Posting
function post(path, params) {
    method = "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");


    form.setAttribute("method", method);
    form.setAttribute("action", path);

    // csrf token for wtf flask
    var token = document.getElementById("csrf_token").value;
    var csrfField = document.createElement("input")
    csrfField.setAttribute("type", "hidden");
    csrfField.setAttribute("name", "csrf_token");
    csrfField.setAttribute("value", token);
    form.appendChild(csrfField);


    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }


    document.body.appendChild(form);
    form.submit();
}


// Event listener to Rezize the code input
document.getElementById("code").addEventListener("input", function() {
    rezizeCodeInput();
});

// Event listener to add another variable
document.getElementById("addInitialVar").addEventListener("click", function() {
    addInitialVar();
});

// Event listener to remove a variable
document.getElementById("removeInitialVar").addEventListener("click", function() {
    removeInitialVar();
});

// Event listener for execution
document.getElementById("runcode").addEventListener("click", function() {

    var re = RegExp('^\\d+$');
    var valid = true;
    for(i = 0; i < initialVarCount; i++) {
        if(!re.test(document.getElementById("s" + i).value)) {
            // Invalid input, highlight
            document.getElementById("s" + i).style.borderColor = "#FF4C00";
            document.getElementById("s" + i).style.borderWidth = "4px";
            valid = false;
        }
    }


    // Only submit when valid
    if(valid) {
        // Disable Inputs
        ["addInitialVar", "removeInitialVar", "code", "runcode"].forEach(function(todisable) {
            document.getElementById(todisable).disabled = true;
        });

        inputs = document.getElementsByTagName("input");
        for(i = 0; i < inputs.length; i++) {
            inputs[i].disabled = true;
        }

        //document.getElementById("addInitialVar").disabled = true;
        document.getElementById("runcode").innerHTML = '<i class="fa fa-spinner fa-spin"></i>';

        var svars = ""
        // Collect all svars
        for(i = 0; i < (initialVarCount - 1); i++) {
            svars = svars + document.getElementById("s" + i).value + ";";
        }
        svars = svars + document.getElementById("s" + (initialVarCount - 1)).value;

        // Create post request
        post("/core/", {
            "code": document.getElementById("code").value,
            "svar": svars
        });
    }
});


// Load example code snipped when the page has loaded
document.addEventListener("load", new function() {

    // initialize code input
    document.getElementById("code").value = exampleCode;
    rezizeCodeInput();

    // initialize initial variables
    addInitialVar();
});