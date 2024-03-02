let $form = $('#hashtableForm');

$("#refreshBtn").click(function (e) {
    e.preventDefault();
    clearFormErrors();
    $form[0].reset();
});

$('#sendBtn').click(function (e) {
    e.preventDefault();
    clearFormErrors();

    let formDataJSON = serializeFormToJSON($form);

    $.ajax({
        type: "POST",
        url: $form.attr('action'),
        data: JSON.stringify(formDataJSON),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            // console.log(response);
        },
        error: function (xhr, textStatus, errorThrown) {
            displayFormErrors(xhr?.responseJSON);
        }
    });
});


$("#addRowBtn").click(function () {
    let newRow = $('.form-group.row').last().clone();

    newRow.find('input').val('');
    newRow.find('input').each(function () {
        let newNameAttr = $(this).attr('name').replace(/\d+$/, function (str) {
            return parseInt(str) + 1;
        });
        let newIdAttr = $(this).attr('id').replace(/\d+$/, function (str) {
            return parseInt(str) + 1;
        });
        $(this).attr('name', newNameAttr);
        $(this).attr('id', newIdAttr);
    });

    newRow.find('.btn-drop-row').removeAttr('id');

    $(newRow).find('.form-errors-div').each(function () {
        $(this).remove();
    });

    $('.form_buttons').before(newRow);
});

$(document).on('click', '.btn-drop-row', function () {
    let $row = $(this).closest('.form-group.row');
    let key = $row.find('input[name^="key"]').val();

    if ($('.form-group.row').length <= 1) {
        return;
    }

    $row.remove();

    let data = {
        "key": key,
        "hash_name": $('#id_hash_name').val()
    }

    $.ajax({
        type: "DELETE",
        url: $form.attr('action'),
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            console.log(response);
        },
        error: function (err) {
            console.error(err);
        }
    });
});

function serializeFormToJSON($form) {
    let formArray = $form.serializeArray();
    let itemsArray = [];

    let formDataJSON = {};

    // Process each form input
    $.each(formArray, function () {
        let match = this.name.match(/(key|value)-(\d+|\w+)/);
        if (match) {
            let type = match[1];
            let index = match[2];

            if (!itemsArray[index]) {
                itemsArray[index] = {key: '', value: ''};
            }
            itemsArray[index][type] = this.value || '';
        }
    });

    itemsArray = itemsArray.filter(function (item) {
        return item !== undefined;
    });

    formDataJSON['hash_name'] = $('#id_hash_name').val();
    formDataJSON['items'] = itemsArray;

    return formDataJSON;
}

function displayFormErrors(errors) {
    function insertError($elem, err) {
        $elem.after($('<div>', {
            class: 'text-danger form-errors-div',
            text: err,
        }));
    }

    let hash_name_errors = errors?.hash_name || null;
    if (hash_name_errors) {
        let $field = $('#id_hash_name');
        hash_name_errors.forEach(function (error) {
            insertError($field, error);
        });
    }

    let items_errors = errors?.items || null;
    if (items_errors) {
        $('.form-group.row').each(function (index, element) {
            let $element = $(element);

            let current_errors = items_errors[index];
            if (current_errors) {
                let key_errors = current_errors?.key || null;
                let value_errors = current_errors?.value || null;

                if (key_errors) {
                    let $elems = $element.find('.key-class');
                    $elems.each(function () {
                        insertError($(this), key_errors);
                    });
                }

                if (value_errors) {
                    let $elems = $element.find('.value-class');
                    $elems.each(function () {
                        insertError($(this), value_errors);
                    });
                }
            }
        });
    }
}

function clearFormErrors() {
    $('.form-group.row').each(function () {
        $(this).find('.form-errors-div').remove();
    });
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
                            id: index + 1,
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
                console.log(response)
            })
            .fail(function (error) {
                console.error(error);
            });
    });
});