// function for changing pictures in hotel home page
    $('.carousel').carousel({
        interval: 2000 //changes the speed
    })

    function check()
    {
            document.getElementById('model1btn').style.visibility = 'hidden';
            document.getElementById('proceed').style.visibility = 'visible';
            var divbar2=document.getElementById("selectType");
            divbar2.style.display='none';
            var divbar1=document.getElementById("ConfirmationPage");
            divbar1.style.display='none';
            var divbar11=document.getElementById("roomSelect");
            divbar11.style.display='block';
    }


    function makeVisible(id)
    {
        var divbar=document.getElementById(id);
        divbar.style.display='block';
         $('html,body').animate({
                scrollTop: $("#keepHidden1").offset().top
                },
                'slow'
          );
    }

    function dropdownSelected(type)
    {
        myElement = $("#payment");
        myElement.value = type+"";
    }


    $(".dropdown-menu li a").click(function(){
          var selText = $(this).text();
          $(this).parents('.dropdown').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');

    });

    function PaymentDone()
    {
        var divbar=document.getElementById("payment_Status_success");
        divbar.style.display='block';
    }

//fuction that gets the available rooms
    function get_Room()
    {
        var data1 = {};
        //get available rooms request
        $.post("/availablerooms")
        .done(function(data){
            console.log("success");
            data1 = JSON.parse(data);
            console.log(data1);
            var s="";
            console.log(data1);
            singlerooms = document.getElementById('available_single_rooms');
            $('#available_single_rooms').empty()
            for(var i=0;i<data1.single_rooms.length;i++) {
                singlerooms.options[singlerooms.options.length] = new Option("Room No: "+data1.single_rooms[i].number+" A/c:"+data1.single_rooms[i].acstatus+"  Rs."+data1.single_rooms[i].cost, data1.single_rooms[i].number);
            }
            $('#available_double_rooms').empty()
            doublerooms = document.getElementById('available_double_rooms');
            for(var i=0;i<data1.double_rooms.length;i++) {
                doublerooms.options[doublerooms.options.length] = new Option("Room No: "+data1.double_rooms[i].number+' A/c:'+data1.double_rooms[i].acstatus+'           Rs.'+data1.double_rooms[i].cost, data1.double_rooms[i].number);
            }
            $('#available_triple_rooms').empty()
            triplerooms = document.getElementById('available_triple_rooms');
            for(var i=0;i<data1.triple_rooms.length;i++) {
                triplerooms.options[triplerooms.options.length] = new Option("Room No: "+data1.triple_rooms[i].number+'           A/c:'+data1.triple_rooms[i].acstatus+'           Rs.'+data1.triple_rooms[i].cost, data1.triple_rooms[i].number);
            }
        });

        $('.modal-title').text('Room Availability');
        document.getElementById('confirm').style.visibility = 'hidden';
        document.getElementById('proceed').style.visibility = 'visible';
        document.getElementById('back').style.visibility = 'hidden';
        var divbar1=document.getElementById("model1");
        divbar1.style.display='block';
        var divbar1=document.getElementById("ConfirmationPage");
        divbar1.style.display='none';
        var divbar21=document.getElementById("personal_details");
        divbar21.style.display='none';
    }

    var rooms='';

    function proceed()
    {
        var start_date = document.getElementById("startdate");
        var end_date = document.getElementById("enddate");
        if(validate_dates(start_date.value,end_date.value)) {
            single_rooms = $("#available_single_rooms").val()
            double_rooms = $("#available_double_rooms").val()
            triple_rooms = $("#available_triple_rooms").val()
            s="";
            if(single_rooms!=null) {
                for(var i=0;i<single_rooms.length;i++)
                    s=s+single_rooms[i]+",";
            }
             if(double_rooms!=null) {
                for(var i=0;i<double_rooms.length;i++)
                    s=s+double_rooms[i]+",";
             }
             if(triple_rooms!=null) {
                for(var i=0;i<triple_rooms.length;i++)
                    if((i+1)==triple_rooms.length)
                        s=s+triple_rooms[i];
                    else
                        s=s+triple_rooms[i]+",";
             }
             rooms=s;
             if(s!="") {
                document.getElementById("allrooms").innerHTML=s;
                var divbar12=document.getElementById("model1");
                divbar12.style.display='none';

                var divbar1=document.getElementById("ConfirmationPage");
                divbar1.style.display='none';

                var divbar21=document.getElementById("personal_details");
                divbar21.style.display='block';

                document.getElementById('proceed').style.visibility = 'hidden';
                document.getElementById('back').style.visibility = 'visible';
                document.getElementById('confirm').style.visibility = 'visible';

                $('.modal-title').text('Personal Details');
             }
             else {
                alert("please select atleast one room");
             }
        } else {
            start_date.focus();
        }
    }
    function ConfirmationDone()
    {
        console.log("Rooms booked"+rooms);
        var name = document.getElementById("person_name").value;
        var email = document.getElementById("person_email");
        var mobileno = document.getElementById("person_mobileno");
        var start_date = document.getElementById("startdate").value;
        var end_date = document.getElementById("enddate").value;
        if(validate_email(email)&&validate_mobile(mobileno)){
            var data1 = {
                'booked_rooms':rooms,
                'person_name':document.getElementById("person_name").value,
                'person_email':document.getElementById("person_email").value,
                'person_mobileno':document.getElementById("person_mobileno").value,
                'start_date':document.getElementById("startdate").value,
                'end_date':document.getElementById("enddate").value,
            };
            var data = JSON.stringify(data1);
            $.post("/conformrequest",data)
            .done(function(data){
                console.log("success");
                console.log(data);
                document.getElementById('back').style.visibility = 'hidden';
                $('.modal-title').text('Room Booked');
                document.getElementById('confirm').style.visibility = 'hidden';

                var divbar1=document.getElementById("ConfirmationPage");
                divbar1.style.display='block';

                var divbar=document.getElementById("model1");
                divbar.style.display='none';

                var divbar21=document.getElementById("personal_details");
                divbar21.style.display='none';
            });
        }
    }

    $(document).ready(function() {
        $('#example-getting-started').multiselect();
    });

    function feedback()
    {
        var rating = document.getElementById("user_rating");

        var name=document.getElementById("name").value;

        var email=document.getElementById("email");

        var msg=document.getElementById("msg").value;

        var phone = document.getElementById("phone");

        if(!(rating.value.match(/^[0-5]([.][0-9]+)?$/))){
            alert("Give valid rating");
            rating.focus();
            return;
        }
         var x=parseFloat(rating.value);
        if(!(0<=x<=5)){
                alert("Give valid rating");
                rating.focus();
                return;
        }
        if(name=""){
            alert("Please fill the Name Field");
        }
        if(validate_email(email)&&validate_mobile(phone)) {

            data = {
                'rating':rating.value,
                'name':name,
                'email':email.value,
                'msg':msg,
                'phone':phone.value,
            }

            data = JSON.stringify(data)
            $.post("/feedback",data)
            .done(function(data){
                console.log("success");
                console.log(data);
                alert("Feedback Successfully submitted");
                window.location.assign("/.");

            });
        }
    }

