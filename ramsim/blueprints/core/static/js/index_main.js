var exampleCode =
`INPUT 0..1
OUTPUT 2
  0: a <- s[0]
  1: a <- a + s[1]
  2: s[2] <- a
  4: HALT`


// Rezizes 
var rezizeCodeInput = function() {
    document.getElementById("code").rows = document.getElementById("code").value.split("\n").length
}


// Adds a s[i] to the right area
var initialVarCount = 0

var addInitialVar = function() {
    document.getElementById("initial_vars").innerHTML = "<div><label>s[" + initialVarCount + "]</label>" +
                                                        "<input name=\"" + initialVarCount + "\"></div>\n" +
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
    for(b in document.getElementsByClassName("btn")) {
        // @TODO
    }
    document.getElementById("runcode").innerHTML = '<i class="fa fa-spinner fa-spin"></i>'

    // @TODO
});


// Load example code snipped when the page has loaded
document.addEventListener("load", new function() {

    // initialize code input
    document.getElementById("code").value = exampleCode;
    rezizeCodeInput()

    // initialize initial variables
    addInitialVar()
});
