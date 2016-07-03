
$(document).ready(function() {
  $('select').material_select();
  $('#export_all').click(function () {
    var doc = new jsPDF('', '', 'a4');
    var specialElementHandlers = {
      '#editor': function(element, renderer){
        return true;
      }
    };
    var chartHeight = 100;
    doc.setFontSize(40);
    doc.text(15, 10, "Relatório de modulo gerencial");
    doc.fromHTML($('#table_content').get(0), 35, 35, {
      'width': 300,
      'height': 100, 
      'elementHandlers': specialElementHandlers
    });
    doc.addPage();

    if ($(".myChart")[0]){

      $('.myChart').each(function (index) {
        var imageData = $(this).highcharts().createCanvas();
        doc.addImage(imageData, 'JPEG', 1, (index * chartHeight) + 50, 200, chartHeight);
      });
    } else {
      doc.fromHTML($('#container_prod').get(0), 15, 15, {
      'width': 170,
      //'height': 100,
      'text-align': 'center',
      'elementHandlers': specialElementHandlers
    });
    }
      var data_name = new Date();
      var name_file = "report_estoque" + data_name.getDate() + "_" + (parseInt(data_name.getMonth()) + parseInt(1)) + data_name.getFullYear() + ".pdf";

    doc.save(name_file);
  })
  $("#print_all").click(function (){
    window.print();
  })

  var time_enabled = 40;
  for (var x=1; x<= time_enabled; x++){
    if (x == time_enabled){
      $("#print_all").removeAttr('disabled');
      $("#export_all").removeAttr('disabled');
    }
  }

});
$("#form_company input[name='enabled_photo']").click(function () {
  var element = document.getElementById('file_input_company');
  if (element.style.display == 'none'){
    element.style.display='';
  } else {
    element.style.display='none';
  }
});
$("#form_branch input[name='enabled_photo']").click(function () {
  var element = document.getElementById('file_input_branch');
  if (element.style.display == 'none'){
    element.style.display='';
  } else {
    element.style.display='none';
  }
});
  function IncrementValue(input_id){
    var id = "#" + input_id;
    var product_id = input_id.split("_")[2];
    jqxhr = $.ajax("/stock/disponible/" + product_id, {
        data: $(this).serialize(),
        type: 'GET',
        dataType: 'json',
    });
    jqxhr.done(function(data) {
        if (data.status == 'ok') {
            var requisited_value = (parseInt($(id).val()) + 1);
            if (requisited_value > parseInt(data.total_disponible)){
              $(id).val(parseInt(data.total_disponible))
              Materialize.toast("Ops... Quantidade excede o disponível em estoque :'(", 4000);
            } else {
              $(id).val(parseInt($(id).val()) + 1);
            }
        } else {
            Materialize.toast("Erro ao consultar a estoque: " + data.message, 40000);
        }

    });    
    return false
    };

  function DecrementValue(input_id){
    var id = "#" + input_id;
    if (parseInt($(id).val()) == 0){
      Materialize.toast('Valor não pode ser menor que 0', 4000)
    } else {
      $(id).val(parseInt($(id).val()) - 1);
    }
  }
