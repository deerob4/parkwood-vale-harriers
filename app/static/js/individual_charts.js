$(document).ready(function () {

    $.ajax({
        url: '/ajax/user-charts',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({"month": $('.calorie-subtitle').text().replace(' Calorie Progress', '')}),
        success: function (data) {
            constructUserChart(data)
        }
    });

    function constructUserChart(chartData) {
        var runningCtx = document.getElementById("runningChart").getContext("2d");
        var runningData = {
            labels: chartData.activities.running.dates,
            datasets: [{
                label: 'Running',
                strokeColor: "rgba(16,170,59, 0.8)",
                fillColor: "rgba(82,170,94, 0.8)",
                highlightFill: "rgb(82,170,94)",
                highlightStroke: "rgb(16,170,59)",
                data: chartData.activities.running.calories
            }]
        };
        var cyclingCtx = document.getElementById("cyclingChart").getContext("2d");
        var cyclingData = {
            labels: chartData.activities.cycling.dates,
            datasets: [{
                label: 'Cycling',
                strokeColor: "rgba(236,151,31,0.8)",
                fillColor: "rgba(240,173,78,0.8)",
                highlightFill: "rgb(240,173,78)",
                highlightStroke: "rgba(236,151,31)",
                data: chartData.activities.cycling.calories
            }]
        };
        var swimmingCtx = document.getElementById("swimmingChart").getContext("2d");
        var swimmingData = {
            labels: chartData.activities.swimming.dates,
            datasets: [{
                label: 'Swimming',
                strokeColor: "rgba(49,176,213,0.8)",
                fillColor: "rgba(91,192,222,0.8)",
                highlightFill: "rgb(91,192,222)",
                highlightStroke: "rgb(49,176,213)",
                data: chartData.activities.swimming.calories
            }]
        };

        var runningChart = new Chart(runningCtx).Bar(runningData, {bezierCurve: false});
        var cyclingChart = new Chart(cyclingCtx).Bar(cyclingData, {bezierCurve: false, animation: false});
        var swimmingChart = new Chart(swimmingCtx).Bar(swimmingData, {bezierCurve: false, animation: false});
    }

    $('.activity-change').click(function () {
        var sport = $(this).attr('id');
        if ($('.' + sport + '-data').hasClass('active') == false) {
            $('.active').addClass('animated bounceOutRight');
            setTimeout(function () {
                $('.active').css('display', 'none').removeClass('animated bounceOutRight active');
                $('.' + sport + '-data').css('display', 'block').addClass('animated bounceInLeft active');
            }, 600)
        }
    })

    $('.trainingHeading').click(function() {
        $('.runningChart').update();
    })

});

