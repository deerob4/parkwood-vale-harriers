$(document).ready(function () {

    // Initialises the datepicker plugin for all inputs with a class of "datepicker"
    $('.datepicker').datepicker({endDate: '-18y', startDate: '-75y', format: 'yyyy-mm-dd'});

    $('#running-activities, #cycling-activities, #swimming-activities').DataTable({
        //"filter": false
    });

    function genericAnimation($element, animation, timeout) {
        $element.addClass('animated ' + animation);
        if (timeout === true) {
            setTimeout(function () {
                $element.removeClass('animated ' + animation);
            }, 1400);
        }
    }

    // Animates the removal of the block
    function animateRemove($activity) {
        genericAnimation($activity, 'zoomOut', false);
        setTimeout(function () {
            $activity.remove();
        }, 175);
    }

    // Called when the delete button on an activity block is pressed
    $('.saved-activity .glyphicon').click(function () {
        var $activity = $(this).closest('li'),
            toRemove = {"activityId": $activity.attr('id')};
        // If the activity block has been returned from the database
        if ($activity.hasClass('added')) {
            animateRemove($activity);
            ajaxCall('/ajax/remove-activity', 'POST', 'json', 'application/json', JSON.stringify(toRemove), null);
        } else {
            animateRemove($activity);
        }
    });

    // Sends a request to the server for the correct 
    $('.sport-button').click(function () {
        var activity = $(this).attr('id');
        ajaxCall('/ajax/sport-block', 'POST', 'text', 'text/plain', activity, updateActivities);
    });

    // Validates that times have been entered in the activity block
    function validateActivity($activity) {
        var $start = $activity.find('#start'),
            $finish = $activity.find('#finish');
        ($start, $finish).removeClass('animated zoomIn');
        if ($start.val() === '') {
            genericAnimation($start, 'shake', true);
        }
        if ($finish.val() === '') {
            genericAnimation($finish, 'shake', true);
        }
        if ($start.val() !== '' && $finish.val() !== '') {
            animateActivity($activity);
        }
    }

    function updateActivities($activity) {
        $activity = $($activity);
        genericAnimation($('.no-activities'), 'fadeOutDown', 300);
        $('.activity-list').append($activity);
        genericAnimation($activity, 'zoomIn', false);
        $('.time').pickatime({interval: 60, formatLabel: 'HH:i A', formatSubmit: 'HH:i A'});
        // If the delete button is pressed, call the remove function
        $('.activity-block .glyphicon').click(function () {
            animateRemove($(this).closest('li'));
        });
        // If the add button is clicked, call the validate function
        $('.add-activity').click(function () {
            validateActivity($(this).closest('.panel'));
        });
    }

    function animateActivity($activity) {
        var sport = $activity.attr('id'),
            containerWidth = $('.container').width();
        $activity.find('label, input, select, textarea, .panel-body ').addClass('animated zoomOut');
        setTimeout(function () {
            $activity.find('.panel-heading').animate({
                width: containerWidth, height: 60, borderBottomLeftRadius: 4,
                borderBottomRightRadius: 4, paddingTop: 17
            }, 500);
            $activity.find('.activity-block').css('margin-bottom', '15px');
            $activity.parent().removeClass('col-lg-4 col-md-6 col-sm-12').addClass('col-lg-12 col-md-12 col-sm-12');
            $activity.find('label, input, select, textarea, .form-group, .panel-body').hide();
        }, 200);
        calculateCalories(sport, $activity);
    }

    // Calculates the number of hours between the start and finish times
    function calculateHours($activity) {
        var start = new Date('01/01/2000 ' + $activity.find('#start').val()).getHours(),
            stop = new Date('01/01/2000 ' + $activity.find('#finish').val()).getHours();
        return stop - start;
    }

    function calculateCalories(sport, $activity) {
        // Activity information needed for calculations are displayed here
        var effigy = $activity.find('#effigy').val(),
            rating = $activity.find('#rating').val(),
            start = $activity.find('#start').val(),
            finish = $activity.find('#finish').val(),
            thoughts = $activity.find('#thoughts').val(),
            hours = calculateHours($activity);
        ajaxCall('/ajax/calculate-calories', 'POST', 'json', 'application/json', JSON.stringify({
            "sport": sport,
            "effigy": effigy,
            "hours": hours,
            "thoughts": thoughts,
            "start": start,
            "finish": finish,
            "rating": rating
        }), addActivity, $activity);
    }

    function addActivity(data, $activity) {
        var caloriesBurned = data.calories,
            currentCalories = parseInt($('.total-calories').text()),
            currentHours = parseInt($('.total-hours').text()),
        // Builds a string to display in the animated activity block
        // activityString = data.sport + ' (' + effigy.toLowerCase() + ') - ' + caloriesBurned + ' calories burned over ' + data.hours + ' hours',
            activityString = data.sport,
        // Constructs the final activity object in JSON, to send to the server and save to the database
            activityObject = {
                "sport": data.sport.toLowerCase(),
                "effigy": data.effigy,
                "calories": caloriesBurned,
                "start": data.start,
                "finish": data.finish,
                "hours": data.hours,
                "rating": data.rating,
                "thoughts": data.thoughts
            };

        $('.total-hours').text(currentHours + data.hours);
        $('.total-calories').text(currentCalories + caloriesBurned);

        $activity.find('.sport').text(activityString);

        ajaxCall('/ajax/send-activity', 'POST', 'json', 'application/json', JSON.stringify(activityObject), null)
    }

    // A generic function that sends a request to the server and calls a function with the returned data
    function ajaxCall(url, requestType, dataType, contentType, data, callbackFunction, activity) {
        $.ajax({
            url: url,
            type: requestType,
            dataType: dataType,
            contentType: contentType,
            data: data,
            success: function (data) {
                if (typeof activity != 'undefined') {
                    callbackFunction(data, activity);
                } else {
                    callbackFunction(data);
                }
            }
        })
    }
    
    $('[data-toggle="tooltip"]').tooltip();
    Chart.defaults.global.scaleFontFamily = "'Raleway', 'Helvetica', 'Arial', sans-serif";

});