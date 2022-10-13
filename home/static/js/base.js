function hideSelf(element) {
    // Hide the given element, used in messages
    element.style.opacity = "0";
    setTimeout(() => {
        element.style.display = "none";
    }, 300);
}

// hide all messages after 15 seconds
setTimeout(() => {
    let messages = document.getElementsByClassName("message");
    for (let i = 0; i < messages.length; i++) {
        hideSelf(messages[i]);
    }
}, 15000);

// Add the correct padding to the bottom of the main content
// so that the content is not hidden behind the footer

function setMainPadding() {
    let footerHeight = document.getElementsByTagName("footer")[0].offsetHeight;
    let mainContent = document.getElementsByTagName("main")[0];
    let margin = footerHeight + 50;
    mainContent.style.marginBottom = margin + "px";
}

// Deferring the execution of the function until the page is loaded
window.onload = function () {
    setMainPadding();
};
