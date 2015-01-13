$(document).ready(function () {

    $('.sport').click(function () {
        var activity = $(this).attr('id');
        $.ajax({
            url: '/ajax/' + activity + '-block',
            type: 'POST',
            dataType: 'html',
            success: function (data) {
                var activity = $(data);
                updateActivities(activity)
            },
            error: function (data) {
                console.log('Something has gone wrong: ' + data);
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
        $('.no-activities').addClass('animated fadeOutDown');
        $('.activity-block .glyphicon').click(function () {
            var $parent = $(this).closest('li');
            removeActivity($parent)
        });

        $('#add-swim').click(function () {
            var $activity = $(this).closest('li');
            var $start = $activity.closest('#start');
            var $finish = $activity.closest('#finish');
            $finish.fadeOut();
        });

        $('.activity-block').not('.animated').click(function () {
            console.log('clicked');
            expandActivity($(this));
        });
    }

    function expandActivity($activity) {
        $activity.transition({height: '503px'});
        $activity.find('.glyphicon').fadeIn('slow').delay(0.5);
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeIn')
    }

    function closeActivity($activity) {
        $activity.find('.glyphicon').fadeOut('slow').delay(0.5);
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeOut')
        $activity.transition({height: '0px'}, 500);
    }
    
    function removeActivity($activity) {
        $activity.addClass('animated zoomOut');
        setTimeout(function() {
            $activity.remove();
        }, 250);
    }

});