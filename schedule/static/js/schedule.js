// Initialize activity data in JSON format
var activity_data = {
    "activities": []
};

(function($) {

	"use strict";

// Setup the calendar with the current date
$(document).ready(function(){
    load_activities(dataJSON);
    var date = new Date();
    var today = date.getDate();
    // Set click handlers for DOM elements
    $(".right-button").click({date: date}, next_year);
    $(".left-button").click({date: date}, prev_year);
    $(".month").click({date: date}, month_click);
    $("#add-button").click({date: date}, new_event);
    // $(".delete-btn").click(delete_activity);
    // Set current month as active
    $(".months-row").children().eq(date.getMonth()).addClass("active-month");
    init_calendar(date);
    // console.log("load actvity_data AFTER ajax 1: " + JSON.stringify(activity_data["activities"]));
    var activities = check_activities(today, date.getMonth()+1, date.getFullYear());
    show_activities(activities, months[date.getMonth()], today);
});

// Initialize the calendar by appending the HTML dates
function init_calendar(date) {
    console.log("init_calendar");
    // load_activities(dataJSON); uncomment
    $(".tbody").empty();
    $(".events-container").empty();
    var calendar_days = $(".tbody");
    var month = date.getMonth();
    var year = date.getFullYear();
    var day_count = days_in_month(month, year);
    var row = $("<tr class='table-row'></tr>");
    var today = date.getDate();
    // Set date to 1 to find the first day of the month
    date.setDate(1);
    var first_day = date.getDay();
    // 35+firstDay is the number of date elements to be added to the dates table
    // 35 is from (7 days in a week) * (up to 5 rows of dates in a month)
    for(var i=0; i<35+first_day; i++) {
        // Since some of the elements will be blank, 
        // need to calculate actual date from index
        var day = i-first_day+1;
        // If it is a sunday, make a new row
        if(i%7===0) {
            calendar_days.append(row);
            row = $("<tr class='table-row'></tr>");
        }
        // if current index isn't a day in this month, make it blank
        if(i < first_day || day > day_count) {
            var curr_date = $("<td class='table-date nil'>"+"</td>");
            row.append(curr_date);
        }   
        else {
            var curr_date = $("<td class='table-date'>"+day+"</td>");
            var events = check_activities(day, month+1, year);
            if(today===day && $(".active-date").length===0) {
                curr_date.addClass("active-date");
                show_activities(events, months[month], day);
            }
            // If this date has any events, style it with .event-date
            if(events.length!==0) {
                curr_date.addClass("event-date");
            }
            // Set onClick handler for clicking a date
            curr_date.click({events: events, month: months[month], day:day}, date_click);
            row.append(curr_date);
        }
    }
    // Append the last row and set the current year
    calendar_days.append(row);
    $(".year").text(year);
}

// Get the number of days in a given month/year
function days_in_month(month, year) {
    var monthStart = new Date(year, month, 1);
    var monthEnd = new Date(year, month + 1, 1);
    return (monthEnd - monthStart) / (1000 * 60 * 60 * 24);    
}

// Event handler for when a date is clicked
function date_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    $(".active-date").removeClass("active-date");
    $(this).addClass("active-date");
    show_activities(event.data.events, event.data.month, event.data.day);
};

// Event handler for when a month is clicked
function month_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    var date = event.data.date;
    $(".active-month").removeClass("active-month");
    $(this).addClass("active-month");
    var new_month = $(".month").index(this);
    date.setMonth(new_month);
    init_calendar(date);
}

// Event handler for when the year right-button is clicked
function next_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear()+1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

// Event handler for when the year left-button is clicked
function prev_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear()-1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

