/*------------create dropdowns---------------*/
function dropDownInteractivity() {

    var acc = document.getElementsByClassName('accordion');
    var i;

    for (i = 0; i < acc.length; i++) {
        acc[i].onclick = function() {
            this.classList.toggle('active');
            this.nextElementSibling.classList.toggle('show');
        }
    }
}

dropDownInteractivity();

/*------------------Populate dropdowns---------------------*/
function populateResults(data) {
    console.log(data);
    $.ajax({
        type: 'POST',
        url: '/getResults',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            var data = response["result"];
            localStorage.setItem("mealPlan", data);
            $("#bars").remove();



            $("#main").append('<div id = "bars"><div class="col-md-3">' +
                '<button class="accordion"></button>' +
                '<div class="panel" id="panel1"><p></p></div><button class="accordion"></button><div class="panel" id="panel2">' +
                '<p></p></div></div><div class="col-md-3"><button class="accordion"></button><div class="panel" id="panel3">' +
                '<p></p></div><button class="accordion"></button><div class="panel" id="panel4"><p></p></div></div>' +
                '<div class="col-md-3"><button class="accordion"></button><div class="panel" id="panel5"><p></p></div>' +
                '<button class="accordion"></button><div class="panel" id="panel6"><p></p></div></div>' +
                '<div class="col-md-3"><button class="accordion"></button><div class="panel" id="panel7"><p></p></div>' +
                '<button class="accordion"></button><div class="panel" id="panel8"><p></p></div></div></div>')
            for (var i = 0; i < 8; i++) {
                console.log(data[i]);
                for (var j = 0; j < data[i]["meal_plan"].length; j++) {
                    $("#panel" + (i + 1) + " p").append(data[i]["meal_plan"][j] + "<br>");
                }
            }

            dropDownInteractivity();
            $('.accordion').each(function(index) {
                var i = (index % 4) + 1;
                console.log(i)
                this.style["background-image"] = "url('/static/img/drop_down_" + i + ".png')";
                //this.css("background-image", "url('../img/drop_down_" + index + ".png')")
            });

        }
    });
}


function populateDropdown() {
    var data = localStorage.mealPlan;
    for (var i = 0; i < 8; i++) {
        console.log(data[i]);
        for (var j = 0; j < data[i]["meal_plan"].length; j++) {
            $("#panel" + (i + 1) + " p").append(data[i]["meal_plan"][j] + "\n");
        }
    }
}
/*----------------get user input-------------------------*/
var data = {}
data["restrictions"] = [];
data["feelings"] = [];
data['activity'] = "moderate";
var restriction_ids = ["gluten", "wheat", 'soybeans', "peanuts", "dairy", "shellfish", "milk", "eggs", "tree_nut"]
$(document).on('click', '.dropdown-menu li a', function() {
    console.log($(this).text());
    data['activity'] = $(this).text();
});

function getUserInput() {
    //data['username'] = username;
    data['weight'] = $('#weight').val();
    data['height_ft'] = $('#height_ft').val();
    data['height_in'] = $('#height_in').val();
    data['age'] = $('#age').val();
    data['gender'] = $('#gender').val();
    for (var i = 0; i < restriction_ids.length; i++) {
        if ($("#" + restriction_ids[i]).is(':checked')) {
            data["restrictions"].push(restriction_ids[i]);
        }
    }
    return data;
}


$('#go').click(function() {
    console.log("go pressed")
    var data = getUserInput();
    populateResults(data);
});

function populateMealPlanResults() {
    $.ajax({
        type: 'POST',
        url: '/get_meal_plan_info',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            var data = response["result"];
            populateResults(data);
        }
    });
}
/*-----------------user----------------------*/
function createUser(username, password) {
    console.log("Username: " + username);
    console.log("password: " + password);
    $.ajax({
        type: 'POST',
        url: '/createaccount',
        data: JSON.stringify({ "username": username, "password": password }),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            console.log('in ajax create user');
            console.log(response);
            alert(response);

        }
    });
}

function login(username, password) {
    $.ajax({
        type: 'POST',
        url: '/login',
        data: JSON.stringify({ "username": username, "password": password }),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            console.log('in ajax login user');
            console.log(response);
            alert(response);
        }
    });

}

/*-----------------------journal---------------------*/

var feelings_ids = ["happy", "content", "neutral", "excited", "angry", "frustrated", "sick", "sad", "disappointed"];

feelings_ids.map(function(id) {
    $("#" + id).click(function() {
        console.log($("#" + id));
        var val = $("#" + id).attr("value");
        console.log(val);
        $("#" + id).attr("value", -1 * parseInt(val));
    });
})

