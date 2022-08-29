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