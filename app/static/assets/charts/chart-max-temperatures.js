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

function addData(chart, data) {
    chart.config.data.datasets.forEach((dataset) => {
        dataset.data.push({
            x: Date.now(),
            y: data
        });
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

// Area Chart Example
var ctx = document.getElementById("chart-max-temperatures");
var chartMaxTemperatures_config = {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Temperature",
            lineTension: 0.3,
            backgroundColor: "rgba(0, 97, 242, 0.5)",
            fill: false,
            borderColor: "rgba(163, 97, 39, 1)",
            pointRadius: 3,
            pointBackgroundColor: "rgba(163, 30, 39, 1)",
            pointBorderColor: "rgba(163, 30, 39, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(163, 30, 39, 1)",
            pointHoverBorderColor: "rgba(163, 30, 39, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: []
        }]
    },
    options: {
        maintainAspectRatio: false,
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
                type: 'realtime',
				realtime: {
					duration: 120000,
					refresh: 250,
					delay: 1000,
                    ttl: 120000,
                    pause: false,
					// onRefresh: onRefresh
				},
                gridLines: {
                    color: "rgba(234,236,244,0.1)",
                     borderDash: [2]
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
                    value: warning_threshold,
                    fontStyle: "normal",
                    borderColor: "rgba(244, 161, 0, 0.8)",
                    borderDash: [5, 5],
                    borderWidth: 1,
                    position: "center",
                    label: {
                        backgroundColor: "rgba(244, 161, 0, 0.9)",
                        content: "Warning Threshold",
                        enabled: false
                    }
                },
                {
                    drawTime: "beforeDatasetsDraw",
                    type: "box",
                    xScaleID: "x-axis-0",
                    yScaleID: "y-axis-0",
                    xMin: "Jan",
                    xMax: "Dec",
                    yMin: 69,
                    yMax: 90,
                    backgroundColor: "rgba(244, 161, 0, 0.1)",
                    borderColor: "rgba(244, 161, 00, 0)",
                    borderWidth: 0
                },
                {
                    drawTime: "afterDatasetsDraw",
                    type: "line",
                    mode: "horizontal",
                    scaleID: "y-axis-0",
                    value: alarm_threshold,
                    fontStyle: "normal",
                    borderColor: "rgba(232, 21, 0, 0.8)",
                    borderDash: [5, 5],
                    borderWidth: 1,
                    position: "center",
                    label: {
                        backgroundColor: "rgba(232, 21, 0, 0.9)",
                        content: "Alarm Threshold",
                        enabled: false
                    }
                }
            ]
        }
    }
};
var chartMaxTemperatures = new Chart(ctx, chartMaxTemperatures_config);
