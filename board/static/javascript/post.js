let registerbtn = document.querySelector('.register-btn');

registerbtn.addEventListener('click', e => {
    let comment = document.querySelector('.comment-write').value;
    let param = {
        'comment-write': comment
    }
    $.ajax({
        url : '{% url "board:post" %}',
        type: 'POST',
        headers:{
            'X-CSRFTOKEN' : '{{csrf-token}}'
        },
        data: JSON.stringify(param),
        success:function(data){
            console.log(data);
        }
    });
});
