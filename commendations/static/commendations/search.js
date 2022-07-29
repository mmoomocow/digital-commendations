function filterStudents(searchTerm) {
    var students = document.getElementsByClassName("studentChoice");
    for (var i = 0; i < students.length; i++) {
        if (students[i].text.toLowerCase().indexOf(searchTerm.toLowerCase()) > -1) {
            students[i].style.display = "";
        } else {
            students[i].style.display = "none";
        }
    }
}