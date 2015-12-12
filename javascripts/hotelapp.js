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
        $.post("/confirmrequest",data)
        .done(function(data){
            console.log("Success:" + data);
        });
        console.log("before room status");
        window.location="/login";
    }

}
function getaroom(){
    var p=document.getElementById("roomno").value;
    console.log(p);
    if( p.length==0){
        alert("you didnt submit any number to cancel");
    } else{
        var objectData =
        {
            rooms: document.getElementById("roomno").value,
        };
        var data = JSON.stringify(objectData);
        $.post("/bookroom",data)
        .done(function(data){
            console.log("Success:" + data);
        });
        console.log("before room status");
        window.location="/login";
    }

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
        console.log(data);
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

function cancelrooms(){
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
        $.post("/cancelrooms",data)
        .done(function(data){
            console.log("Success:" + data);
        });
        console.log("before room status");
        window.location="/login";
    }

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