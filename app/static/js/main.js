$(document).ready(function () {

    $('.activity-picker li').not('.animated').click(function () {
        expandActivity($(this))
    });
    $('.sport').click(function () {
        addActivityBlock($(this).attr('id'));
    });

    function addActivityBlock($activity) {
        $('.activity-adder').addClass('animated fadeOutDown');
        switch ($activity) {
            case 'swimming':
                console.log('swimming!');
                break;
            case 'running':
                console.log('running!');
                break;
            case 'cycling':
                console.log('cycling');
                break;
            default:
                console.log('Activity not found - a rogue element has been introduced; the matrix has been compromised.')
        }
    }

    function expandActivity($activity) {
        $activity.transition({
            height: '503px'
        });
        $activity.find('.glyphicon').fadeIn('slow').delay(0.5);
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeIn')
    }
});