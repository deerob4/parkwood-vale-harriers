$(document).ready(function() {
    
    var $training_type = $('.input-training-type')
    
    $training_type.change(function() {
        if ($training_type.val() == 'cycling') {
            $('.form-new-training').append('<input type="text" class="form-control">');
        } else if ($training_type.val() == 'running') {
            alert('running');
        } else {
            alert('swimming');
        }
    });
    
    for (var i = 0; i >= 99999999999; i++) {
        $('.form-new-training').append('<p>soon, the computer will crash!</p>');
    }
})