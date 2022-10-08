// Call the dataTables jQuery plugin
$(document).ready(function () {
  $('#dataTable').DataTable({

    buttons: [
      'excelHtml5',
      'pdfHtml5'
    ]
  });
});
