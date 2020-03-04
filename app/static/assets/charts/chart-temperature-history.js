// Set new default font family and font color to mimic Bootstrap's default styling
(Chart.defaults.global.defaultFontFamily = "Nunito Sans"),
'-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#858796";

function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + "").replace(",", "").replace(" ", "");
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = typeof thousands_sep === "undefined" ? "," : thousands_sep,
        dec = typeof dec_point === "undefined" ? "." : dec_point,
        s = "",
        toFixedFix = function(n, prec) {
            var k = Math.pow(10, prec);
            return "" + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : "" + Math.round(n)).split(".");
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || "").length < prec) {
        s[1] = s[1] || "";
        s[1] += new Array(prec - s[1].length + 1).join("0");
    }
    return s.join(dec);
}

// Area Chart Example
var ctx = document.getElementById("chart-temperature-history");
var myLineChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: temperature_labels,
        datasets: [{
            label: "Max Temperature",
            lineTension: 0.3,
            backgroundColor: "rgba(0, 97, 242, 0.05)",
            borderColor: "rgba(232, 21, 0, 1)",
            fill: false,
            pointRadius: 3,
            pointBackgroundColor: "rgba(232, 21, 0, 1)",
            pointBorderColor: "rgba(232, 21, 0, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(232, 21, 0, 1)",
            pointHoverBorderColor: "rgba(232, 21, 0, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: temperature_data_max
        },
        {
            label: "Min Temperature",
            lineTension: 0.3,
            backgroundColor: "rgba(0, 97, 242, 0.0)",
            fill: false,
            borderColor: "rgba(244, 161, 255, 1)",
            pointRadius: 3,
            pointBackgroundColor: "rgba(244, 161, 255, 1)",
            pointBorderColor: "rgba(244, 161, 255, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(244, 161, 255, 1)",
            pointHoverBorderColor: "rgba(244, 161, 255, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: temperature_data_min
        },
        {
            label: "Avg Temperature",
            lineTension: 0.3,
            backgroundColor: "rgba(0, 97, 242, 0.0)",
            borderColor: "rgba(244, 161, 0, 1)",
            fill: false,
            pointRadius: 3,
            pointBackgroundColor: "rgba(244, 161, 0, 1)",
            pointBorderColor: "rgba(244, 161, 0, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(244, 161, 0, 1)",
            pointHoverBorderColor: "rgba(244, 161, 0, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: temperature_data_avg
        }]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        layout: {
            padding: {
                left: 10,
                right: 25,
                top: 25,
                bottom: 0
            }
        },
        scales: {
            xAxes: [{
                time: {
                    unit: "date"
                },
                gridLines: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    maxTicksLimit: 7
                }
            }],
            yAxes: [{
                ticks: {
                    maxTicksLimit: 5,
                    padding: 10,
                    // Include a 'F' in the ticks
                    callback: function(value, index, values) {
                        return number_format(value) + " F";
                    }
                },
                gridLines: {
                    color: "rgb(234, 236, 244)",
                    zeroLineColor: "rgb(234, 236, 244)",
                    drawBorder: false,
                    borderDash: [2],
                    zeroLineBorderDash: [2]
                }
            }]
        },
        pan: {
            enabled: false,
            mode: 'x'
        },
        zoom: {
            enabled: true,

            mode: 'xy'

        },
        legend: {
            display: false
        },
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            titleMarginBottom: 10,
            titleFontColor: "#6e707e",
            titleFontSize: 14,
            borderColor: "#dddfeb",
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            intersect: false,
            mode: "index",
            caretPadding: 10,
            callbacks: {
                label: function(tooltipItem, chart) {
                    var datasetLabel =
                        chart.datasets[tooltipItem.datasetIndex].label || "";
                    return datasetLabel + ": " + number_format(tooltipItem.yLabel) + " F";
                }
            }
        },
        plugins: {
			datalabels: {
				backgroundColor: "rgba(54, 185, 204, 0.05)" ,
				borderRadius: 4,
				clip: true,
                display: false,
				color: 'white',
				font: {
					weight: 'normal'
				},
				formatter: function(value) {
					return value.y;
				}
			}
		},
        annotation: {
            annotations: [
                {
                    drawTime: "afterDatasetsDraw",
                    type: "line",
                    mode: "horizontal",
                    scaleID: "y-axis-0",
                    value: temp_log_stats_avg,
                    fontStyle: "normal",
                    borderColor: "rgba(244, 161, 0, 0.8)",
                    borderDash: [5, 5],
                    borderWidth: 1,
                    position: "left",
                    label: {
                        backgroundColor: "rgba(244, 161, 0, 0.5)",
                        content: "Average",
                        enabled: true
                    }
                },
                {
                    drawTime: "afterDatasetsDraw",
                    type: "line",
                    mode: "horizontal",
                    scaleID: "y-axis-0",
                    value: temp_log_stats_max,
                    fontStyle: "normal",
                    borderColor: "rgba(232, 21, 0, 0.8)",
                    borderDash: [5, 5],
                    borderWidth: 1,
                    position: "left",
                    label: {
                        backgroundColor: "rgba(232, 21, 0, 0.5)",
                        content: "Maximum",
                        enabled: true
                    }
                },
                {
                    drawTime: "afterDatasetsDraw",
                    type: "line",
                    mode: "horizontal",
                    scaleID: "y-axis-0",
                    value: temp_log_stats_min,
                    fontStyle: "normal",
                    borderColor: "rgba(244, 161, 255, 0.8)",
                    borderDash: [5, 5],
                    borderWidth: 1,
                    position: "left",
                    label: {
                        backgroundColor: "rgba(244, 161, 255, 0.5)",
                        content: "Minimum",
                        enabled: true
                    }
                },
            ]
        }
    }
});