//    function bookRoom(x,y){
//        data={
//            'roomno':x,
//            'customer_name'y,
//        }
//        data = JSON.stringify(data);
//        $.post("/confirm_rm",data)
//        .done(function(data){
//            console.log("success");
//            console.log(data);
//            alert("Feedback Successfully submitted");
//            window.location.assign("/.");
//
//        });
//    }

    function validate_mobile(fld) {
         if (fld.value == "") {
          alert("You didn't enter a phone number.");
          fld.value = "";
          fld.focus();
          return false;
         }
          else if (isNaN(fld.value)) {
          alert("The phone number contains illegal characters.");
          fld.value = "";
          fld.focus();
          return false;
         }
         else if (!(fld.value.length == 10)) {
          alert("The phone number is the wrong length. \nPlease enter 10 digit mobile no.");
          fld.value = "";
          fld.focus();
          return false;
         }
         else
           return true;
    }

    function validate_email(tbEMObj) {
        with (tbEMObj) {
            apos = value.indexOf("@");
            dotpos = value.lastIndexOf(".");
            if (value == '') {
                alert('field can not be blank');
                tbEMObj.focus()
                return false;
            }
            else if (apos < 1 || dotpos - apos < 2) {
                alert('please enter correct email');
                tbEMObj.focus()
                return false;
            }
        }
        return true;
    }

    function validate_dates(x,y) {
        var date = x.substring(0, 2);
        var month = x.substring(3, 5);
        var year = x.substring(6, 10);
        var date1 = y.substring(0, 2);
        var month1 = y.substring(3, 5);
        var year1 = y.substring(6, 10);
        var startdate = new Date(x);
        var enddate= new Date(y);
        var currentDate = new Date();
        if(currentDate>=startdate) {
            alert("The start date should be after the current date");
            return false;
        } else if(enddate<=startdate) {
            alert("The end date should be after startdate");
            return false;
        }
        return true;
    }