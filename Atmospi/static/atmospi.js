$(function() {

  /**
   * Build the graph.
   */
  function buildGraph(settings) {

    // Start with empty data.
    var data = []

    // Define the graph layout.
    var layout = {
      title: 'Measurements by device',
      xaxis: {
        autorange: true,
        rangeselector: {buttons: [
          {
            count: 1,
            label: '1d',
            step: 'day',
            stepmode: 'backward'
          },
          {
            count: 7,
            label: '1w',
            step: 'day',
            stepmode: 'backward'
          },
          {
            count: 1,
            label: '1m',
            step: 'month',
            stepmode: 'backward'
          },
          {
            count: 6,
            label: '6m',
            step: 'month',
            stepmode: 'backward'
          },
          {step: 'all'}
        ]},
        rangeslider: {},
        type: 'date'
      },
      yaxis: {
        title: 'Temperature ' + settings['t_unit'],
        autorange: true,
        type: 'linear'
      },
      yaxis2: {
        title: 'Humidity %',
        overlaying: 'y',
        side: 'right'
      },
    };


    // Add a filled area below freezing temperature.
    //data.push({
    //  title: 'Freezing',
    //  x: [0, Date.now()],
    //  y: [32, 32],
    //  fill: 'tozeroy',
    //  opacity: 0.5,
    //  type: 'scatter'
    //});

    // Plot the graph.
    Plotly.newPlot('graph-test', data, layout);

    // Define a simple function for unpacking data from Atmospi JSON.
    function unpack(rows, key) {
      return rows.map(function(row) {
        return row[key];
      });
    }

    // Define the measures we will be plotting.
    var measures = [
      'temperature',
      'humidity',
    ];

    // Iterate over the measures.
    $.each(measures, function(index, measure) {

      // Load a list of devices for this measure.
      $.getJSON('data/devices/' + measure, function(devices) {

	    // Iterate through the devices...
        $.each(devices, function(device, label) {

          // Load the device temperature data.
          Plotly.d3.json('data/device/' + device + '/' + measure, function(err, rows) {

            // Build a new trace.
            var trace = {
              type: "scatter",
              mode: "lines",
              name: label + ' (' + measure + ')',
              x: unpack(rows, 0),
              y: unpack(rows, 1),
            }

            // If this is a humidity measure...
            if (measure == 'humidity') {

              // Use a dotted line.
              trace.line = {dash: 'dot'};

              // Plot it on the second Y axis.
              trace.yaxis = 'y2';
            }

            // Add the trace to the plot.
            Plotly.addTraces('graph-test', trace);
          });
        });
      });
    });
  }

  /**
   * Load latest measurements.
   */
  function loadLatestMeasurements(settings) {

    // Insert a div for the current time in the summary.
    $('#summary').html('<h2>Latest Measurements:</h2>');

    // Load the latest temperature data.
    $.getJSON('data/latest/temperature', function(devices) {
      $.each(devices, function(device, data) {

        // Insert the most recent measurements into the #summary div.
        $('#summary').append('<div id="' + device + '">' + device + ' (temperature): <span class="measurement">' + data[1] + ' &deg;' + settings['t_unit'] + '</span> <span class="time">(' + Highcharts.dateFormat('%b %e, %Y - %H:%M', new Date(data[0])) + ')</span></div>');
      });
    });

    // Load the latest humidity data.
    $.getJSON('data/latest/humidity', function(devices) {
      $.each(devices, function(device, data) {

        // Insert the most recent measurements into the #summary div.
        $('#summary').append('<div id="' + device + '">' + device + ' (humidity): <span class="measurement">' + data[1] + ' %</span> <span class="time">(' + Highcharts.dateFormat('%b %e, %Y - %H:%M', new Date(data[0])) + ')</span></div>');
      });
    });
  }

  /**
   * Initial chart setup.
   */
  function initialSetup(settings) {

    // Get the current time.
    var now = new Date();

    // Use local timezone.
    Highcharts.setOptions({
      global: {
        useUTC: false
      }
    });

    // Calculate freezing temperature based on temperature unit.
    var freezing = (settings['t_unit'] == 'F') ? 32 : 0;

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
          text: 'Temperature (°' + settings['t_unit'] + ')'
        },
        labels: {
          formatter: function() {
            return this.value + ' ' + settings['t_unit']
          },
        },
        plotBands: [{
          from: -100,
          to: freezing,
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
      $.each(devices, function(device, label) {

        // Turn the loading text on.
        chart.showLoading();

        // Load the device temperature data.
        $.getJSON('data/device/' + device + '/temperature', function(data) {

          // Add it as a series to the chart.
          var series = {
            name: label + ' (temperature)',
            id: device,
            data: data,
            tooltip: {
              valueSuffix: ' ' + settings['t_unit']
            }
          }
          chart.addSeries(series);

          // Load flags.
          $.getJSON('data/device/' + device + '/flags', function(flags) {

            // If there are flags...
            if (flags.length > 0) {

              // Define series for flags.
              var series = {
                type: 'flags',
                name: label + ' (flags)',
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
      $.each(devices, function(device, label) {

        // Turn the loading text on.
        chart.showLoading();

        // Load the device humidity data.
        $.getJSON('data/device/' + device + '/humidity', function(data) {

          // Add it as a series to the chart.
          var series = {
            name: label + ' (humidity)',
            id: device,
            data: data,
            dashStyle: 'dot',
            tooltip: {
              valueSuffix: '%'
            },
            yAxis: 1
          }
          chart.addSeries(series);

          // Redraw.
          chart.redraw();

          // Hide the loading text.
          chart.hideLoading();
        });
      });
    });
  }

  // Load Atmospi settings and begin!
  $.getJSON('settings', function(settings) {

    // Load the latest measurements.
    loadLatestMeasurements(settings);

    // Set up the graph.
    initialSetup(settings);

    // Build the graph.
    buildGraph(settings);
  });
});
