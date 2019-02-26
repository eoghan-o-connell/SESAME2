(function() {

    var user_type;
    var user_form;
    var researcher_form;
    var res_req;
    var reviewer_form;
    var funder_form;
    var current;
    var organisation;
    var field;
    var passowrd1;
    var password2;
    var no_match;
    var reg;

    document.addEventListener('DOMContentLoaded', init, false);

    function init() {
        researcher_form = document.getElementById('researcher_form');
        reviewer_form = document.getElementById('reviewer_form');
        funder_form = document.getElementById('funder_form');
        user_form = document.getElementsByClassName('user_form');
        res_req = document.getElementsByClassName('res_req')
        organisation = document.getElementById('organisation');
        field = document.getElementById('field');
        user_type = document.getElementById('user_type');
        password1 = document.getElementById('password1');
        password2 = document.getElementById('password2');
        no_match = document.getElementById('no_match');
        reg = document.getElementById('reg');
        user_type.addEventListener("change", change_type);
        password1.addEventListener("change", password_match);
        password2.addEventListener("change", password_match);
        reg.addEventListener("submit", function(){submit(event);});
    }

    function submit(event){
        if (password1.value !== password2.value){
            event.preventDefault();
            no_match.hidden = false;
        }
    }

    function password_match(){
        no_match.hidden = ((password1.value === password2.value) || password2.value === "");
    }

    function change_type(){

        for (var i=0;i<user_form.length;i++){
            user_form[i].hidden = false;
        }

        if (current != null){
            current.hidden = true;
        }
        switch(user_type.options[user_type.selectedIndex].value){
            case "researcher":
                res_req_change(true);
                current = researcher_form;
                field.required = false;
                organisation.required = false;
                break;
            case "reviewer":
                res_req_change(false);
                current = reviewer_form;
                field.required = true;
                organisation.required = false;
                break;
            case "funder":
                res_req_change(false);
                current = funder_form;
                field.required = false;
                organisation.required = true;
                break;
        }
        current.hidden = false;
    }

    function res_req_change(required){
        for (var i=0;i<res_req.length;i++){
            res_req[i].required = required;
        }
    }

})();
