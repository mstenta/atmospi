$(function() {

  /**
   * Initial chart setup.
   */
  function initialSetup() {

    // Get the current time.
    var now = new Date();

    // Use local timezone.
    Highcharts.setOptions({
      global: {
        useUTC: false
      }
    });

    // Insert a div for the current time in the summary.
    $('#summary').html('<h2>Latest Measurements:</h2>');

    // Set up the Highcharts graph.
    var chart = new Highcharts.Chart({
      chart: {
        renderTo: 'graph',
        zoomType: 'xy'
      },
      title: {
        text: 'Measurements by device:'
      },
      subtitle: {
        text: document.ontouchstart === undefined ? 'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
      },
      xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: {
          minute: '%H:%M',
          hour: '%H:%M',
          day: '%b %e',
          week: '%b %e',
          month: '%b \'%y',
          year: '%Y'
        },
        gridLineWidth: 1,
        min: now.getTime() - 24 * 60 * 60 * 1000,  // Default visible range of 1 day.
        max: now.getTime()
      },
      yAxis: [{
        title: {
          text: 'Temperature (°F)'
        },
        labels: {
          formatter: function() {
            return this.value + ' F'
          },
        },
        plotBands: [{
          from: -100,
          to: 32,
          color: '#CCDDEE'
        }]
      },
      {
        title: {
          text: 'Humidity (%)'
        },
        labels: {
          formatter: function() {
            return this.value + '%'
          },
        }
      }],
      navigator: {
        enabled: true
      },
      rangeSelector: {
        enabled: true,
        buttons: [{
          type: 'day',
          count: 1,
          text: '1d'
        }, {
          type: 'week',
          count: 1,
          text: '1w'
        }, {
          type: 'month',
          count: 1,
          text: '1m'
        }, {
          type: 'month',
          count: 6,
          text: '6m'
        }, {
          type: 'year',
          count: 1,
          text: '1y'
        }, {
          type: 'all',
          text: 'all'
        }]
      },
      scrollbar: {
        enabled: true
      },
      tooltip: {
        shared: true,
      },
      legend: {
        layout: 'vertical'
      },
      plotOptions: {
        series: {
          marker: {
            radius: 1
          }
        }
      },
    });

    // Turn the loading text on.
    chart.showLoading();

    // Load a list of temperature sensing devices.
    $.getJSON('data/devices/temperature', function(devices) {

      // Iterate through the devices...
      $.each(devices, function(index, device) {

        // Turn the loading text on.
        chart.showLoading();

        // Load the device temperature data.
        $.getJSON('data/device/' + device + '/temperature', function(data) {

          // Add it as a series to the chart.
          var series = {
            name: device,
            id: device,
            data: data,
            tooltip: {
              valueSuffix: ' F'
            }
          }
          chart.addSeries(series);

          // Insert the most recent measurements into the #summary div.
          var last = data.pop();
          $('#summary').append('<div id="' + device + '">' + device + ': <span class="measurement">' + last[1] + ' &deg;F</span> <span class="time">(' + Highcharts.dateFormat('%b %e, %Y - %H:%M', new Date(last[0])) + ')</span></div>');

          // Load flags.
          $.getJSON('data/device/' + device + '/flags', function(flags) {

            // If there are flags...
            if (flags.length > 0) {

              // Define series for flags.
              var series = {
                type: 'flags',
                name: device + ' annotations',
                onSeries: device,
                data: flags,
              }

              // Add the series.
              chart.addSeries(series);
            }
          });

          // Redraw.
          chart.redraw();

          // Hide the loading text.
          chart.hideLoading();
        });
      });
    });

    // Load a list of humidity sensing devices.
    $.getJSON('data/devices/humidity', function(devices) {

      // Iterate through the devices...
      $.each(devices, function(index, device) {

        // Turn the loading text on.
        chart.showLoading();

        // Load the device humidity data.
        $.getJSON('data/device/' + device + '/humidity', function(data) {

          // Add it as a series to the chart.
          var series = {
            name: device,
            id: device,
            data: data,
            tooltip: {
              valueSuffix: '%'
            },
            yAxis: 1
          }
          chart.addSeries(series);

          // Insert the most recent measurements into the #summary div.
          var last = data.pop();
          $('#summary').append('<div id="' + device + '">' + device + ': <span class="measurement">' + last[1] + ' %</span> <span class="time">(' + Highcharts.dateFormat('%b %e, %Y - %H:%M', new Date(last[0])) + ')</span></div>');

          // Redraw.
          chart.redraw();

          // Hide the loading text.
          chart.hideLoading();
        });
      });
    });
  }

  // Do it!
  initialSetup();
});
