$(document).ready(function() {
    var podge = function () {
        alert('wee')
    }
    var $startInput = $('.input-swim-start').pickatime({
        onSet: podge()
    })
    var $startPicker = $startInput.pickatime('picker')
    
    var $finishInput = $('.input-swim-finish').pickatime()
    var $finishPicker = $finishInput.pickatime('picker')
})