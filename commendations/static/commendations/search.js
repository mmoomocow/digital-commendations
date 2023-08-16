function filterStudents(searchTerm) {
    var selectableStudents = document.getElementById('selectable-students').getElementsByTagName("li");
    var selectedStudents = document.getElementById('selected-students').getElementsByTagName("li");

    if (searchTerm == "") {
        for (var i = 0; i < selectableStudents.length; i++) {
            selectableStudents[i].style.display = "";
        }

        for (var i = 0; i < selectedStudents.length; i++) {
            selectedStudents[i].style.display = "";
        }

        return;
    }


    searchTerm = searchTerm.toLowerCase();

    for (var i = 0; i < selectableStudents.length; i++) {
        var studentName = selectableStudents[i].innerHTML.toLowerCase();
        if (studentName.indexOf(searchTerm) > -1) {
            selectableStudents[i].style.display = "";
        } else {
            selectableStudents[i].style.display = "none";
        }
    }

    for (var i = 0; i < selectedStudents.length; i++) {
        var studentName = selectedStudents[i].innerHTML.toLowerCase();
        if (studentName.indexOf(searchTerm) > -1) {
            selectedStudents[i].style.display = "";
        } else {
            selectedStudents[i].style.display = "none";
        }
    }
}