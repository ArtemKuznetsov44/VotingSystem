$(window).on('beforeunload', function (event) {

    let checked_users_id = []

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


    console.log('Мы пытаемся покинуть страницу');
    $('div.super-container').find('div.one-instance-card div.card-time input').each(function (index, input) {
        // console.log($(input).attr('number'));


        if ($(input).prop('checked')) {
            checked_users_id.push(($(input).attr('number')));
        }

        // checked_users_id.push(3);
        // checked_users_id.push(2);


    });

    if (checked_users_id.length > 0) {
            $.ajax({
                type: 'post',
                url: '/users/all-users/',
                headers: {'X-CSRFToken': getCookies('csrftoken')},
                dataType: 'json',
                data: {'checked_users': checked_users_id},
                success: function (response) {
                    console.log('ok - ', response);
                    // $('.alert-danger').text('').addClass('d-none')
                    // $('.alert-success').text(response.ok).removeClass('d-none')
                    // setTimeout(() => window.location.reload(), 2000)
                },
                error: function (response) {
                    console.log('error - ', response);
                    // if (response.status === 400) {
                    //     $('.alert-success').text('').addClass('d-none')
                    //     $('.alert-danger').text(response.responseJSON.error).removeClass('d-none')
                    // }
                }
            });
        }


})