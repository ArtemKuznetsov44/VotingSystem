$(function ($) {
   


    let element_to_add_before = $('form').children('div:last')
    let current_anonymous_element = $('input[name="anonymous"]').parent().detach()
    let current_users_element  = $('input[name="users"]').closest('div.one-field')


    $('input[name="is_open"]').on('change', function() {
        if ($(this).prop('checked')) {
            current_anonymous_element.detach()
            element_to_add_before.before(current_users_element)
        }
        else {

            current_users_element.detach()
            element_to_add_before.before(current_anonymous_element)
        }

    })
})