$(document).ready(function() {

    $('.activity-picker li').not('.animated').click(function() {
        expandActivity($(this))
    });

    function expandActivity($activity) {
        //$activity.animate({ height: '520' }, { duration: 350, queue: false });
        $activity.transition({ height: '503px' });
        $activity.find('.glyphicon').fadeIn('slow').delay(0.5)
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeIn')
    }

});