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

    // Function is used when user click on "Создать" main button in our modal window:
    $('#send-data-modal').on('click', function () {
        let forms_data = [{}];

        // We get all forms with specified class and for each form in loop:
        $('form.add-question-ajax-modal-form').each(function (index, form) {
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
                setTimeout(()=>window.location.reload(), 2000)
            },
            error: function (response) {
                console.log('error - ', response);
                if (response.status === 400) {
                    $('.alert-success').text('').addClass('d-none')
                    $('.alert-danger').text(response.error).removeClass('d-none')
                }
            }
        });

    });


    // Привязываем обработчик к родительскому элементу, используя делегирование.
    // We need to this because when we clone the form our jsFile does not know about the new instances of our buttons with the same class.
    // That is whe we specify the parent element which is const (our modal body) ans whe makes the onClick event for our buttons to add new answer:
    $('div.modal-body').on('click', 'button.add-new-answer-btn', function () {
        // We need to know, the div.one-form question attribute
        const question_form_number = parseInt($(this).closest('div.one-form').attr('question'));
        console.log('add new answer')
        // We can do this because the value in div.one-form question attribute is the
        formAnswers[question_form_number ]['answers'] += 1;
        let answers_count = formAnswers[question_form_number]['answers'];


        // Existing in our form div block which is used like a container for our new inputs for answers:
        let form_answers_container = $(this).next();

        // Create new div element with class <<one-field>> as a container for input and label:
        let new_one_field_div = $('<div>').addClass('one-field').attr('answer', answers_count);

        // Create the label and input elements. Input element should contain name, label should contain for with the same value as name for input:
        let new_label_for_answer_input = $('<label>').attr('for', answers_count).text(`Ответ ${answers_count}:`).
        prop('required', true).css ({
            'display': 'flex',
            'flex-direction': 'row',
            'align-items': 'center',
            'justify-content': 'space-between'
        });
        let new_input_for_answer = $('<input>').addClass('form-control').attr('name', answers_count);
        let new_icon_for_answer = $('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"/></svg>')

        // Adding label and input into the new <<one-fild>> div container:
        new_label_for_answer_input.append(new_icon_for_answer)
        new_one_field_div.append(new_label_for_answer_input);
        new_one_field_div.append(new_input_for_answer);

        // Adding the new div.one-field container into the main container for answers:
        form_answers_container.append(new_one_field_div);
        // check_answers_count();
    });


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



