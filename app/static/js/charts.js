$.ajax({
    url: '/ajax/running',
    type: 'POST',
    success: function (data) {
        createRunningChart(data)
    }
});

function createRunningChart(data) {
    console.log(data['running_data']['calories']);
    var ctx = $("#runningChart").get(0).getContext("2d");
    var runningData = {
        labels: data['running_data']['dates'],
        datasets: [
            {
                label: "Running calories",
                fillColor: "rgba(82, 170, 94, 0.5)",
                strokeColor: "rgba(82, 170, 94, 0.8)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: data['running_data']['calories']
            }
        ]
    };
    var runningChart = new Chart(ctx).Line(runningData, {bezierCurve: true});
}