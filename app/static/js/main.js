$(document).ready(function() {

    $('.activity-picker li').not('.animated').click(function() {
        expandActivity($(this))
    });
    
    $('.add-training li').click(function() {
            addActivityBlock($(this).attr('class'));
    });

    function addActivityBlock($activity) {
        $('.activity-adder').addClass('animated fadeOutDown');
        switch ($activity) {
            case 'swimming':
                $('.activity-picker ul').append("<li class='activity-block'> <span>Swimming <span class='glyphicon glyphicon-ok'></span></span> <br/> <form method='POST'> <div class='form-group'>{{form.style.label}}{{form.style(class='form-control activity-input')}}</div><div class='row'> <div class='col-md-6'> <div class='form-group'>{{form.start.label}}{{form.start(class='form-control activity-input')}}</div></div><div class='col-md-6'> <div class='form-group'>{{form.finish.label}}{{form.finish(class='form-control activity-input')}}</div></div></div><div class='form-group'>{{form.rating.label}}{{form.rating(class='form-control activity-input')}}</div><div class='form-group'>{{form.thoughts.label}}{{form.thoughts(class='form-control activity-input')}}</div>{{form.submit(class='btn btn-primary')}}</form></li>")
                console.log('swimming!');
                break;
                console.log('running!');
            case 'running':
                break;
            case 'cycling':
                console.log('cycling');
                break;
            default:
                console.log('Activity not found - a rogue element has been introduced; the matrix has been compromised.')
        }
    }

    function expandActivity($activity) {
        //$activity.animate({ height: '520' }, { duration: 350, queue: false });
        $activity.transition({ height: '503px' });
        $activity.find('.glyphicon').fadeIn('slow').delay(0.5)
        $activity.find('label, input, select, textarea').css('display', 'block').addClass('animated fadeIn')
    }

});