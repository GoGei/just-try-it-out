function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    xhrFields: {withCredentials: true},
    headers: {'X-CSRFToken': getCookie('csrftoken')},
});


$(document).ready(function () {
    $(".breadcrumb li:last").addClass("active").css("font-weight", "bold");

    // $('.select2').select2();
    $('.select2').each(function () {
        initSelect2($(this));
    });
});


function initSelect2($field) {
    /*
    function to init or re-init select2
    function used to init and re-init field with its properties after show/hide actions of parent with class d-none
    properties of width of select2 are related to parent.
    In case of select2 width related to parent -> width on hidden parent is set to 0px
    */
    let ajaxConfig = {};
    try {
        let jsonString = $field?.data('select-2-config')?.replaceAll("'", "\"");
        if (jsonString) {
            ajaxConfig = JSON.parse(jsonString);
        }
    } catch (e) {
        console.log(e)
    }

    $field.select2(ajaxConfig);
}

DEFAULT_PAGE_SIZE = 50;