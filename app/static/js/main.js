$(document).ready(function () {

    $('.datepicker').datepicker({
        endDate: '-18y',
        startDate: '-75y',
        format: 'yyyy-mm-dd'
    });

    $('.activity-block .glyphicon, .saved-activity .glyphicon').click(function () {
        var $activity = $(this).closest('li');
        if ($activity.hasClass('added')) {
            removeActivity($activity);
            var toRemove = {"activityId": $activity.attr('id')};
            $.ajax({
                url: '/ajax/remove-activity',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(toRemove),
                success: function (data) {
                    console.log(data.responseText);
                },
                error: function (data) {
                    console.log(data.responseText);
                }
            });
        } else {
            removeActivity($activity);
        }

    });

    $('.sport').click(function () {
        var activity = $(this).attr('id');
        $.ajax({
            url: '/ajax/sport-block',
            type: 'POST',
            data: activity,
            success: function (data) {
                updateActivities($(data));
            },
            error: function (data) {
                console.log(data.responseText);
            }
        });
    });

    $('.final-delete').click(function () {
        var $finalDeleteInput = $('.delete-input');
        if ($finalDeleteInput.val() == 'I will lose everything') {
            $.ajax({
                url: '/ajax/delete-account',
                type: 'POST',
                success: function () {
                    window.location.replace("/login");
                },
                error: function () {
                    window.location.replace("/login");
                }
            });
        } else {
            genericAnimation($finalDeleteInput, 'shake', true)
        }
    });

    function updateActivities($activity) {
        genericAnimation($('.no-activities'), 'fadeOutDown', 300);
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
            validateActivity($(this).closest('.panel'));
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

        $activity.find('label, input, select, textarea, .panel-body').addClass('animated bouceOutUp');
        setTimeout(function () {
            $activity.find('label, input, select, textarea, .panel-body').hide();
            $activity.find('.panel-heading').animate({width: '1125px', borderRadius: '4px'}, 500).addClass('added');
        }, 1000);

        var sport = $activity.attr('id');
        var effigy = $activity.find('#effigy').val();
        var rating = $activity.find('#rating').val();
        var hours = calculateHours($activity);

        //var caloriesBurned = calculateCalories(sport, effigy, hours, rating);
        var caloriesBurned = 500;

        var $totalCalories = $('.total-calories');
        var currentCalories = parseInt($totalCalories.text().replace(' calories in total', ''));
        var newCalories = currentCalories + caloriesBurned;
        $totalCalories.text(newCalories + ' calories in total today!');

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
            data: JSON.stringify(activityObject)
        });
    }

    function removeActivity($activity) {
        genericAnimation($activity, 'zoomOut', false);
        setTimeout(function () {
            $activity.remove();
        }, 200);
    }

    function calculateHours($activity) {
        var start = new Date('01/01/2000 ' + $activity.find('#start').val()).getHours();
        var stop = new Date('01/01/2000 ' + $activity.find('#finish').val()).getHours();
        return stop - start;
    }

    function calculateCalories(sport, effigy, hours, rating) {
        $.ajax({
            url: '/ajax/calculate-calories',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({"sport": sport, "effigy": effigy, "hours": hours, "rating": rating}),
            success: function (data) {
                var calories = data;
            },
            error: function () {
                console.log('Error calculating calories.')
            }
        });
    }

    function genericAnimation($element, animation, timeout) {
        $element.addClass('animated ' + animation);
        if (timeout == true) {
            setTimeout(function () {
                $element.removeClass('animated ' + animation);
            }, 1400);
        }
    }

});