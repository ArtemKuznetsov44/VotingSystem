$(function ($) {

    let anonyms_box = $('form > div.box-for-anonyms')
    let users_box = $('form > div.box-for-users')
    console.log(anonyms_box);
    console.log(users_box);

    // Function for show or hidden the users and anonyms boxes by input[name="is_open"] value:
    $('input[name="is_open"]').on('change', function () {
        if ($(this).prop('checked')) {
            users_box.removeAttr('hidden');
            anonyms_box.attr('hidden', '');
        } else {
            users_box.attr('hidden', '');
            anonyms_box.removeAttr('hidden');
        }
    });

    // Function to update value under input with range type for anonymous:
    $('input[type="range"]').on('change', function(){
        let p = $(this).next();
        $(p).text('Количество: ' + this.value);
    });

    // Function where we use the click on label like/instead the click on input with checkbox type:
    $('fieldset > div.bulletins-for-select > div.one-row > label').on('click', function () {
        let input_element = $(this).find('input[type="checkbox"]')[0];
        if ($(input_element).prop('checked')) {

            console.log('element to unchecked | BEFORE STATE- ', $(input_element).prop('checked'));
            // With prop method we can change the real state of input-checked state.
            // ! IN HTML OUR INPUT CAN STEAL HAVE CHECKED IN ITS TAG, but in POST method with form submit, current input,
            // would not be sent !
            $(input_element).prop('checked', false);
            console.log('AFTER - ', $(input_element).prop('checked'));
            $(input_element).removeAttr('checked');
            $(this).css({
                'background-color': 'white',
            })
        } else {
            console.log('element to check | BEFORE STATE - ', $(input_element).prop('checked'));
            $(input_element).prop('checked', true);
            console.log('AFTER - ', $(input_element).prop('checked'));
            $(input_element).attr('checked')
            $(this).css({
                'background-color': 'lightgreen',
            })
        }
    });

    $('svg.svg-as-btn-delete').on('click', function() {

        let bulletin_id_for_delete = $(this).prev('label').find('input[type="checkbox"]').attr('value');
        let div_element_for_remove = $(this).closest('div.one-row')
        console.log(div_element_for_remove);
        console.log('For deleting bulletin_id - ', bulletin_id_for_delete);

        let confirm_res = confirm('Вы действительно хотите удалить бюллетень?')

        if (confirm_res) {
            fetch($('div.modal-body > div.one-form > form').attr('action'), {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookiesByName('csrftoken'),
                'Content-Type': 'application/json',
                'accept': 'application/json'
            },
            body: JSON.stringify({'to_delete': bulletin_id_for_delete})
        })
            .then(response => {
                console.log(response);
                div_element_for_remove.remove();
                let bulletins_selection_container = $('div.bulletins-for-select');
                console.log('Length - ', bulletins_selection_container.children().length)
                if (bulletins_selection_container.children().length === 1) {
                    $(bulletins_selection_container).find('div.empty-content').prop('hidden', false);
                }
            })
            .catch(error => console.log(error))
        }

    });

});
