// Today - used for max date in date picker
var today = new Date();
// 3 weeks ago - used for default date in date picker
var threeWeeksAgo = new Date(today.getTime() - (3 * 7 * 24 * 60 * 60 * 1000));
// 3 months ago - used for min date in date picker
var threeMonthsAgo = new Date(today.getTime() - (3 * 30 * 24 * 60 * 60 * 1000));

// Set the datepicker to the 3 weeks ago date and disable the future dates
var datepicker = document.getElementById('date');
datepicker.value = threeWeeksAgo.toISOString().split('T')[0];
datepicker.setAttribute('min', threeMonthsAgo.toISOString().split('T')[0]);
datepicker.setAttribute('max', today.toISOString().split('T')[0]);

// get query string parameters
const queryParams = new URLSearchParams(window.location.search);

// Get the date query string parameter and set the datepicker to that date if it exists
var date = queryParams.get('date');
if (date) {
    datepicker.value = date;
}

// Use the query to have persistent form data
types = queryParams.getAll('type');
if (types.length > 0) {
    for (var i = 0; i < types.length; i++) {
        var type = types[i];
        var checkbox = document.getElementById(type);
        checkbox.checked = true;
    }
}

// Add select all checkbox functionality
function selectAllCheckboxes() {
    var checkboxes = document.getElementsByName('milestone');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = document.getElementsByName("selectAll")[0].checked;
    }
}

// If any table row is clicked, tick the checkbox
// and if the checkbox is clicked still tick the checkbox
rows = document.getElementsByClassName('clickable-row');
for (var i = 0; i < rows.length; i++) {
    rows[i].getElementsByTagName('input')[0].onclick = function () {
        this.checked = !this.checked;
    };
    rows[i].onclick = function () {
        var checkbox = this.getElementsByTagName('input')[0];
        checkbox.checked = !checkbox.checked;
    };
}