// On load, start a countdown timer to redirect to the award commendation page
// If the user clicks the cancel button, stop the timer and stay on the page
// Also keep track of the time remaining and display it to the user

// Set the time to redirect in milliseconds
var timeToRedirect = 7000;

// Redirect to the award commendation page
function redirect() {
    window.location.href = "/commendations/award/";
}

document.addEventListener("DOMContentLoaded", function () {
    // Start the timer
    var timer = setTimeout(redirect, timeToRedirect);

    // Display the time remaining to the user rounded to 1 decimal place
    var timeRemaining = document.getElementById("timeRemaining");
    timeRemaining.innerHTML = (timeToRedirect / 1000).toFixed(1);

    // Update the time remaining every 100 milliseconds
    var updateInterval = setInterval(function () {
        timeRemaining.innerHTML = (timeRemaining.innerHTML - 0.1).toFixed(1);
    }, 100);

    // If the user clicks the cancel button, stop the timer
    var cancelButton = document.getElementById("cancelButton");
    var redirectH2 = document.getElementById("redirectH2");
    var redirectP = document.getElementById("redirectP");

    cancelButton.addEventListener("click", function () {
        clearTimeout(timer);
        clearInterval(updateInterval);
        redirectH2.innerHTML = "Redirect cancelled";
        redirectP.innerHTML = "You will not be redirected to the award commendation page. You can still access the page by using the navigation bar at the top of the page.";
    });
});