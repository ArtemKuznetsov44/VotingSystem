function display_bulletin() {

}

function create_bulletin() {

}


/**
 * @param description_key {string} - Key for describe what to send;
 * @param data_to_send {dict|string} - Data for sending
*/
function send_data(description_key, data_to_send){
    voteSocket.send(JSON.stringify({description_key: data_to_send}))
}