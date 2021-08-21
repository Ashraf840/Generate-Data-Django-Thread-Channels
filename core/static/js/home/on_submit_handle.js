// alert('Hellow!')

var input_field = document.getElementById('input_field');
var submit_btn = document.getElementById('submit_btn');


// Input-field enter-btn press
input_field.onkeypress = function (event) {
    if (event.keyCode == 13) {
        axiosPost();
    }
}

// Submit btn click
submit_btn.onclick = function (e) {
    axiosPost();
}

// Call the API to start populating Dummy Data
function axiosPost () {
    var input_value = input_field.value;
    var url = 'http://127.0.0.1:8080/students/api/create_dummy_student_data/';

    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';

    let data = new FormData();  // easy to pass key-value pair along with the url in 'axios.posy'
    data.append("total", input_value);

    axios.post(url, data)
    .then(res => {
        console.log(res.data);
    })
    .catch(errors => console.log(errors))
}
