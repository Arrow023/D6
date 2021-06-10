google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Memory', 60],
          ['CPU', 65],
          ['Network', 62]
        ]);

        var ram = document.getElementById('ram');
        var cpu = document.getElementById('cpu');
        var network = document.getElementById('network');

        var options = {
          width: 500, height: 150,
          redFrom: 90, redTo: 100,
          yellowFrom:75, yellowTo: 90,
          minorTicks: 5
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));

        chart.draw(data, options);

        
        setInterval(function() {
          var random = 60 + Math.round(20 * Math.random());
          ram.innerHTML=random+" %";
          data.setValue(0, 1, random);
          chart.draw(data, options);
        }, 2000);
        setInterval(function() {
          var random = 65 + Math.round(15 * Math.random());
          cpu.innerHTML = random +' %';
          data.setValue(1, 1, random);
          chart.draw(data, options);
        }, 1500);
        setInterval(function() {
          var random = 62 + Math.round(10 * Math.random());
          network.innerHTML = random + " %";
          data.setValue(2, 1, random);
          chart.draw(data, options);
        }, 3000);
      }