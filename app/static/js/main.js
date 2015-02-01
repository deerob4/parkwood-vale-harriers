$(document).ready(function () {

    $('.datepicker').datepicker({
        endDate: '-18y',
        startDate: '-75y',
        format: 'yyyy-mm-dd'
    });
    $('.activity-block .glyphicon').click(function () {
        var $activity = $(this).closest('li');
        if ($activity.hasClass('added')) {
            removeActivity($activity);
            var toRemove = {"activityId": $activity.attr('id')};
            $.ajax({
                url: '/ajax/remove-activity',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(toRemove)
            });
        } else {
            removeActivity($activity);
        }

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
        genericAnimation($('.no-activities'), 'fadeOutDown', false);
        $('.activity-list').append($activity);
        genericAnimation($activity, 'zoomIn', false);
        $('.time').pickatime({
            interval: 60,
            formatLabel: 'HH:i A',
            formatSubmit: 'HH:i A'
        });
        $('.activity-block .glyphicon').click(function () {
            removeActivity($(this).closest('li'));
        });
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
        var effigy = $activity.find('#effigy option:selected').text();
        var hours = calculateHours($activity);
        var caloriesBurned = hours * $activity.find('#effigy').val();

        var currentCalories = parseInt($('.well').text().replace(' calories in total', ''));
        var newCalories = currentCalories + caloriesBurned;
        $('.well').text(newCalories + ' calories in total today!');
        
        $activity.find('.sport').text(sport + ' (' + effigy.toLowerCase() + ') - ');
        $activity.find('.calories').text(caloriesBurned + ' calories burned over');
        $activity.find('.hours').text(hours + ' hours');

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
        $.ajax({
            url: '/ajax/send-activity',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(activityObject),
            success: function (data) {
                alert(data);
            },
            error: function (data) {
                console.log('very bad: ' + data);
            }
        });
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