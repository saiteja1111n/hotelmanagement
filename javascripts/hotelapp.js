function getaroom(){

			}
function addrooms(){
    var objectData =
    {
        numberofrooms: document.getElementById("roomno").value,
    };
    var data = JSON.stringify(objectData);
    $.post("/addroom",data)
    .done(function(data){
		//console.log("Success:" + data);
	});
	console.log("before room status");
	window.location="/login";
}

function removerooms() {
    var p=document.getElementById("roomno1").value;
    console.log(p);
    if( p.length==0){
        alert("you didnt submit any number to cancel");
    } else{
        var objectData =
        {
            rooms: document.getElementById("roomno1").value,
        };
        var data = JSON.stringify(objectData);
        $.post("/removeroom",data)
        .done(function(data){
            console.log("Success:" + data);
        });
        console.log("before room status");
        window.location="/login";
    }

}
function addaroom(){
      /*  var nelement1=document.createElement("INPUT");
        nelement1.setAttribute("type","text");
        nelement1.setAttribute("id","roomno");
        nelement1.setAttribute("placeholder","roomno");
        var s= document.getElementById("rooms");
        var nelement2=document.createElement("INPUT");
        nelement2.setAttribute("type","text");
        nelement2.setAttribute("id","roomno");
        nelement2.setAttribute("placeholder","room details");
        var s= document.getElementById("rooms");
        s.appendChild(nelement1);
        s.appendChild(nelement2);
        var nelement3=document.createElement("BUTTON");
        nelement3.setAttribute("value","Add room");
        nelement3.setAttribute("onClick","addroom1()");
        var s= document.getElementById("rooms");
        s.appendChild(nelement3);*/
        $('#rooms').append('<br>    <input id="roomno" type="text" placeholder="Room Number"><br><br><input id="roomdetails" placeholder="Room Detals" type="text"><br><br><button height="50px" width="50px" onClick="addroom1()" value="Add">');
}
function login() {
   window.location="/login";
}
function logout() {
    window.location="/logout";
}
function roomstatus() {
    var data1="";
    $.post("/getroomstatus")
    .done(function(data){
        console.log("succesfully updated");
        data1=JSON.parse(data);
        var s="<h1>Available Rooms</h1>";
        //console.log(data1);
        for(var i=0;i < data1.availablerooms.length;i++) {
            s=s+"<h5>"+data1.availablerooms[i].number+"</h5>";
        }
        document.getElementById("available").innerHTML=s;
        s="<h1>booked rooms</h1>"

        for(var i=0;i < data1.bookedrooms.length;i++) {
            s=s+"<h5>"+data1.bookedrooms[i].number+"</h5>";
        }
        document.getElementById("booked").innerHTML=s;
    });

}

function getname(){
    console.log("get name");
    $.post("/getname")
    .done(function(data){
        data=JSON.parse(data);
        document.getElementById("name").innerHTML=data.name;
    })
    .fail(function(){
        $.post("/getname")
        .done(function(data){
            data=JSON.parse(data);
            document.getElementById("name").innerHTML=data.name;
        })
        .fail(function(){
            alert("some thing went wrong please reload the page");
        });
    });
}

function saveprofile() {
    return true;
 }