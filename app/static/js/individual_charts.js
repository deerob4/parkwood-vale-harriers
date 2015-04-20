$(document).ready(function () {

    // Sends a request to get the chart data and calls constructUserChart.
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

    // Builds the three performance charts
    function constructUserChart(chartData) {

        // Builds the running chart data
        var runningCtx = document.getElementById("runningChart").getContext("2d"),
            runningData = {
                labels: chartData.activities.running.dates,
                datasets: [{
                    label: 'Running',
                    strokeColor: "rgba(16,170,59, 0.8)",
                    fillColor: "rgba(82,170,94, 0.8)",
                    data: chartData.activities.running.calories
                }]
            };

        // Buils the cycling chart data
        var cyclingCtx = document.getElementById("cyclingChart").getContext("2d"),
            cyclingData = {
                labels: chartData.activities.cycling.dates,
                datasets: [{
                    label: 'Cycling',
                    strokeColor: "rgba(236,151,31,0.8)",
                    fillColor: "rgba(240,173,78,0.8)",
                    data: chartData.activities.cycling.calories
                }]
            };

        // Builds the swimming chart data
        var swimmingCtx = document.getElementById("swimmingChart").getContext("2d"),
            swimmingData = {
                labels: chartData.activities.swimming.dates,
                datasets: [{
                    label: 'Swimming',
                    strokeColor: "rgba(49,176,213,0.8)",
                    fillColor: "rgba(91,192,222,0.8)",
                    data: chartData.activities.swimming.calories
                }]
            };

        // Displays the chart data in the individual canvas elements
        var runningChart = new Chart(runningCtx).Line(runningData, {bezierCurve: false}),
            cyclingChart = new Chart(cyclingCtx).Line(cyclingData, {bezierCurve: false, animation: false}),
            swimmingChart = new Chart(swimmingCtx).Line(swimmingData, {bezierCurve: false, animation: false});
    }

    // Animates the sport change buttons
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

});

