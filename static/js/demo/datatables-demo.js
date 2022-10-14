$(document).ready(function () {
  //Initialise the table
  var table = $('#dataTable').DataTable({
    order: [[0, 'desc']],
    dom: 'Bfrtip',
    lengthMenu: [
      10, 25, 50, -1
    ],
    buttons: [
      'pageLength', 'copy',
      {
        extend: 'excel',
        messageBottom: "Kings Educational Center Information Management System",
        title: "Report"
      },
      {
        extend: 'pdf',
        messageBottom: "Kings Educational Center Information Management System",
        title: "Report"
      },
    ],
    columnDefs: [{
      orderable: false,
      className: 'select-checkbox',
      targets: 0
    }],
    select: {
      style: 'multi',
      selector: 'td:first-child'
    },
    order: [[0, 'asc']]
  });

  //Add Styling to the buttons
  table.buttons().container().appendTo('#example_wrapper .col-md-6:eq(0)')

});