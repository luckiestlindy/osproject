var $ = django.jQuery;

$(function () {
    var event_type = $('#id_event_type').val();
    if (event_type !== 'wedding') {
        $('.field-wedding_options').hide();
    }
    $("#id_event_type").change(function () {
        var status = this.value;
        if (status === "wedding") {
            $('.field-wedding_options').show();
        } else {
            $('.field-wedding_options').hide();
        }
    });
});

//$(function () {
//    var ensemble_type = $('#id_ensemble_type').val();
//    if (ensemble_type == 1) {
//        console.log('Soloist');
//    }
//    $('#id_ensemble_type').change(function () {
//        console.log('it changed');
//    })
//})