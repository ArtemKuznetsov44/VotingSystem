$(document).ready(function () {
    console.log("Function is active")
    function formatPhoneNumber(value) {

        return '+7-9' + value.slice(2, 4) + '-' + value.slice(4, 7) + '-' + value.slice(7, 9) + '-' + value.slice(9)
    }

    $('#id_phone').on('change', function () {

        console.log('Next function is working now!')
        let inputValue = $(this).val();

        // Deleting all non number/numeric values:
        let numericValue = inputValue.replace(/\D/g, '');


        let formattedValue = formatPhoneNumber(numericValue);

        $(this).val(formattedValue);
    })
});