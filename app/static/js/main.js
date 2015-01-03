$(document).ready(function() {

    $('.activity-picker li').not('.animated').click(function() {
        expandActivity($(this))
    });
    
    $('.add-training li').click(function() {
            addActivityBlock($(this).attr('class'));
    });

    function addActivityBlock($activity) {
        switch ($activity) {
            case 'swimming':
                console.log('swimming!')
                break;
            case 'running':
                console.log('running!')
                break;
            case 'cycling':
                console.log('cycling')
                break;
            default:
                console.log('Activity not found - a rogue element has been introduced; the matrix has been compromised.')
        }
    }

    function expandActivity($activity) {
        $activity.animate({ height: '520' }, { duration: 350, queue: false });
        //$activity.transition({ height: '503px' });
        $activity.find('.glyphicon').fadeIn('slow').delay(0.5)
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeIn')
    }

});