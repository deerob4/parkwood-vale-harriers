$.ajax({
    url: '/ajax/comparison-graph',
    data: {
        "graphType": 'swimming_calories',
        "comparisonUser": 1
    },
    dataType: 'json',
    contentType: 'application/json',
    type: 'POST',
    success: function (data) {
        alert(data.graphData.current_user);
    },
    error: function (data) {
        alert(data);
    }
});

function renderCharts(data) {
    alert(data)
}

$('#user_list').change(function() {
    alert($(this).val());
});