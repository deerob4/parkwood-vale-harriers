$(document).ready(function () {

    $('.sport').click(function () {
        var activity = $(this).attr('id');
        $.ajax({
            url: '/ajax/' + activity + '-block',
            type: 'POST',
            dataType: 'html',
            success: function (data) {
                var item = $(data);
                $('.activity-list').append(item);
                expandActivity(item);
                $('.activity-block').not('.animated').click(function () {
                    console.log('clicked');
                    expandActivity($(this));
                });
            },
            error: function (data) {
                console.log('Something has gone wrong: ' + data);
            }
        });
    });

    function expandActivity($activity) {
        $activity.transition({height: '503px'});
        $activity.find('.glyphicon').fadeIn('slow').delay(0.5);
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeIn')
    }
});