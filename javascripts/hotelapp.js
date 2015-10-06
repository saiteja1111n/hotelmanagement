function getaroom(){

			}
function login() {
   window.location="/login";
}
function logout() {
    window.location="/logout";
}


function getname(){
    console.log("get name");
    $.post("/getname")
    .done(function(data){
        data=JSON.parse(data);
        document.getElementById("name").innerHTML=data.name;
    })
    .fail(function(data){
        alert("some thing went wrong please reload the page");
    });
}

function saveprofile1() {
    return false;
 }