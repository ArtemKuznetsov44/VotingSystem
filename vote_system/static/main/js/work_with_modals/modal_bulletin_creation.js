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
                'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between'
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
    });

    // Current event happens when user change the checkbox-switch status:
    $('div.modal').on('change', 'div.form-check.form-switch input.form-check-input', function () {
        // console.log(window.location.href.slice(0, -1).split('/'))
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

    function clean_modal_window() {
        // noinspection JSUnresolvedReference
        $('#add_question_ajax').modal('hide');
        let modal_body = $('div.modal-body');
        $(modal_body).find('form').trigger('reset');
        $(modal_body).find('div.one-bulletin[bulletin!="0"]').remove();

        $('div.one-form[bulletin="0"]').find('div.answers-input-container').empty();
        $('.alert-success').text('').addClass('d-none');
        $('.alert-danger').text('').addClass('d-none');
        bulletinForms = {0: 0};
    }


    // Current event happens when use click on 'СОЗДАТЬ (main)' button:
    $('div.modal-content').on('click', 'div.modal-footer > button.send-form-btn', function () {

        let data_from_all_forms = collect_all_from_modal();
        let voting_pk_element = document.getElementById('voting_pk')
        let voting_pk = null;

        if (voting_pk_element) {
            voting_pk = JSON.parse(voting_pk_element.textContent);
            console.log('Voting PK - ', voting_pk);
            data_from_all_forms['voting_pk'] = voting_pk;
        }


        // Send fetch XMLHTTPRequest - each fetch return promises (for ok result and for errors(in catch block)):
        fetch($('div.modal-body > div.one-form > form').attr('action'), {
            method: 'POST', // Sending method type
            // Headers for csrf_token and also specify that content type of data to send is JSON-format:
            headers: {
                'X-CSRFToken': getCookiesByName('csrftoken'), 'Content-Type': 'application/json',
            }, // Our data for send, here the name for it is "body":
            body: JSON.stringify(data_from_all_forms),
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

                    let bulletins_response_dict = JSON.parse(data['bulletins_data']);
                    if (voting_pk) {
                        add_into_active_vote_page(bulletins_response_dict);
                    } else {
                        add_into_voting_creation_page(bulletins_response_dict)
                    }

                    setTimeout(() => clean_modal_window(), 1500);

                    // // add_created_elements(JSON.parse(data['bulletins_data']));
                    // // if (voting_creation_action) {
                    // //
                    // // }
                    // // Save the count of anonyms:
                    // let anonyms_count = $('input[name="anonyms"]').val();
                    // // Save the checked users:
                    // let selected_users = $('input[name="users"]:checked').map(function () {
                    //     return $(this).attr('id')
                    // }).get();
                    //
                    // let data_to_save = {
                    //     voting_title: $('input[name="title"]').val(),
                    //     voting_description: $('textarea[name="description"]').val(),
                    //     voting_participants: {'anonyms_count': anonyms_count, 'selected_users': selected_users}
                    // }
                    //
                    // localStorage.setItem('form_data', JSON.stringify(data_to_save));
                    // console.log('Data in localStorage - ', localStorage.getItem('form_data'), typeof (localStorage.getItem('form_data')))
                    // // Set timout for window reload - 2 seconds:
                    // //setTimeout(() => window.location.reload(), 2000)
                }
            })
    });

    function add_into_voting_creation_page(bulletins_dict) {
        console.log('Our bulletins_dict', bulletins_dict)
        let empty_content_div = $('div.empty-content');

        if (!empty_content_div.prop('hidden')) {
            empty_content_div.prop('hidden', true);
        }

        $.each(bulletins_dict, function (bulletin_pk, bulletin_data) {
            let div_one_row = $('<div>').attr('class', 'one-row');
            let label = $('<label>');
            label.append($('<input>').attr('type', 'checkbox').attr('name', 'bulletins').val(bulletin_pk).prop('hidden', true));

            let div_one_bulletin = $('<div>').attr('class', 'one-bulletin');
            div_one_bulletin.append($('<div>').css({'font-weight': 'bold'}).text(bulletin_data['question']));
            div_one_bulletin.append($('<div>').css({'font-style': 'italic'}).text(bulletin_data['type'] === 'single' ? 'Одиночный ответ' : 'Множественный выбор'));
            let answers_div = $('<div>');
            let answers_ol = $('<ol>');

            $.each(bulletin_data['answers'], function (answer_id, answer_text) {
                answers_ol.append($('<li>').text(answer_text));
            });

            answers_div.append(answers_ol);
            div_one_bulletin.append(answers_div);
            label.append(div_one_bulletin);
            div_one_row.append(label).append($('<svg style="margin-top: 5px;" class="delete-icon svg-as-btn-delete" xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24"><path fill="currentColor" d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"></path></svg>').attr('value', bulletin_pk));

            $('div.bulletins-for-select').append(div_one_row);
        });

    }

    function add_into_active_vote_page(bulletins_dict) {

        let results_preview_container = $('div.results-preview');
        let bulletins_for_select_container = $('div.bulletins-container');

        $.each(bulletins_dict, function (bulletin_pk, bulletin_data) {
             // Code to append into results-preview container:
            let one_bulletin_result_preview = $('<div>').attr('class', 'one-bulletin-result-preview').attr('id', `bulletin_res_preview_${bulletin_pk}`);
            one_bulletin_result_preview.append($('<h5>').text(`Бюллетень с ID ${bulletin_pk}:`));
            one_bulletin_result_preview.append($('<p>').text(bulletin_data['question']).css({
                'font-style': 'italic'
            }));
            one_bulletin_result_preview.append($('<hr/>'));
            // Current element is the part of one bulletin result-preview:
            let answers_ol = $('<ol>')

            // This element for bulletins card to make bulletin active:
            let answers_ol_with_class_name = $('<ol>').attr('class', 'bulletin-answers');

            $.each(bulletin_data['answers'], function (answer_id, answer_text) {
                answers_ol.append($('<li>').attr('id', `answer_${answer_id}`).text(`${answer_text} - 0`))
                answers_ol_with_class_name.append($('<li>').text(answer_text));
            });

            one_bulletin_result_preview.append(answers_ol);
            one_bulletin_result_preview.append($('<hr/>'));
            one_bulletin_result_preview.append($('<div>').attr('class', 'total-votes-count').text('Всего проголосовало: 0').css({
                'text-decoration': 'underline'
            }));

            results_preview_container.append(one_bulletin_result_preview);

            // Code to append into bulletins-for-select container:
            let one_bulletin_card = $('<div>').attr('class', 'one-bulletin-card');
            let label = $('<label>').attr('class', 'bulletin-for-select');

            label.append($('<input>').attr('type', 'checkbox').attr('name', 'active').val(bulletin_pk));

            let one_bulletin_context = $('<div>').attr('class', 'one-bulletin-context');
            one_bulletin_context.append($('<div>').attr('class', 'bulletin-question').text(bulletin_data['question']).css({
                'white-space': 'pre-wrap',
                'font-weight': 'bold'
            }));
            one_bulletin_context.append($('<div>').attr('class', 'bulletin-type').val(bulletin_data['type']).text('Тип вопроса: ' + bulletin_data['type'] === 'single' ? 'Одиночный ответ' : 'Множественный выбор').css({
                'font-style': 'italic'
            }));
            one_bulletin_context.append(answers_ol_with_class_name);
            label.append(one_bulletin_context);
            one_bulletin_card.append(label);

            bulletins_for_select_container.append(one_bulletin_card);
        });

    }

    function add_into_bulletins_for_activate(bulletins_dict, container) {

    }

    function add_into_results_preview(bulletins_dict, results_container) {

    }

    // function add_created_elements(bulletins) {
    //     // voting_creation_action contains: TRUE or FALSE
    //     let voting_creation_action = check_url()
    //     console.log('Voting creation action -', voting_creation_action);
    //
    //     if (voting_creation_action) {
    //         // Code to add bulletins for select into voting_create.html
    //         console.log('Code has been stated!')
    //         add_into_voting_creation_page(bulletins)
    //     } else {
    //         // Code to add bulletins for select into active_vote.html
    //     }
    // }

    // Function to collect all data from form into dict:
    function collect_all_from_modal() {

        // Collect data from all Forms in modal windows:
        let all_data_from_forms = {}
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
            all_data_from_forms[index]= dict_for_form_data;
        });

        return all_data_from_forms
    }

    // // Window load event - happens during page loading:
    $(window).on('load', function () {
        // Try to get data for voting-form from sessionStorage (getItem will return null on nothing in it):
        let form_data = JSON.parse(localStorage.getItem('form_data'))
        /*
        form_data = {
            'voting_title': <voting_title_value>,
            'voting_description': <voting_description_value>,
            'voting_participants': {'anonyms_count': <count_of_anonyms>, 'selected_users': [input_id_1, input_id_2, ...]}
        }
        */
        // Cases when received data not null:
        if (form_data) {
            $('input[name="title"]').val(form_data.voting_title);
            $('textarea[name="description"]').val(form_data.voting_description);

            $('input[name="anonyms"]').val(form_data.voting_participants.anonyms_count);

            form_data.voting_participants.selected_users.forEach(function (value) {
                $(`#${value}`).prop('checked', true);
            })
        }

        localStorage.clear();
    });
});

