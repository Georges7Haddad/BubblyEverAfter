function show(y) {
    var x = document.getElementById("myInput".concat(y));
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}