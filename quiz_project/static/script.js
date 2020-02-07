check_quiz_name = function(value){
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajax({
        url: '/quizzes/check/' + value,
        type: 'POST',
        success: function(data){
            if (!data['available']) {
            $('input[name ="quiz_name"]')[0].style.boxShadow = "0 0 2px 1px rgba(245, 0, 0, 0.7), 0 2px 2px 0 rgba(245, 0, 0, 0.7)";
            document.getElementById('error-message').text = "Quiz name is already taken!"; }
            if(data['available']) {
            $('input[name ="quiz_name"]')[0].style.boxShadow = "0 0 2px 1px rgba(0, 180, 0, 0.7), 0 2px 2px 0 rgba(0, 180, 0, 0.7)";
            document.getElementById('error-message').text = "";}
            },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
        },
        dataType: 'json',
    });
}

check_name = function(value){
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    data = {check_username: value};
    $.ajax({
        url: '/users/register/',
        type: 'POST',
        data: data,
        success: function(data){
            if (!data['name_available']) {
            $('input[name ="username"]')[0].style.boxShadow = "0 0 2px 1px rgba(245, 0, 0, 0.7), 0 2px 2px 0 rgba(245, 0, 0, 0.7)";
            document.getElementById('error-message').text = "Username is already taken!"; }
            if(data['name_available']) {
            $('input[name ="username"]')[0].style.boxShadow = "0 0 2px 1px rgba(0, 180, 0, 0.7), 0 2px 2px 0 rgba(0, 180, 0, 0.7)";
            document.getElementById('error-message').text = "";}
            },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
        },
        dataType: 'json',
    });
}

check_email = function(value){
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    data = {check_mail: value};
    $.ajax({
        url: '/users/register/',
        type: 'POST',
        data: data,
        success: function(data){
            if (!data['mail_available']) {
            $('input[name ="email"]')[0].style.boxShadow = "0 0 2px 1px rgba(245, 0, 0, 0.7), " +
                                                           "0 2px 2px 0 rgba(245, 0, 0, 0.7)";
            document.getElementById('error-message').text = "Email is already taken!"; }
            if(data['mail_available']) {
            $('input[name ="email"]')[0].style.boxShadow = "0 0 2px 1px rgba(0, 180, 0, 0.7), " +
                                                           "0 2px 2px 0 rgba(0, 180, 0, 0.7)";
            document.getElementById('error-message').text = "";}
            },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
        },
        dataType: 'json',
    });
}


quiz_select = function() {
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var choice = document.getElementById("quizSelect").value;
    $('.selected').empty();
    if(choice == "users"){
        $.ajax({
            url: '/quizzes/get_users/',
            type: 'GET',
            success: function(data){
                quizzes = data['quizzes'];
                for(let i = 0; i < quizzes.length; i++){
                    $('.selected').append(get_usersHTML(quizzes[i]))
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
            },
            dataType: 'json',
        });
    }
    if(choice == "passed"){
        $.ajax({
            url: '/quizzes/get_passed/',
            type: 'GET',
            success: function(data){
                quizzes = data['quizzes'];
                for(let i = 0; i < quizzes.length; i++){
                    $('.selected').append(get_usersHTML(quizzes[i]))
                }
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
            },
            dataType: 'json',
        });
    }
}

get_usersHTML = function(quiz){
    var $res = $('<div class="quiz_box" style="max-width:480px;">' +
        '<div class="quiz_box_info_left">' +
            '<a style="font-size:23px;">' + quiz['name'] +'</a> <br>' +
            '<a style="font-size:11px;">' + quiz['date'].slice(0,10) + ' </a></div>' +
            '<div class="quiz_box_info_right" style="margin-right:15px;">' +
            '<a style="font-size:16px;">rate: ' + quiz['rate'] + '</a><br>' +
            '<a>average score: ' + quiz['avg_score'] + '</a>' +
            '<a>' + (quiz['user_score'] ? ( 'your score: ' + quiz['user_score']) :
            ('users passed: ' + quiz['passed_count'])) + ' </a></div>' +
            '<div class="quiz_box_info_right">' +
            '<button onclick="window.location=\'/quizzes/' + quiz['id'] + '\';">Retry</button><br>' +
            '<button onclick="window.location=\'/quizzes/' + quiz['id'] + '/comments\';">Comment</button></div>');
    return $res;
}


validate = function(){
        if($('input[name ="new_password"]')[0].value == $('input[name ="old_password"]')[0].value){
            $('input[name ="new_password"]')[0].style.boxShadow = "0 0 2px 1px rgba(245, 0, 0, 0.7), " +
                                                                  "0 2px 2px 0 rgba(245, 0, 0, 0.7)";
            document.getElementById('error-message').text = "you haven't changed pass!";
            }
        else {
            $('input[name ="new_password"]')[0].style.boxShadow = "";
            document.getElementById('error-message').text = "";
            }
        }

validate_repeat = function(){
        if($('input[name ="new_password"]')[0].value == $('input[name ="repeat_password"]')[0].value){
            let shadow = "0 0 2px 1px rgba(0, 180, 0, 0.7), 0 2px 2px 0 rgba(0, 180, 0, 0.7)";
            $('input[name ="new_password"]')[0].style.boxShadow = shadow;
            $('input[name ="repeat_password"]')[0].style.boxShadow = shadow;
            document.getElementById('error-message').text = "";
            }
        else {
            let shadow = "0 0 2px 1px rgba(245, 0, 0, 0.7), 0 2px 2px 0 rgba(245, 0, 0, 0.7)";
            $('input[name ="new_password"]')[0].style.boxShadow = shadow;
            $('input[name ="repeat_password"]')[0].style.boxShadow = shadow;
            document.getElementById('error-message').text = "passwords are not matching";
            }
}

delete_comment = function(rateId, form){
    let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    $.ajax({
        url: `${rateId}`,
        type: 'DELETE',
        success: function(data){
        if(data['deleted']){
            form.parentElement.parentElement.remove();
        }
        },
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", `${csrf_token}`);
        },
        dataType: 'json',
        });
}