// Event handler for clicking the new event button
function new_event(event) {
    // if a date isn't selected then do nothing
    if($(".active-date").length===0)
        return;
    // remove red error input on click
    $("input").click(function(){
        $(this).removeClass("error-input");
    })
    // empty inputs and hide events
    $("#dialog input[type=text]").val('');
    $("#dialog input[type=time]").val('');
    $("#id_desc").val('');
    $(".events-container").hide(250);
    $("#dialog").show(250);
    // Event handler for cancel button
    $("#cancel-button").click(function() {
        $("#id_activity").removeClass("error-input");
        $("#id_start_time").removeClass("error-input");
        $("#id_end_time").removeClass("error-input");
        $("#id_type").removeClass("error-input");
        $("#id_desc").removeClass("error-input");
        $("#dialog").hide(250);
        $(".events-container").show(250);
    });
    // Event handler for ok button
    $("#ok-button").unbind().click({date: event.data.date}, function() {
        var date = event.data.date;
        var activity = $("#id_activity").val().trim();
        var start_time = $("#id_start_time").val().trim();
        var end_time = $("#id_end_time").val().trim();
        var day = parseInt($(".active-date").html());
        // Basic form validation
        if (activity.length === 0) {
            $("#id_activity").addClass("error-input");
        }
        else if (!validate_time(start_time)) {
            $("#id_start_time").addClass("error-input");
        }
        else if (!validate_time(end_time)) {
            $("#id_end_time").addClass("error-input");
        }
        else {
            $("#dialog").hide(250);
            console.log("new event");
            $("#id_year").val(date.getFullYear());
            $("#id_month").val(date.getMonth()+1);
            $("#id_day").val(day);
            $("#form").submit(function(e) {
                // preventing from page reload and default actions
                e.preventDefault();
                var serializedData = $(this).serialize();
                var csr = $("input[name=csrfmiddlewaretoken]").val();
                console.log("about to be submitted");
                    $.ajax({
                        type: 'POST',
                        url: '',
                        data: serializedData,
                        success: function (response) {
                            // alert('Form is submitted');
                            var instance = JSON.parse(response["activity"]);
                            var activity = instance[0]["fields"];
                            activity["id"] = instance[0]["pk"];  // add pk as this activity's id
                            activity["csr"] = csr;  // add pk as this activity's id
                            activity_data["activities"].push(activity);
                            //  clear the form
                            $("#form").trigger('reset');
                            console.log("success");
                            date.setDate(day);
                            init_calendar(date);
                        },
                        error: function (response) {
                            //  clear the form
                            $("#form").trigger('reset');
                            date.setDate(day);
                            init_calendar(date);
                        },
                        // complete: function (response) {
                        //     // load_activities(dataJSON);  uncomment
                        //     date.setDate(day);
                        //     init_calendar(date);
                        //     // console.log("load actvity_data AFTER ajax 4: " + JSON.stringify(activity_data));
                        // }
                    })
            })
        }
    });
}

function delete_activity(event) {
    var id = parseInt($(this).attr("data-sid"));
    var csr = $("input[name=csrfmiddlewaretoken").val();
    var date = new Date();
    var day;
    var month;
    var year;
    console.log(id);
    var action = confirm("Are you sure you want to delete this activity?");
    if (action != false) {
        $.ajax({
            url: url_delete,
            method: 'POST',
            data: {
                sid: id,
                csrfmiddlewaretoken: csr
            },
            success: function (data) {
                console.log(data);
                if (data.status == 1) {
                    for (var i = 0; i < activity_data["activities"].length; i++) {
                        if (activity_data["activities"][i]["id"] === id) {
                            day = activity_data["activities"][i]["day"]
                            month = activity_data["activities"][i]["month"]
                            year = activity_data["activities"][i]["year"]
                            activity_data["activities"].splice(i, 1)
                            console.log("deleted from activity_data")
                        }
                    }
                    // alert("Activity has been successfully deleted!");
                    // var date = event.data.date;
                    // var day = parseInt($(".active-date").html());
                    // date.setDate(day);
                    // init_calendar(date);
                    console.log(day + " " + month + " " + year)
                    date.setDate(day);
                    date.setMonth(month-1);
                    date.setFullYear(year);
                    init_calendar(date);
                    // var activities = check_activities(day, month, year)
                    // show_activities(activities, month, day);
                }
            }
        });
    }
}

function load_activities(data) {
    activity_data = {
        "activities": []
    };

    for (var key in data) {
        var activity = data[key]["fields"];
        activity["id"] = data[key]["pk"];
        activity_data["activities"].push(activity);
    }
}

