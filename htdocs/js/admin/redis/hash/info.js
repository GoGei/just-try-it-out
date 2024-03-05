let $form = $('#hashtableForm');

function applyResponse(response) {
    $('#form-rows').html(response);
}

$(document).ready(function () {
    let $hash_name = $('#id_hash_name');

    $hash_name.select2({
        allowClear: false,
        width: '100%',
        tags: true,
        ajax: {
            url: $form.data('keys-url'),
            method: 'GET',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    search: params.term,
                    page: params.page,
                    limit: DEFAULT_PAGE_SIZE,
                    offset: DEFAULT_PAGE_SIZE * params.page || 0,
                    format: 'json'
                };
            },
            processResults: function (data, params) {
                params.page = params.page || 1;
                return {
                    pagination: {
                        more: Boolean(data.next)
                    },
                    results: $.map(data, function (obj, index) {
                        return {
                            id: obj.key,
                            text: obj.key
                        };
                    })
                }
            }
        }
    });

    $hash_name.on('select2:select', function (e) {
        let selectedValue = e.params.data.text; // Get the selected value
        $.get($form.attr('action'),
            {
                key: selectedValue
            })
            .done(function (response) {
                applyResponse(response);
            })
            .fail(function (error) {
                console.error(error);
            });
    });
});