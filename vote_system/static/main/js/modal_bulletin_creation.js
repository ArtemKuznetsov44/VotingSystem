$(document).ready(function () {

    // The key - it is the bulletin form attribute - bulletin; the value - count of answers for current bulletin:
    let bulletinForms = {0: 0}

    let div_with_form_template = $('div.modal-body > div.one-form').clone();

    let svg_delete_icon_template = $('<svg class="delete-icon svg-as-btn-delete" xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24"><path fill="currentColor" d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"></path></svg>');

    // Such event happens when user click on 'Добавить ответ' button:
    $('div.modal-body').on('click', 'button.add-new-answer-btn', function () {
        // Finding the div.one-form element to find its bulletin value:
        const bulletin_form_number = parseInt($(this).closest('div.one-form').attr('bulletin'))

        // Find the count of answers for current bulletin:
        // let current_answers_count = bulletinForms[bulletin_form_number]['answers'];
        let current_answers_count = bulletinForms[bulletin_form_number];

        // The next element of current button is our container:
        let current_form_container_for_answers = $(this).next()

        add_new_answers(bulletin_form_number, current_answers_count, current_form_container_for_answers, 1)
    });


    // Such event happens when user click on 'Добавить бюллетень' button:
    $('button.add-new-bulletin-btn').on('click', function () {
        /* STEPS:
           1. Clone form template
           2. Add new instance in bulletinForms dictionary
           2. Add new clone after current last form element in modal window
        * */

        let tmp_clone = div_with_form_template.clone();

        let last_bulletin_form_number = Object.keys(bulletinForms).length - 1;
        let new_bulletin_form_number = last_bulletin_form_number + 1;


        bulletinForms[new_bulletin_form_number] = 0

        tmp_clone.attr('bulletin', new_bulletin_form_number);
        tmp_clone.find('h5').text(`Бюллетень №${new_bulletin_form_number + 1}`)

        $('div.modal-body').children(':last').after(tmp_clone);
    });


    function add_new_answers(bulletin, current_answers_count, container, count_of_fields, initial = null) {

        // In a loop (because we can create more the one answer-field; their count we can specify
        // on <count_of_fields> argument for current function):
        for (let i = 1; i <= count_of_fields; i++) {

            // Create new div with one-field class, also add attr answer for it:
            let new_one_field_div = $('<div>').addClass('one-field').attr('answer', current_answers_count + i);

            let new_label_for_answer_input = $('<label>').attr('for', current_answers_count + i).text(`Ответ №${current_answers_count + i}:`).css({
                'display': 'flex',
                'flex-direction': 'row',
                'align-items': 'center',
                'justify-content': 'space-between'
            });

            let new_input_for_answer = $('<input>').addClass('form-control').attr('name', current_answers_count + i).attr('required', true);

            if (initial != null) {
                new_input_for_answer.val(initial[i - 1]);
            }

            let new_icon_for_answer = svg_delete_icon_template.clone();

            new_label_for_answer_input.append(new_icon_for_answer);
            new_one_field_div.append(new_label_for_answer_input);
            new_one_field_div.append(new_input_for_answer);

            container.append(new_one_field_div);
        }

        // bulletinForms[bulletin]['answers'] += count_of_fields;
        bulletinForms[bulletin] += count_of_fields;
        console.log(bulletinForms)
    }

    // Current event happens when user click on delete-icon near the answer div:
    $('div.modal-dialog').on('click', 'svg.delete-icon', function () {

        const current_bulletin_form = $(this).closest('div.one-form');

        let answer_div_container = $(this).closest('div.one-field[answer]');

        let bulletin_form_number = parseInt($(current_bulletin_form).attr('bulletin'));

        console.log('element to remove - ', answer_div_container);

        answer_div_container.remove();

        bulletinForms[bulletin_form_number] -= 1;
        console.log('Delete answer: ', bulletinForms)

        // Now we need to find all other answers for current bulletin and make the label and div count - 1:
        current_bulletin_form.find('div.one-field[answer]').each(function (index, answer_div_container) {

            // Re-numerate them - specify the index:
            $(answer_div_container).attr('answer', index);

            let label = $(answer_div_container).find('label');
            label.attr('for', index);
            label.text(`Ответ №${index + 1}`);
            label.append(svg_delete_icon_template.clone());

            $(answer_div_container).find('input').attr('name', index);
        });
    })

    // Current event happens when user change the checkbox-switch status:
    $('div.modal').on('change', 'div.form-check.form-switch input.form-check-input', function () {
        const def_answers = ['За', 'Против', 'Воздержался'];
        const bulletin_form_number = parseInt($(this).closest('div.one-form').attr('bulletin'));
        let answers_container = $(this).parent().next().next();
        let current_answer_count = bulletinForms[bulletin_form_number];

        if ($(this).prop('checked')) {
            add_new_answers(bulletin_form_number, current_answer_count, answers_container, 3, def_answers);
        } else {
            // Keep the count of div.one-field elements in answers-container div element:
            let count = answers_container.find('div.one-field').length;
            // Clean answers-container with all answers:
            answers_container.empty();
            // Change data about the count of answers for current bulletin:
            // bulletinForms[bulletin_form_number]['answers'] -= count;
            bulletinForms[bulletin_form_number] -= count;
        }

    });

    // Current event happens when user click on delete-bulletin-icon:
    $('div.modal div.modal-dialog').on('click', 'svg.delete-bulletin-icon', function () {
        if (Object.keys(bulletinForms).length > 1) {

            let current_bulletin = $(this).closest('div.one-form');
            let current_bulletin_number = parseInt($(current_bulletin).attr('bulletin'));

            delete bulletinForms[current_bulletin_number];

            let new_tmp_dict = {}
            Object.values(bulletinForms).forEach((value, index) => {
                new_tmp_dict[index] = value;
            })

            bulletinForms = new_tmp_dict;
            current_bulletin.remove();

            // Modify each element in each div block with form:
            $('div.modal-body').find('div.one-form').each(function (index, div_form_container) {
                $(div_form_container).attr('bulletin', index);
                $(div_form_container).find('h5').text(`Бюллетень №${index + 1}`);
            });
        }
    });


    // Current event happens when use click on 'СОЗДАТЬ (main)' button:
    $('div.modal-content').on('click', 'div.modal-footer > button.send-form-btn', function () {

        // Collect data from all Forms in modal windows:
        let all_data_from_forms = []
        $('div.modal-content div.modal-body').find('div.one-form').each(function (index, one_div_with_form) {
            let current_form = $(one_div_with_form).find('form')
            let current_form_data = $(current_form).serializeArray();

            let dict_for_form_data = {}
            let answers_in_form = []

            console.log(current_form_data)

            current_form_data.forEach(function (field) {
                console.log('field.name - ', field.name, ' | ', 'field.value - ', field.value);

                if (field.value.trim() === '') {
                    $('.alert-danger').text(`В бюллетени №${index + 1} есть незаполненные поля`).removeClass('d-none');
                    return;
                }

                if (['type', 'question'].includes(field.name)) {
                    dict_for_form_data[field.name] = field.value;
                } else {
                    answers_in_form.push(field.value);
                }
            });

            dict_for_form_data['answers'] = answers_in_form;
            console.log('Словарь с данными с ', index, ' формы - ', dict_for_form_data);
            all_data_from_forms.push(dict_for_form_data);
        });

        // Send fetch XMLHTTPRequest - each fetch return promises (for ok result and for errors(in catch block)):
        fetch($('div.modal-body > div.one-form > form').attr('action'), {
            method: 'POST', // Sending method type
            // Headers for csrf_token and also specify that content type of data to send is JSON-format:
            headers: {
                'X-CSRFToken': getCookiesByName('csrftoken'),
                'Content-Type': 'application/json',
                // 'action': 'create'
            },
            // Our data for send, here the name for it is "body":
            body: JSON.stringify(all_data_from_forms),
        })
            // Here we need to get response.json() for first promise then:
            .then(response => response.json())
            // Only after first promise with then, in the second one we can work with our json object from server:
            .then(data => {
                console.log(data);
                if ('error' in data) {
                    $('.alert-success').text('').addClass('d-none')
                    $('.alert-danger').text(data.error).removeClass('d-none')
                } else {
                    $('.alert-danger').text('').addClass('d-none')
                    $('.alert-success').text(data.ok).removeClass('d-none')


                    let data_to_save = {
                        voting_title: $('input[name="title"]').val(),
                        voting_description: $('textarea[name="description"]').val()
                    }

                    localStorage.setItem('form_data', JSON.stringify(data_to_save));
                    console.log('Data in localStorage - ', localStorage.getItem('form_data'), typeof(localStorage.getItem('form_data')))
                    // Set timout for window reload - 2 seconds:
                    setTimeout(() => window.location.reload(), 2000)
                }
            })
    });


    // // Window load event - happens during page loading:
    $(window).on('load', function() {
        // Try to get data for voting-form from sessionStorage (getItem will return null on nothing in it):
        let form_data = JSON.parse(localStorage.getItem('form_data'))
        // Cases when received data not null:
        if (form_data) {
            $('input[name="title"]').val(form_data.voting_title);
            $('textarea[name="description"]').val(form_data.voting_description);
        }

        localStorage.clear();
    });
});

// Function from Django site. Lets to send data not from form only. It generates a csrf_token
function getCookiesByName(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookieValue;
}