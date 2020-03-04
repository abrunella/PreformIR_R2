(function($) {
    "use scrict";

    //var socket = io.connect('http://' + document.domain + ':' + location.port);
    var socket = io.connect();
    
    //Alarm active
    socket.on('alarm-active-status', function(msg){
        $('#toastAlarmMessage').toast("show");
        $('#toastAlarmMessage > div > small').html(msg['timestamp']);
        $('#toastAlarmMessage div:nth-child(2) > strong:nth-child(1)').html(msg['value']);
        $('#toastAlarmMessage div:nth-child(2) > strong:nth-child(2)').html(msg['threshold']);
    });
  
    // Alarm has been reset
    $('#toastAlarmMessage').on('hide.bs.toast', function(){
      socket.emit('btn-reset-alarm');
    });

    socket.on('connect', function () {
        socket.emit('client_connected', {data: 'Client Connected'});
    });

    socket.on('setting-thresholds', function(msg){
        $('#txt-warning-val').html(msg['warning'] + " " + String.fromCharCode(176) + "F");
        $('#txt-alarm-val').html(msg['alarm'] + " " + String.fromCharCode(176) + "F");

        // Change the warning chart target line
        chartMaxTemperatures_config.options.annotation.annotations[0].value = parseInt(msg['warning']);
        // Change the alarm chart target line
        chartMaxTemperatures_config.options.annotation.annotations[2].value = parseInt(msg['alarm']);
        window.chartMaxTemperatures.update({duration: 0});
    });

    socket.on('status-sensor-temperatures', function(msg){
        $('#sensor-value-table > tbody > tr').each(function(){
            var sens_id = $(this).find("#sensorIDCell").html();
            if (msg['sensor'] == sens_id){
                 $(this).find("td:eq(2)").html(msg['avg']);
                 $(this).find("td:eq(3)").html(msg['max']);
                 $(this).find("td:eq(4)").html(msg['min']);
                 $(this).find("td:eq(5)").html(moment().format('MM/DD/YY h:mm:ss'));
            }
         });
    });

    socket.on('status-overall-temperatures', function(msg){
        $('#maxPill > h1').html(msg['max'] + " " + String.fromCharCode(176) + "F");
        $('#maxPill > p.text-muted').html(moment().format('MM/DD/YY hh:mm:ss'));
        $('#minPill > h1').html(msg['min'] + " " + String.fromCharCode(176) + "F");
        $('#minPill > p.text-muted').html(moment().format('MM/DD/YY hh:mm:ss'));
        $('#avgPill > h1').html(msg['avg'] + " " + String.fromCharCode(176) + "F");
        $('#avgPill > p.text-muted').html(moment().format('MM/DD/YY hh:mm:ss'));

        $('#overallMax').html(msg['max'] + " " + String.fromCharCode(176) + "F");
        $('#overallMin').html(msg['min'] + " " + String.fromCharCode(176) + "F");
        $('#overallAvg').html(msg['avg'] + " " + String.fromCharCode(176) + "F");
        addData(chartMaxTemperatures, msg['max'])
    });

    $("#btn-warning-minus").click(function() {
        socket.emit('btn-click-high-temp-thresholds', 'warning', 'dn');
    });

    $("#btn-warning-plus").click(function() {
        socket.emit('btn-click-high-temp-thresholds', 'warning', 'up');
    });

    $("#btn-alarm-minus").click(function() {
        socket.emit('btn-click-high-temp-thresholds', 'alarm', 'dn');
    });

    $("#btn-alarm-plus").click(function() {
        socket.emit('btn-click-high-temp-thresholds', 'alarm', 'up');
    });

})(jQuery);