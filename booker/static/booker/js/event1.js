var $ = django.jQuery;
$(function () {
    var event_type = $('#id_event_type').val();
    var ensemble_type = $('#id_ensemble_type').val();
    console.log(ensemble_type);
    if (ensemble_type == 'String Quartet') {
        $('.field-musician_five').hide();
    }
    if (ensemble_type == 'Soloist') {
        $('.field-musician_five').hide();
        $('.field-musician_two').hide();
        $('.field-musician_three').hide();
        $('.field-musician_four').hide();
        $('.field-musician_five').hide();
    }
    if (ensemble_type == 'String Duo') {
        $('.field-musician_five').hide();
        $('.field-musician_three').hide();
        $('.field-musician_four').hide();
        // $('.field-musician_five').hide();
    }
    if (ensemble_type == 'String Trio' || 'Piano Trio') {
        $('.field-musician_four').hide();
        $('.field-musician_five').hide();
    }
    // if (ensemble_type == '2') {
    //     $('.field-musician_four').hide();
    //     $('.field-musician_five').hide();
    // }

    $("#id_ensemble_type").change(function () {
        var type = this.value;
        $('.field-musician_one').show();
        $('.field-musician_two').show();
        $('.field-musician_three').show();
        $('.field-musician_four').show();
        $('.field-musician_five').show();
        var ensemble_type = $('#id_ensemble_type').val();
        console.log('its', ensemble_type);
        if (type == '1') {
            console.log('String Quartet');
            $('.field-musician_five').hide();
        }
        if (type == '5') {
            console.log('soloist');
            $('.field-musician_two').hide();
            $('.field-musician_three').hide();
            $('.field-musician_four').hide();
            $('.field-musician_five').hide();
        }
        if (type == '4') {
            console.log('string duo');
            $('.field-musician_three').hide();
            $('.field-musician_four').hide();
            $('.field-musician_five').hide();
        }
        if (type == '3') {
            console.log('piano trio');
            $('.field-musician_four').hide();
            $('.field-musician_five').hide();
        }
        if (type == '2') {
            console.log('string trio');
            $('.field-musician_four').hide();
            $('.field-musician_five').hide();
        }
    });
    if (event_type !== 'wedding') {
        $('.field-wedding_options').hide();
        $('.field-prelude_one').hide();
        $('.field-prelude_two').hide();
        $('.field-prelude_three').hide();
        $('.field-prelude_four').hide();
        $('.field-prelude_five').hide();
        $('.field-processional').hide();
        $('.field-num_grandmothers').hide();
        $('.field-num_mothers').hide();
        $('.field-num_bridesmaids').hide();
        $('.field-num_flowers').hide();
        $('.field-num_rings').hide();
        $('.field-bridal').hide();
        $('.field-unity').hide();
        $('.field-communion').hide();
        $('.field-recessional').hide();
    }
    $("#id_event_type").change(function () {
        var status = this.value;
        if (status === "wedding") {
            console.log('wedding');
            $('.field-wedding_options').show();
            $('.field-prelude_one').show();
            $('.field-prelude_two').hide();
            $('.field-prelude_three').show();
            $('.field-prelude_four').show();
            $('.field-prelude_five').show();
            $('.field-processional').show();
            $('.field-num_grandmothers').show();
            $('.field-num_mothers').show();
            $('.field-num_bridesmaids').show();
            $('.field-num_flowers').show();
            $('.field-num_rings').show();
            $('.field-bridal').show();
            $('.field-unity').show();
            $('.field-communion').show();
            $('.field-recessional').show();
        } else {
            console.log('not wedding');
            $('.field-wedding_options').hide();
            $('.field-prelude_one').hide();
            $('.field-prelude_two').hide();
            $('.field-prelude_three').hide();
            $('.field-prelude_four').hide();
            $('.field-prelude_five').hide();
            $('.field-processional').hide();
            $('.field-num_grandmothers').hide();
            $('.field-num_mothers').hide();
            $('.field-num_bridesmaids').hide();
            $('.field-num_flowers').hide();
            $('.field-num_rings').hide();
            $('.field-bridal').hide();
            $('.field-unity').hide();
            $('.field-communion').hide();
            $('.field-recessional').hide();
        }
    });
});
