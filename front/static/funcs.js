
// /add.html
function enableProductSpecifics(element) {
    // hide and unrequire all specific product fields
    hideThem(document.querySelectorAll(".specifics"));
    unrequireThem(document.querySelectorAll(".specifics input, .specifics select"));

    if (element.value != "product") {
        // get the id of the one we wanna show
        var divId = element.value + "-details";
        console.log(divId);

        // set them to required
        requireThem(document.querySelectorAll("#" + divId + " input, #" + divId + " select"))

        // show the div
        document.getElementById(divId).style.display = 'block';
    }
}

function hideThem(elements) {
    elements.forEach(elm => {
        elm.style.display = 'none';
    });
}

function unrequireThem(elements) {
    elements.forEach(elm => {
        elm.removeAttribute("required")
    });
}

function requireThem(elements) {
    elements.forEach(elm => {
        elm.setAttribute("required", "")
    });
}