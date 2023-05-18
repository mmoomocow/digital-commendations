function hideSelf(element) {
    // Hide the given element, used in messages
    element.style.opacity = "0";
    setTimeout(() => {
        element.style.display = "none";
    }, 300);
}

function toggleNavResponsive() {
    // Toggle the responsive navigation bar
    // Get nav tag
    let nav = document.getElementsByTagName("nav")[0];
    if (nav.className === "responsive") {
        nav.className = "";
    } else {
        nav.className = "responsive";
    }
}

// hide all messages after 15 seconds
setTimeout(() => {
    let messages = document.getElementsByClassName("message");
    for (let i = 0; i < messages.length; i++) {
        hideSelf(messages[i]);
    }
}, 15000);