function feelingsToArray() {
    var data = [];
    for (var i = 0; i < feelings_ids.length; i++) {
        if (parseInt($("#" + feelings_ids[i]).attr("value")) > 0) {
            data.push(feelings_ids[i]);
        }
    }
    return data;
}

function enterFeelings() {
    var feelingsArray = feelingsToArray();
    var notes = $("#notes").val();
    var food = $("#food").val();
    console.log("feelings array: ");
    console.log(feelingsArray);
    $.ajax({
        type: 'POST',
        url: '/writeEmotions',
        data: JSON.stringify({ "emotions": feelingsArray, "notes": notes, "food": food }),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            console.log("Success");
        }
    });
}


function getCalendar() {
    //calendar(11);

    $.ajax({
        type: 'GET',
        url: '/getCalendar',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
            console.log(response);
            var data = response["result"];
            console.log(data);

            var table = $('<table></table>').addClass('foo');
            for (var date in data) {
                console.log("date: " + date);
                for (var i = 0; i < data[date].length; i++) {
                    if (data[date][i]["emotions"][0]!=null) {
                        var img = "<img src='/static/img/" + data[date][i]["emotions"][0] + ".png'>";
                    } else {
                        var img = ""; }
                    var row = $('<tr></tr>').addClass('bar').html("Food: " + data[date][i]["food"] + ", " + date.toString() + img);
                    table.append(row);
                }
            }

            $('#calendar').append(table);
        }
    });

}




function calendar(month) {

    //Variables to be used later.  Place holders right now.
    var padding = "";
    var totalFeb = "";
    var i = 1;
    var testing = "";

    var current = new Date();
    var cmonth = current.getMonth(); // current (today) month
    var day = current.getDate();
    var year = current.getFullYear();
    var tempMonth = month + 1; //+1; //Used to match up the current month with the correct start date.
    var prevMonth = month - 1;

    //Determing if Feb has 28 or 29 days in it.  
    if (month == 1) {
        if ((year % 100 !== 0) && (year % 4 === 0) || (year % 400 === 0)) {
            totalFeb = 29;
        } else {
            totalFeb = 28;
        }
    }

    // Setting up arrays for the name of the months, days, and the number of days in the month.
    var monthNames = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"];
    var dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thrusday", "Friday", "Saturday"];
    var totalDays = ["31", "" + totalFeb + "", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"];

    // Temp values to get the number of days in current month, and previous month. Also getting the day of the week.
    var tempDate = new Date(tempMonth + ' 1 ,' + year);
    var tempweekday = tempDate.getDay();
    var tempweekday2 = tempweekday;
    var dayAmount = totalDays[month];

    // After getting the first day of the week for the month, padding the other days for that week with the previous months days.  IE, if the first day of the week is on a Thursday, then this fills in Sun - Wed with the last months dates, counting down from the last day on Wed, until Sunday.
    while (tempweekday > 0) {
        padding += "<td class='premonth'></td>";
        //preAmount++;
        tempweekday--;
    }
    // Filling in the calendar with the current month days in the correct location along.
    while (i <= dayAmount) {

        // Determining when to start a new row
        if (tempweekday2 > 6) {
            tempweekday2 = 0;
            padding += "</tr><tr>";
        }

        // checking to see if i is equal to the current day, if so then we are making the color of that cell a different color using CSS. Also adding a rollover effect to highlight the day the user rolls over. This loop creates the actual calendar that is displayed.
        if (i == day && month == cmonth) {
            padding += "<td class='currentday'  onMouseOver='this.style.background=\"#00FF00\"; this.style.color=\"#FFFFFF\"' onMouseOut='this.style.background=\"#FFFFFF\"; this.style.color=\"#00FF00\"'>" + i + "</td>";
        } else {
            padding += "<td class='currentmonth' onMouseOver='this.style.background=\"#00FF00\"' onMouseOut='this.style.background=\"#FFFFFF\"'>" + i + "</td>";
        }
        tempweekday2++;
        i++;
    }


    // Outputing the calendar onto the site.  Also, putting in the month name and days of the week.
    var calendarTable = "<table class='calendar'> <tr class='currentmonth'><th colspan='7'>" + monthNames[month] + " " + year + "</th></tr>";
    calendarTable += "<tr class='weekdays'>  <td>Sun</td>  <td>Mon</td> <td>Tues</td> <td>Wed</td> <td>Thurs</td> <td>Fri</td> <td>Sat</td> </tr>";
    calendarTable += "<tr>";
    calendarTable += padding;
    calendarTable += "</tr></table>";
    console.log(calendarTable);
    $("#calendar").html(calendarTable);
}