// Display all events of the selected date in card views
function show_activities(activities, month, day) {
    console.log("show_activities");
    console.log(activities);
    // activity_data = {
    //     "activities": []
    // };
    // load_activities(dataJSON); uncomment
    // console.log("load actvity_data AFTER ajax 3: " + JSON.stringify(activity_data));

    // Clear the dates container
    $(".events-container").empty();
    $(".events-container").show(250);
    // If there are no events for this date, notify the user
    if(activities.length===0) {
        var activity_card = $("<div class='event-card'></div>");
        var activity_title = $("<div class='event-name' style='font-size: 14px;'>There are no activities planned for "+month+" "+day+".</div>");
        // $(activity_card).css({ "border-left": "10px solid #FF1744" });
        $(activity_card).append(activity_title);
        $(".events-container").append(activity_card);
    }
    else {
        activities.sort(function (a, b) {
            return a["start_time"].localeCompare(b["start_time"]);
        });

        // Go through and add each event as a card to the events container
        for(var i=0; i<activities.length; i++) {
            var as_button = $("<a class='clickable-card' data-bs-toggle='collapse' href='.multi-collapse' role='button' aria-expanded='false' aria-controls='"+activities[i]["id"]+"1 "+activities[i]["id"]+"2'/>")
            var activity_card = $("<div class='event-card'></div>");
            var row_container = $("<div class='row'></div>")
            var col_container = $("<div class='col'></div>")
            var activity_time = $("<div class='event-time row'>"+activities[i]["start_time"].slice(0, 5)+" - "+activities[i]["end_time"].slice(0,5)+"</div>");
            var activity_title = $("<div class='event-name row'><strong>"+activities[i]["activity"]+"</strong> </div>");
            var activity_type = $("<div class='event-type col d-flex align-items-center justify-content-end'>"+activities[i]["type"]+"</div>");
            var activity_detail = $("<div class='event-desc row' id='"+activities[i]["id"]+"1'><strong class='title-text'>Description</strong><br><span>"+activities[i]["desc"]+"</span></div>")
            // var trash_icon = $("<input type='submit' value='f2ed Delete' data-sid='"+activities[i]["id"]+"' class='delete-btn fa fa-input' style='padding-top:22px; padding-left: 5px; font-size:22px;'/>");
            var trash_icon = $("<input type='submit' value='Delete' data-sid='"+activities[i]["id"]+"' class='button delete-btn'/>");
            // var edit_icon = $("<div class='edit-btn fa fa-edit' style='padding-top:22px; padding-right: 5px; font-size:22px;'></div")
            var edit_icon = $("")
            var icons = $("<div class='collapse d-flex justify-content-end' id='"+activities[i]["id"]+"2'></div>");

            trash_icon.click(delete_activity);
            // trash_icon.bind()

            $(col_container).append(activity_time).append(activity_title)
            $(row_container).append(col_container).append(activity_type);
            $(icons).append(edit_icon).append(trash_icon);
            $(activity_card).append(row_container).append(activity_detail).append(icons);
            $(as_button).append(activity_card);
            $(".events-container").append(as_button);
        }
    }
}

// Checks if a specific date has any events
function check_activities(day, month, year) {
    var activities = [];
    // console.log(day + " " + month + " " + year + JSON.stringify(activity_data["activities"][0]))
    for(var i=0; i<activity_data["activities"].length; i++) {
        var activity = activity_data["activities"][i];
        // console.log(day + " " + month + " " + year + " " + JSON.stringify(activity_data["activities"][i]))
        if(activity["day"]===day &&
            activity["month"]===month &&
            activity["year"]===year) {
                activities.push(activity);
                console.log("WEHH MASUK");
            }
    }
    // console.log("check_activities: " + JSON.stringify(activities));
    return activities;
}

// Validate date format in form
function validate_time(time) {
    if (!time) {
        return false;
    }
    var military = /^\s*([01]?\d|2[0-3]):[0-5]\d\s*$/i;
    var standard = /^\s*(0?\d|1[0-2]):[0-5]\d(\s+(AM|PM))?\s*$/i;
    return time.match(military) || time.match(standard);
}

const months = [ 
    "January", 
    "February", 
    "March", 
    "April", 
    "May", 
    "June", 
    "July", 
    "August", 
    "September", 
    "October", 
    "November", 
    "December" 
];

})(jQuery);