$(document).ready(function() {
    var $startInput = $('.input-swim-start').pickatime();
    var $startPicker = $startInput.pickatime('picker');
    
    var $finishInput = $('.input-swim-finish').pickatime();
    var $finishPicker = $finishInput.pickatime();

    $('.activity-picker li').not('.animated').click(function() {
        $(this).animate({ width: '83%' }, 350, function() {
            $(this).find('.glyphicon').fadeIn('slow');
            $(this).animate({ height: '+=250' }, 350, function () {
                $(this).addClass('animated');
            });
        });
    })
});