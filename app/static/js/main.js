$(document).ready(function() {
    var $startInput = $('.input-swim-start').pickatime();
    var $startPicker = $startInput.pickatime('picker');
    
    var $finishInput = $('.input-swim-finish').pickatime();
    var $finishPicker = $finishInput.pickatime();

    //$('.activity-picker li').not('.animated').click(function() {
    //    var $this = $(this);
    //    $this.animate({ height: '520', paddingLeft: '180', fontSize: '35' }, 350, function () {
    //        $this.find('.glyphicon').fadeIn('slow');
    //        //$this.find('span').animate({ paddingLeft: '180' }, 350);
    //        $this.addClass('animated').css('background-color', 'rgba(231, 73, 68, 0.88)');
    //    });
    //});
    $('.activity-picker .glyphicon').click(function() {
        var $this = $(this);
        $this.parent('.activity-block').animate({ height: '-=445' }, 350);
    });

    $('.activity-picker li').not('.animated').click(function() {
        expandActivity($(this))
    });

    function expandActivity($activity) {
        $activity.animate({ height: '520' }, { duration: 350, queue: false });
        //$activity.find('span').animate({ paddingLeft: '180' }, { duration: 350, queue: false });
        $activity.find('input').css('display', 'block').addClass('animated fadeInUp')
    }

});