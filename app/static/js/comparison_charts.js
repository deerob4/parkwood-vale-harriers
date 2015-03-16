$.ajax({
    url: '/ajax/comparison_data',
    type: 'POST',
    success: function (data) {
        renderCharts(data)
    }
});

function renderCharts(data) {
    alert(data)
}