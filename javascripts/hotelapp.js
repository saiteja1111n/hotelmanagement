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
    var datak = {
        "name":document.getElementById("name").value,
        "phno":document.getElementById("phno").value,
        "address":document.getElementById("address").value
    };
    var json_Data = JSON.stringify(datak);
    console.log(json_Data);
    $.post("/createprofile",json_Data)
    .done(function(){
        return true;
    })
    .fail(function(){
        console.log("please try again");
        return false;
    });
 }