function func_show_item(item){
  found = item.search(item);
  var url = '/'+ item + '/create/';
  if (found != -1){
    var item = item.replace(new RegExp("/", "g"), '_');
  }
  var id = '#' + item;
  var element_father = document.getElementById("div_forms_configurations");
  var t = document.createElement('div');
  t.id = item;
  element_father.appendChild(t);
  $.get(url, function(data){
    $(id).html(data);
    document.getElementById(item).style.display='';
  })
    func_clear_specific_item(item);
  }

  var array_delete = [];
  function AddOrDeleteItem(element){
    if (element.checked){
        array_delete.push(element.id)
    } else {
      for (var i=0; i < array_delete.length; i++){
        if (array_delete[i] == element.id){
          delete array_delete[i]
        }
      }
    }
  }
  function PostRemove(){
    var array_itens = [];
    for (var j=0; j < array_delete.length; j++){
      if (array_delete[j]){
        array_itens.push(array_delete[j].split("_")[1]);
      }
    }
    $("#list_removes").html("IDs: " + array_itens);
    $("#modalRemove").openModal();
  }
  function SendSignalRemove(url_uri){
    for (var i=0; i < array_delete.length; i++){
      if (array_delete[i]){
        var id = url_uri + array_delete[i].split("_")[1] + "/";
        $('#remove_form').attr("action", id).submit();
      }
    }
  }

  function UpdatePaymentTable(){
    var value_account = parseFloat($("#total_account_label").text()).toFixed(2);
    var value_paid = parseFloat($("#all_paid").text()).toFixed(2);
    var value_for_paid = parseFloat(value_account - value_paid);
    if (value_for_paid < 0){
      $("#for_change").text(parseFloat(value_for_paid * -1).toFixed(2));
      $("#value_for_paid").text(value_for_paid.toFixed(2))
    } else if (value_for_paid > 0 ){
      $("#value_for_paid").text(value_for_paid.toFixed(2));
      $("#for_change").text("00.00");
    } else {
      $("#value_for_paid").text("00.00");
      $("#all_paid").text(value_for_paid.toFixed(2));
      $("#for_change").text("00.00");
    }
  }

  function GetCellValues() {
    var id_orders = [];
    $('#table_products tr').each(function() {
      var customerString = $(this).closest('tr').find('td:eq(0)').html();
      if ((customerString) && ($.isNumeric(customerString))){
        id_orders.push(customerString.replace(/(\r\n|\n|\r| )/gm,""));
      }
    });
    return id_orders;
  }

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function CheckIsNaN(value){
    if (isNaN(value)){
      console.log("ified...");
      value = "0.00";
    }
    console.log(isNaN(value));
    return value
  }

  function ajax_send_payment(){
    //var object_payments = new Object();
    var object_send = new Object();
    var get_orders = GetCellValues();
    object_send['all_value'] = $("#total_value_table").text().replace(/(\r\n|\n|\r| )/gm,"");
    object_send['include_couvert'] = $("#deactive_cover").is(":checked");
    object_send['include_rate'] = $("#deactive_rate").is(":checked");
    object_send['type_calculate'] = $("#calculate_options").val();
    object_send['discount'] = CheckIsNaN(parseFloat($("#total_disccount").val()).toFixed(2));
    object_send['rate'] = CheckIsNaN(parseFloat($("#new_value").val()).toFixed(2));
    console.log(object_send['rate']);
    object_send['table_id'] = $("#table").val();
    object_send['orders[]'] = get_orders.toString();
    //JSON.stringify(get_orders);
    object_send['csrfmiddlewaretoken'] = getCookie('csrftoken');
    object_send['payments'] = [];

    object_send['payments'].push({
      'payment_method': $("#payment_method").val()
    });
    object_send['payments'].push({
      'payment_value': $("#value_paid").val()
    });

    if (!object_send['type_calculate']){
      console.log('ifedd...here');
      object_send['type_calculate'] = 'R$';
    }


    console.log(object_send['orders']);

    if ((object_send['payments'][0].payment_method == 'debit') || (object_send['payments'][0].payment_method == 'credit')){
      object_send['payments'].push({
        'flag': $("#flags_payments").val()
      });
    } else if (object_send['payments'][0].payment_method == 'ticket'){
      object_send['payments'].push({
        'flag': $("#vr_flags_payments").val()
      });
    } else if (object_send['payments'][0].payment_method == 'check'){
      object_send['payments'].push({
        'flag': $("#total_payd_check").val()
      });
    } else {
      object_send['payments'].push({
        'flag': 'money'
      });
    }
    object_send.payments = JSON.stringify(object_send.payments);
    return object_send
  }

  var value_paid_fixed = 0;

  function CalculatePayment(element){
    var value = parseFloat(String(element.val()).replace(',', '.'));
    var account_for_paid = parseFloat($("#all_paid").text().replace(',', '.'));

    value_paid_fixed = value_paid_fixed + 1;

    if ((!isNaN(value)) && (!isNaN(account_for_paid))){
      var paid = parseFloat(
          parseFloat(
            $("#all_paid").text()) + parseFloat(value));
      var value_for_paid = parseFloat(
          parseFloat($("#total_account_label").text()) - parseFloat(paid));
      if (value_for_paid < 0 ){
        $("#for_change").text(
          value_for_paid = value_for_paid * -1
        );
        $("#all_paid").text(paid.toFixed(2));
        $("#total_value_paid").text(paid.toFixed(2));
        $("#value_for_paid").text(parseFloat(value_for_paid * -1).toFixed(2));
        $("#btn_closed_account").attr("disabled", false);
      } else if (value_for_paid > 0 ){
        $("#all_paid").text(paid.toFixed(2));
        $("#value_for_paid").text(value_for_paid.toFixed(2));
        $("#total_value_paid").text(paid.toFixed(2));
      } else {
        $("#all_paid").text(paid.toFixed(2));
        $("#total_value_paid").text(paid.toFixed(2));
        $("#value_for_paid").text(value_for_paid.toFixed(2));
        $("#btn_closed_account").attr("disabled", false);
      }
      var value_paid = parseFloat($("#total_value_paid").text().replace(',', '.'));
      var total_account = parseFloat($("#total_account_label").text().replace(',', '.'));
      if ((value_paid > total_account) || (value_paid == total_account)) {
        var modal = $("#modal1");
        modal.openModal();
        $('.modal-action.modal-close').on('click', function(){
          var accepted = $(this).data('action');
          continue_js(accepted);
        })
        function continue_js(event_click){
          if (event_click == true){
            var dataPost = ajax_send_payment();
            dataPost.is_closed = true;
            post_data(dataPost);
          } else {
            var dataPost = ajax_send_payment();
            dataPost.is_closed = false
            post_data(dataPost);
          }
          
        }

      } else {
        var dataPost = ajax_send_payment();
        dataPost.is_closed = false;
        post_data(dataPost);
      }
        addRowTable("add", 'table_products', value, value_paid_fixed, '','Valor pago de conta', 3);
      }
    }
  function post_data(dataPost){
    console.log("posted...")
    jqxhr = $.ajax({
        data: dataPost,
        type: 'POST',
        url: window.location.pathname
    });
    console.log("intiate...s")
    jqxhr.done(function (data) {
      console.log("initate okeyssss...")
      console.log(data);
      if (data.status == 'ok') {
        Materialize.toast(data.message, 4000);
      } else {
          Materialize.toast("Erro encontrado: " + data.message, 40000);
      }

    });
    jqxhr.fail(function (fail) {
      Materialize.toast("Falha na comunicação com o servidores", 40000)
    });
    
    return false
  };  

  function DeactiveRate(element, type, action, calculate){
    if (calculate){
      add_rate = true;
    } else {
      add_rate = false;
    }
    if ((type=='rate') && (element.checked == false)){
      var text_value_rate = $("#all_value_rate").text();
      if (text_value_rate){
        var value = parseFloat(text_value_rate.split(" ")[1]);
        addRowTable('add', 'table_products', value, 'rate_discount', 'Entrada/Taxa de serviço');
        $("#total_account_label").text(parseFloat(parseFloat($("#total_account_label").text()) - value).toFixed(2));
        $("#total_value_table").text(parseFloat(parseFloat($("#total_value_table").text()) - value).toFixed(2));
      }

    } else if ((type=='rate') && (element.checked == true) && (!action) && (add_rate == false)){
      var text_value_rate = $("#all_value_rate").text();
      if (text_value_rate){
        var value = parseFloat(text_value_rate.split(" ")[1]);
        addRowTable('remove', 'table_products', value, 'rate_discount', 'Entrada/Taxa de serviço');
        $("#total_account_label").text(parseFloat(parseFloat($("#total_account_label").text()) + value).toFixed(2));
        $("#total_value_table").text(
          parseFloat(parseFloat($("#total_value_table").text()) + value).toFixed(2));
      }
    }
    if ((type == 'cover') && (element.checked == false)){
      var text_value_cover = $("#all_value_cover").text();

      if (text_value_cover){
        var value = parseFloat(text_value_cover.split(" ")[1]);
        addRowTable('add', 'table_products', value, 'cover_discount', 'cover');
        $("#total_account_label").text(
          parseFloat(
            parseFloat(
              $("#total_account_label").text()
            ) - value
          ).toFixed(2)
        );
        $("#total_value_table").text(
          parseFloat(
            parseFloat(
              $("#total_value_table").text()
            ) - value
          ).toFixed(2)
        );
      }
    } else if ((type=='cover') && (element.checked == true) && (!action) && (add_rate == false)){
      var text_value_rate = $("#all_value_cover").text();
      if (text_value_rate){
        var value = parseFloat(text_value_rate.split(" ")[1]);
        addRowTable('remove', 'table_products', value, 'cover_discount', 'cover');
        $("#total_account_label").text(parseFloat(parseFloat($("#total_account_label").text()) + value).toFixed(2));
        $("#total_value_table").text(parseFloat(parseFloat($("#total_value_table").text()) + value).toFixed(2));
      }
    }
    UpdatePaymentTable();
    
  }


  function PaymentsOptions(value){
    var divs = {
      'money':'payments_type_money', 
      'check': 'payments_type_check',
      'credit': 'payment_cards_cb',
      'debit': 'payment_cards_cb',
      'ticket': 'payment_cards_vr'
    };
    for (option in divs){
      if (option != value){
        var n_element = document.getElementById(divs[option]);
        n_element.style.display='none';
      }
    }
    document.getElementById(divs[value]).style.display='';
    if (divs[value] != 'money'){
      $("#payments_type_money").show();
    }
    $("#payment_button").show();
  }
  function deleteRowTable(table, id){
    var elem = document.getElementById(id);
    if (elem){
      elem.parentNode.removeChild(elem);
    }
    return false;
  }
  function OnChangeCalculate(value){
    var value_discount = $("#total_disccount").val();
    var value_add = $("#new_value").val();
    if (value_add){
      AddValue(value_add);
    }
    if (value_discount){
      DiscountFunction(value_discount);
    }
  }
  function changedOptionCalculate(id){
    var e = document.getElementById(id);
    var option_selected = e.options[e.selectedIndex].text;
    if ((option_selected != '%') && (option_selected != "R$")){
      alert("O calculo do desconto e de acrésimos serão realizados pelo valor padrão (R$), caso queira o calculo em (%) escolha na opção: 'Calcular em' do lado esquerdo");
      $('.select-dropdown').val("R$");
      e.options[e.selectedIndex].text = "R$";
      return "R$";
    }
    if (option_selected == 'R$'){
      return "R$";
    }
    if (option_selected == '%'){
      return '%';
    }
  }
  
  function validate(evt) {
    var theEvent = evt || window.event;
    var key = theEvent.keyCode || theEvent.which;
    key = String.fromCharCode( key );
    var regex = /^[0-9,\9\b]*\.?[0-9]*$/;
    if (( !regex.test(key)) && (evt.keyCode != 8) && (evt.keyCode  != 9)) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
  }


function ShowEditModal(url, form, modal){
  $.get(url, function(data){
    $(form).html(data);
    $(modal).openModal()
  })
}
function ShowTable(table){
  var table = $(table).DataTable({
    "language":{
      "lengthMenu": "Mostrando _MENU_ por pagina",
      "zeroRecords": "Sem resultados, desculpe :(",
      "infoEmpty": "Sem registros, desculpe :(",
      "info": "Mostrando paginas _PAGE_ de _PAGES_",
      "infoFiltered": "(Filtrando de _MAX_)"

    }
  });
}
function func_clear_specific_item(item){
  var t = document.getElementById("div_forms_configurations").childNodes;
  for(var i=0; i < t.length; i++){
    if ((t[i].id) && (t[i].id != item) && (t[i].style)){
      t[i].remove();
    }
  }
}
function func_clear(){
  var t = document.getElementById("div_forms_configurations").childNodes;
  t.remove();
}