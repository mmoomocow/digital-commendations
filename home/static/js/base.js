function hideSelf(element) {
    // Hide the given element, used in messages
    element.style.opacity = "0";
    setTimeout(() => {
        element.style.display = "none";
    }, 300);
}