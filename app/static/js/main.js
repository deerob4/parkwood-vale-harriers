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
            removeActivity($(this).closest('li'))
        });

        //Calls the validateActivity function
        $('.add-activity').click(function () {
            validateActivity($(this).closest('li'))
        });
    }

    function validateActivity($activity) {
        var $start = $activity.find('#start');
        var $finish = $activity.find('#finish');

        if ($start.val() == '') {
            genericAnimation($start, 'shake', true)
        }
        if ($finish.val() == '') {
            genericAnimation($finish, 'shake', true)
        }
        if ($start.val() != '' && $finish.val() != '') {
            addActivity($activity)
        }
        addActivity($activity)
    }

    function addActivity($activity) {
        $activity.find('label, input, select, textarea').addClass('animated zoomOut');
        setTimeout(function () {
            $activity.find('label, input, select, textarea').hide();
            $activity.transition({width: '1170px', height: '75px'}, 500);
        }, 130);
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

});