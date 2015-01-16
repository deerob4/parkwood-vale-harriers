$(document).ready(function () {

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
                alert('Something has gone wrong: ' + data);
            }
        });
    });

    function updateActivities($activity) {
        //Adds the activity to the DOM and the page
        $('.activity-list').append($activity);

        //Calls the expandActivity function, animating the activity
        expandActivity($activity);

        //Sets the activity to animated, preventing the function being called on every click
        $activity.addClass('animated');

        //Initialises the time picker
        $('.time').pickatime();

        //Animates the no activities message
        genericAnimation($('.no-activities'), 'fadeOutDown', false);

        //Calls the removeActivity function
        $('.activity-block .glyphicon').click(function () {
            var $parent = $(this).closest('li');
            removeActivity($parent)
        });

        //Calls the validateActivity function
        $('.add-activity').click(function () {
            var $activityBlock = $(this).closest('li');
            validateActivity($activityBlock)
        });
    }

    function expandActivity($activity) {
        $activity.transition({height: '503px'});
        $activity.find('.glyphicon').fadeIn('slow').delay(0.5);
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeIn');
    }

    function validateActivity($activity) {
        var $start = $activity.find('#start');
        var $finish = $activity.find('#finish');

        $start.removeClass('animated fadeIn');
        $finish.removeClass('animated fadeIn');

        if ($start.val() == '') {
            genericAnimation($start, 'shake', true)
        }
        if ($finish.val() == '') {
            genericAnimation($finish, 'shake', true)
        }
        if ($start.val() != '' && $finish.val() != '') {
            addActivity($activity)
        }
    }

    function addActivity($activity) {
        alert('The star is flying-');
    }

    function closeActivity($activity) {
        $activity.find('.glyphicon').fadeOut('slow').delay(0.5);
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeOut')
        $activity.transition({height: '0px'}, 500);
    }

    function removeActivity($activity) {
        genericAnimation($activity, 'zoomOut', false);
        setTimeout(function () {
            $activity.remove();
        }, 250);
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