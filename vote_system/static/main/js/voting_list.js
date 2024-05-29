$('svg#make-card-view').on('click', function(){
    $('div#votes-container').attr('class', 'votes-container-cards');
})

$('svg#make-list-view').on('click', function(){
    $('div#votes-container').attr('class', 'votes-container-classic');
})