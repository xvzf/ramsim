// Rezizes 
var rezizeCodeInput = function() {
    document.getElementById("code").rows = document.getElementById("code").value.split("\n").length
}

// Load example code snipped when the page has loaded
document.addEventListener("load", new function() {
    rezizeCodeInput();
});