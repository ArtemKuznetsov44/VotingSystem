// This function works when document is ready:
$(function ($) {

    // Some variables for work with:
    // Instance to keep the data about: what the form and how much questions it has:
    let formAnswers = [
        {"question_form": 0, 'answers': 0}
    ]

    // Our first form without any data will be cloned and save:
    let one_from_template = $('div.one-form').clone()

    // Function from Django site. Lets to send data not from form only. It generates a csrf_token
    function getCookies(name) {
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

    function add_new_answers(question, current_answers_count, container, count_of_fields, initial=null) {

        for (let i = 1; i <= count_of_fields; i++) {

            let new_one_field_div = $('<div>').addClass('one-field').attr('answer', current_answers_count + i);

            let new_label_for_answer_input = $('<label>').attr('for', current_answers_count + i).text(`Ответ №${current_answers_count + i}:`).prop('required', true).css({
                'display': 'flex',
                'flex-direction': 'row',
                'align-items': 'center',
                'justify-content': 'space-between'
            });


            let new_input_for_answer = $('<input>').addClass('form-control').attr('name', current_answers_count + i);
            if (initial != null) {
                new_input_for_answer.val(initial[i-1])
            }

            let new_icon_for_answer = $('<svg class="delete-icon" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"><path fill="currentColor" d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"/></svg>')

            new_label_for_answer_input.append(new_icon_for_answer);
            new_one_field_div.append(new_label_for_answer_input);
            new_one_field_div.append(new_input_for_answer)

            container.append(new_one_field_div)
        }

        formAnswers[question]['answers'] += count_of_fields
    }

    // Function is used when user click on "Создать" main button in our modal window:
    $('div.modal-content').on('click', 'div.modal-footer > button.send-form-btn', function () {
        console.log('button click was')
        let forms_data = [{}];
        let all_forms = $('div.modal-body').find('form.add-question-ajax-modal-form').length

        // We get all forms with specified class and for each form in loop:
        $('div.modal-body').find('form.add-question-ajax-modal-form').each(function (index, form) {
            // Getting the question number from parent for form div element with class <<one-form>>:
            let question_number = parseInt($(form).closest('div.one-form').attr('question'))
            // Getting the data from form as a serialize array. It contains the name and value as pair:
            let serialize_array_data = $(form).serializeArray()

            // Making the result dict for our needs:
            let current_form_data_dict = {}
            // List for saving answers as a simple list object:
            let answers = []

            // In the "foreach" loop for serialize data array getting the field by field and work with them:
            serialize_array_data.forEach(function (field) {
                // If the field.name is type or question, we add it as our result dictionary key and value:
                if (field.name === 'type' || field.name === 'question') {
                    // Если это "type" или "question", добавляем в formDataObject
                    current_form_data_dict[field.name] = field.value;
                } else { // In another case, it is an answer instance with number as filed.name and answer title as field.value:
                    // We need to save only the value and we push it into the answers list:
                    answers.push(field.value);
                }
            });

            // And our answer list into the result dictionary:
            current_form_data_dict['answers'] = answers

            // Add our result dictionary with data from current form into the main result dictionary with all forms by question number as a key:
            forms_data[question_number] = current_form_data_dict

            // Only for DEBUG:
            // console.log(`Data from question_form ${question_number} by MY_SELF - `, current_form_data_dict)
            console.log(forms_data)
        })

        // Create the ajax post request to the '/add_question_ajax/' view - it is the simple view class with post method:
        $.ajax({
            type: 'post',
            url: '/add_question_ajax/',
            headers: {'X-CSRFToken': getCookies('csrftoken')},
            dataType: 'json',
            data: JSON.stringify(forms_data),
            success: function (response) {
                console.log('ok - ', response);
                $('.alert-danger').text('').addClass('d-none')
                $('.alert-success').text(response.ok).removeClass('d-none')
                setTimeout(() => window.location.reload(), 2000)
            },
            error: function (response) {
                console.log('error - ', response);
                if (response.status === 400) {
                    $('.alert-success').text('').addClass('d-none')
                    $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
                }
            }
        });

    });

    $('div.modal-dialog').on('click', 'svg.delete-icon', function () {

        // Getting the question form instance:
        const current_question_form = $(this).closest('div.one-form')
        // Getting the answer container for deleting:
        let answer_div_container = $(this).closest('div.one-field[answer]')

        // We need to know the div.one-field answer attribute to know the number of deleting answer field:
        const answer_number_for_deleting = parseInt($(answer_div_container).attr('answer'));
        // Also we need to find the question number where we delete the answer instance:
        const question_form_number = parseInt($(current_question_form).attr('question'));

        // Delete current answer div with input and label in it:
        console.log('element to remove - ', answer_div_container)
        answer_div_container.remove()

        // Decrease the answers count for current question:
        formAnswers[question_form_number]['answers'] -= 1;
        // let new_icon_for_answer = $('<svg class="delete-icon" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"><path fill="currentColor" d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"/></svg>')
        // Now we need to find all other answers for current question and make the label count and div count -1:
        current_question_form.find('div.one-field[answer]').each(function (index, container) {


            $(container).attr('answer', index + 1)
            let label = $(container).find('label')
            label.attr('for', index + 1)
            label.text(`Ответ №${index + 1}`)
            label.append('<svg class="delete-icon" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24"><path fill="currentColor" d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"></path></svg>')
            $(container).find('input').attr('name', index + 1)
        })
    })


    // Привязываем обработчик к родительскому элементу, используя делегирование.
    // We need to this because when we clone the form our jsFile does not know about the new instances of our buttons with the same class.
    // That is whe we specify the parent element which is const (our modal body) ans whe makes the onClick event for our buttons to add new answer:
    $('div.modal-body').on('click', 'button.add-new-answer-btn', function () {
        // We need to know, the div.one-form question attribute
        const question_form_number = parseInt($(this).closest('div.one-form').attr('question'));
        console.log('add new answer')
        // We can do this because the value in div.one-form question attribute is the
        // formAnswers[question_form_number]['answers'] += 1;
        let answers_count = formAnswers[question_form_number]['answers'];
        console.log('Count of answers - ', answers_count)
        console.log('Our main variable - ', formAnswers[question_form_number])

        // Existing in our form div block which is used like a container for our new inputs for answers:
        let form_answers_container = $(this).next();
        console.log('Container in normal button -', form_answers_container)

        add_new_answers(question_form_number, answers_count, form_answers_container, 1)
    });


    $('div.modal').on('change', 'div.form-check.form-switch input.form-check-input', function() {
        const def_answers = ['За', 'Против', 'Воздержался']
        const question_form_number = parseInt($(this).closest('div.one-form').attr('question'));
        let current_answers_count = formAnswers[question_form_number]['answers']
        let container = $(this).parent().next().next()
        console.log('Container in switch - ', container)

        if ($(this).prop('checked')) {
            add_new_answers(question_form_number, current_answers_count, container, 3, def_answers)
        } else {
            let count = container.find('div.one-field').length
            container.empty()
            formAnswers[question_form_number]['answers'] -= count

        }
    })

// Method works when user clicks on button "Добавить вопрос":
    $('button.add-new-question-btn').on('click', function () {
        // We need to do:
        // 1 - create new form instance
        // 2 - in new instance update question attribute = previous_value + 1
        // 3 - add the record of new instance in our formAnswers list with dictionaries
        // 4 - add new form instance into the modal html

        // Make the copy of first form template
        let new_form_instance = one_from_template.clone()

        let last_question_from_number = formAnswers[formAnswers.length - 1]['question_form']
        let new_question_form_number = last_question_from_number + 1

        formAnswers.push({'question_form': new_question_form_number, 'answers': 0})
        new_form_instance.attr('question', new_question_form_number)

        $('div.modal-body').children(':last').after(new_form_instance)
    });

    // function check_answers_count() {
    //     let flag = true
    //     console.log('hello', formAnswers)
    //     for (let i = 0; i < formAnswers.length; i++) {
    //         if (formAnswers[i]['answers'] === 0) {
    //             flag = false
    //             break;
    //         }
    //     }
    //     // $.each(formAnswers, function(key, value) {
    //     //     if (value === 0) {
    //     //         flag = false;
    //     //         return flag;
    //     //     }
    //     // });
    //
    //     if (!flag) {
    //         console.log('button should be disable')
    //         $('#send-data').attr('disabled');
    //     }
    //     else {
    //         console.log('button should be active')
    //         $('#send-data').removeAttr('disabled')
    //     }
    // }
});



