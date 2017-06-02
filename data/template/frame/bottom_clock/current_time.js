function updateCurrentTime() {
    var d = new Date();
    document.getElementById("current_time").innerHTML = d.toLocaleTimeString();
}

setInterval(updateCurrentTime, 1000);