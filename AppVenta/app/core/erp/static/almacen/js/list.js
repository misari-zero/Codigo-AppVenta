// var tblSale;
//
// function format(d) {
//     console.log(d);
//     var html = '<table class="table">';
//     html += '<thead class="thead-dark">';
//     html += '<tr><th scope="col">Producto</th>';
//     html += '<th scope="col">Categoría</th>';
//     html += '<th scope="col">PVP</th>';
//     html += '<th scope="col">PVPCompra/th>';
//     html += '<th scope="col">Cantidad</th>';
//     html += '<th scope="col">Total</th></tr>';
//     html += '</thead>';
//     html += '<tbody>';
//     $.each(d.det, function (key, value) {
//         html+='<tr>'
//         html+='<td>'+value.prod.name+'</td>'
//         html+='<td>'+value.prod.cat.name+'</td>'
//         html+='<td>'+value.price+'</td>'
//         html+='<td>'+value.pricecom+'</td>'
//         html+='<td>'+value.cant+'</td>'
//         html+='<td>'+value.total+'</td>'
//         html+='</tr>';
//     });
//     html += '</tbody>';
//     return html;
// }
//
// $(function () {
//
//     tblSale = $('#data').DataTable({
//         //responsive: true,
//         scrollX: true,
//         autoWidth: false,
//         destroy: true,
//         deferRender: true,
//         ajax: {
//             url: window.location.pathname,
//             type: 'POST',
//             data: {
//                 'action': 'searchdata'
//             },
//             dataSrc: ""
//         },
//         columns: [
//             {
//                 "className": 'details-control',
//                 "orderable": false,
//                 "data": null,
//                 "defaultContent": ''
//             },
//             {"data": "sucursal.name"},
//             {"data": "transf.name"},
//             {"data": "doc.name"},
//             {"data": "nro"},
//             {"data": "date_joined"},
//             {"data": "price"},
//             {"data": "subtotal"},
//             {"data": "iva"},
//             {"data": "total"},
//             {"data": "id"},
//         ],
//         columnDefs: [
//             {
//                 targets: [-2, -3, -4, -5],
//                 class: 'text-center',
//                 orderable: false,
//                 render: function (data, type, row) {
//                     return 'S/.' + parseFloat(data).toFixed(2);
//                 }
//             },
//             {
//                 targets: [-1],
//                 class: 'text-center',
//                 orderable: false,
//                 render: function (data, type, row) {
//                     var buttons = '<a href="/erp/almacen/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
//                     buttons += '<a href="/erp/almacen/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
//                     buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
//                     buttons += '<a href="/erp/almacen/invoice/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
//                     return buttons;
//                 }
//             },
//         ],
//         initComplete: function (settings, json) {
//
//         }
//     });
//
//     $('#data tbody')
//         .on('click', 'a[rel="details"]', function () {
//             var tr = tblSale.cell($(this).closest('td, li')).index();
//             var data = tblSale.row(tr.row).data();
//             console.log(data);
//
//             $('#tblDet').DataTable({
//                 responsive: true,
//                 autoWidth: false,
//                 destroy: true,
//                 deferRender: true,
//                 //data: data.det,
//                 ajax: {
//                     url: window.location.pathname,
//                     type: 'POST',
//                     data: {
//                         'action': 'search_details_prod',
//                         'id': data.id
//                     },
//                     dataSrc: ""
//                 },
//                 columns: [
//                     {"data": "prod.name"},
//                     {"data": "prod.cat.name"},
//                     {"data": "price"},
//                     {"data": "pricecom"},
//                     {"data": "cant"},
//                     {"data": "total"},
//                 ],
//                 columnDefs: [
//                     {
//                         targets: [-1, -3, -4],
//                         class: 'text-center',
//                         render: function (data, type, row) {
//                             return 'S/.' + parseFloat(data).toFixed(2);
//                         }
//                     },
//                     {
//                         targets: [-2],
//                         class: 'text-center',
//                         render: function (data, type, row) {
//                             return data;
//                         }
//                     },
//                 ],
//                 initComplete: function (settings, json) {
//
//                 }
//             });
//
//             $('#myModelDet').modal('show');
//         })
//         .on('click', 'td.details-control', function () {
//             var tr = $(this).closest('tr');
//             var row = tblSale.row(tr);
//             if (row.child.isShown()) {
//                 row.child.hide();
//                 tr.removeClass('shown');
//             } else {
//                 row.child(format(row.data())).show();
//                 tr.addClass('shown');
//             }
//         });
//
// });