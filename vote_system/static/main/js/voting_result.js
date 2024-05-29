$('button.more-info').on('click', function(){
    let next_container = $(this).next();

    if ($(next_container).css('display') === 'none') {
        $(next_container).removeAttr('style');
        $(this).text('Подробней ▼');
    }
    else{
        $(next_container).css({'display': 'none'});
        $(this).text('Подробней ▲');
    }
})