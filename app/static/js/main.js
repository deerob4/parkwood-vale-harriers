$(document).ready(function() {

    //Initialises the datepicker plugin for all inputs with a class of "datepicker"
    $('.datepicker').datepicker({
        endDate: '-18y',
        startDate: '-75y',
        format: 'yyyy-mm-dd'
    });

    $('.running-title').click(function() {
        $.ajax({
            url: '/ajax/running',
            type: 'POST',
            success: function(data) {
                alert(data['calories']);
            }
        })
    });

    //Called when the delete button on an activity block is pressed
    $('.saved-activity .glyphicon').click(function() {
        var $activity = $(this).closest('li');
        //If the activity block has been returned from the database
        if($activity.hasClass('added')) {
            //Calls the remove activity animation
            removeActivity($activity);   
            //Stores the id of the activity in a JSON object
            var toRemove = {"activityId": $activity.attr('id')};
            //Posts this JSON object to the server to delete it from the db
            $.ajax({
                url: '/ajax/remove-activity',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(toRemove),
                error: function(data) {
                    console.log(data.responseText);
                }
            });
        } else {
            removeActivity($activity);
        }
    });
    
    //Sends a request to the server for the correct 
    $('.sport-button').click(function() {
        var activity = $(this).attr('id');
        $.ajax({
            url: '/ajax/sport-block',
            type: 'POST',
            data: activity,
            success: function(data) {
                updateActivities($(data));
            },
            error: function(data) {
                console.log(data.responseText);
            }
        });
    });

    function updateActivities($activity) {
        //Fade out the No activities message
        genericAnimation($('.no-activities'), 'fadeOutDown', 300);
        //Add the activity to the DOM
        $('.activity-list').append($activity);
        //Animate it in
        genericAnimation($activity, 'zoomIn', false);
        //Initialise the timepicker
        $('.time').pickatime({
            interval: 60,
            formatLabel: 'HH:i A',
            formatSubmit: 'HH:i A'
        });
        //If the delete button is pressed, call the remove function
        $('.activity-block .glyphicon').click(function() {
            removeActivity($(this).closest('li'));
        });
        //If the add button is clicked, call the validate function
        $('.add-activity').click(function() {
            validateActivity($(this).closest('.panel'));
        });
    }

    //Validates that times have been entered in the activity block
    function validateActivity($activity) {
        var $start = $activity.find('#start');
        var $finish = $activity.find('#finish');
        $start.removeClass('animated zoomIn');
        $finish.removeClass('animated zoomIn');
        if($start.val() == '') {
            genericAnimation($start, 'shake', true);
        }
        if($finish.val() == '') {
            genericAnimation($finish, 'shake', true);
        }
        if($start.val() != '' && $finish.val() != '') {
            addActivity($activity);
        }
    }

    function addActivity($activity) {
        var sport = $activity.attr('id');
        var containerWidth = $('.container').width();
        $activity.find('label, input, select, textarea, .panel-body ').addClass('animated zoomOut');
        setTimeout(function() {
            $activity.find('.panel-heading').animate({width: containerWidth, height: 60, borderBottomLeftRadius: 4,
                borderBottomRightRadius: 4, paddingTop: 17}, 500);
            $activity.find('.activity-block').css('margin-bottom', '15px');
            $activity.parent().removeClass('col-lg-4 col-md-6 col-sm-12').addClass('col-lg-12 col-md-12 col-sm-12');
            $activity.find('label, input, select, textarea, .form-group, .panel-body').hide();
        }, 200);
        calculateCalories(sport, $activity);
    }

    //Animates the removal of the block
    function removeActivity($activity) {
        genericAnimation($activity, 'zoomOut', false);
        setTimeout(function() {
            $activity.remove();
        }, 175);
    }

    //Calculates the number of hours between the start and finish times
    function calculateHours($activity) {
        var start = new Date('01/01/2000 ' + $activity.find('#start').val()).getHours();
        var stop = new Date('01/01/2000 ' + $activity.find('#finish').val()).getHours();
        return stop - start;
    }

    function calculateCalories(sport, $activity) {
        //Activity information needed for calculations are displayed here
        var effigy = $activity.find('#effigy').val();
        var rating = $activity.find('#rating').val();
        var hours = calculateHours($activity);
        
        //Sends this information to the server, in order to calculate the calories burned
        $.ajax({
            url: '/ajax/calculate-calories',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                "sport": sport,
                "effigy": effigy,
                "hours": hours,
                "rating": rating
            }),
            success: function(data) {
                //Stores the returned value from the server in caloriesBurned
                var caloriesBurned = data;
                
                //Updates the total calories text
                var $totalCalories = $('.total-calories');
                var currentCalories = parseInt($totalCalories.text());
                var newCalories = currentCalories + caloriesBurned;        
                $totalCalories.text(newCalories);
                
                //Updates the total hours text
                var $totalHours = $('.total-hours');
                var currentHours = parseInt($totalHours.text());      
                $totalHours.text(currentHours + hours);
               
                //Sets the text in the added activity block to the correct things
                $activity.find('.sport').text(sport + ' (' + effigy.toLowerCase() + ') - ');
                $activity.find('.calories').text(caloriesBurned + ' calories burned over');
                $activity.find('.hours').text(hours + ' hours');
                
                //Creates a JSON object containing the information for the activity
                var activityObject = {
                    "sport": sport.toLowerCase(),
                    "effigy": effigy,
                    "calories": caloriesBurned,
                    "start": $activity.find('#start').val(),
                    "finish": $activity.find('#finish').val(),
                    "hours": hours,
                    "rating": $activity.find('#rating').val(),
                    "thoughts": $activity.find('#thoughts').val()
                };
                
                //Sends the JSON object to the server
                $.ajax({
                    url: '/ajax/send-activity',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify(activityObject)
                });
            },
            error: function() {
                console.log('Error calculating calories.')
            }
        });
    }

    function genericAnimation($element, animation, timeout) {
        $element.addClass('animated ' + animation);
        if(timeout == true) {
            setTimeout(function() {
                $element.removeClass('animated ' + animation);
            }, 1400);
        }
    }
});