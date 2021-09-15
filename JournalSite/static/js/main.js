function foo() {
    var x = document.getElementById("sign_link");
    if (x.innerHTML == "Sign-In") {
        x.innerHTML = "Sign-Out";
    } else {
        x.innerHTML = "Sign-In";
    }
}