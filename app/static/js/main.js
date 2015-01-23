$(document).ready(function () {

    $('.datepicker').datepicker({
        endDate: '-18y',
        startDate: '-75y'
    });

    $('.sport').click(function () {
        var activity = $(this).attr('id');
        $.ajax({
            url: '/ajax/' + activity + '-block',
            type: 'POST',
            dataType: 'html',
            success: function (data) {
                updateActivities($(data));
            },
            error: function (data) {
                console.log('Something has gone wrong: ' + data);
            }
        });
    });

    function updateActivities($activity) {

        //Animates the no activities message
        genericAnimation($('.no-activities'), 'fadeOutDown', false);

        //Adds the activity to the DOM and the page
        $('.activity-list').append($activity);

        //Animates the newly added element
        genericAnimation($activity, 'zoomIn', false);

        //Initialises the time picker
        $('.time').pickatime();

        //Calls the removeActivity function
        $('.activity-block .glyphicon').click(function () {
            removeActivity($(this).closest('li'));
        });

        //Calls the validateActivity function
        $('.add-activity').click(function () {
            validateActivity($(this).closest('li'));
        });
    }

    function validateActivity($activity) {
        var $start = $activity.find('#start');
        var $finish = $activity.find('#finish');

        $start.removeClass('animated zoomIn');
        $finish.removeClass('animated zoomIn');

        if ($start.val() == '') {
            genericAnimation($start, 'shake', true);
        }
        if ($finish.val() == '') {
            genericAnimation($finish, 'shake', true);
        }
        if ($start.val() != '' && $finish.val() != '') {
            addActivity($activity);
        }
    }

    function addActivity($activity) {
        $activity.find('label, input, select, textarea').addClass('animated zoomOut');
        setTimeout(function () {
            $activity.find('label, input, select, textarea').hide();
            $activity.transition({width: '1125px', height: '75px'}, 500).addClass('added');
        }, 130);
        
        var sport = $activity.attr('id');
        var effigy = $activity.find('.effigy').val()
        var startTime = $activity.find('#start').val();
        var endTime = $activity.find('#end').val();
        var rating = $activity.find('#rating').val();
        var opinion = $activity.find('#opinion').val();
        var hours = calculateHours($activity);
        var caloriesBurned = hours * effigy;
        
        $activity.find('.calories').text(' - ' + caloriesBurned + ' calories');
        
        var activityObject = {
            "sport": sport,
            "effigy": effigy,
            "calories": caloriesBurned,
            "times": {
                "start": startTime,
                "end": endTime,
                "hours": hours
            },
            "ratings": rating,
            "opinion": opinion
        }
        
        var parsedActivityObject = JSON.parse(activityObject)
        
        alert(parsedActivityObject[0])
    }

    function removeActivity($activity) {
        genericAnimation($activity, 'zoomOut', false);
        setTimeout(function () {
            $activity.remove();
        }, 200);
    }

    function genericAnimation($element, animation, timeout) {
        $element.addClass('animated ' + animation);
        if (timeout == true) {
            setTimeout(function () {
                $element.removeClass('animated ' + animation);
            }, 1400);
        }
    }

    function calculateHours($activity) {
        var start = new Date('01/01/2000 ' + $activity.find('#start').val()).getHours();
        var stop = new Date('01/01/2000 ' + $activity.find('#finish').val()).getHours();
        return stop - start;
    }

});