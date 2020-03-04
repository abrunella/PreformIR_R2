// Call the dataTables jQuery plugin
$(document).ready(function() {

    $('#datatable-event-log').DataTable();
    $('#datatable-temperature-log').DataTable();
    $('#datatable-sensor-log').DataTable();
});

$(document).ready(function() {
    $('#dataTableActivity').DataTable({
        "order": [[ 0, 'desc' ]]
    });

    $('#datatable-alarm-history').DataTable({
        "order": [[ 0, 'desc' ]]
    });
});
