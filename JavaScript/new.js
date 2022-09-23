function change(){
    document.querySelector("img").src = "2.jpg";
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("button").onclick = change;
});