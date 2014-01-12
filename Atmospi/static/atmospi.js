$(function() {

  // Get the current time.
  var now = new Date().getTime();

  // Use local timezone.
  Highcharts.setOptions({
    global: {
      useUTC: false
    }
  });

  // Set up the Highcharts graph.
  var chart = new Highcharts.Chart({
    chart: {
      renderTo: 'graph',
      zoomType: 'x'
    },
    title: {
      text: 'Temperatures by device:'
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
      min: now - 24 * 60 * 60 * 1000,  // Default visible range of 1 day.
      max: now
    },
    yAxis: {
      title: {
        text: 'Temperature (°F)'
      },
      plotBands: [{
        from: -100,
        to: 32,
        color: '#CCDDEE'
      }]
    },
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
      formatter: function() {
        return Highcharts.dateFormat('%b %e %H:%M', this.x) + ': <strong>' + this.y + ' °F</strong>';
      }
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

  // Load a list of devices.
  $.getJSON('data/devices', function(devices) {

    // Iterate through the devices...
    $.each(devices, function(index, device) {

      // Turn the loading text on.
      chart.showLoading();

      // Load the device data.
      $.getJSON('data/device/' + device, function(data) {

        // Add it as a series to the chart.
        var series = {
          name: device,
          data: data
        }
        chart.addSeries(series);

        // Insert the most recent measurement into the #summary div.
        var last = data.pop();
        $('#summary').append('<div id="' + device + '">' + device + ': <span class="temperature">' + last[1] + ' &deg;F</span></div>');

        // Redraw.
        chart.redraw();

        // Hide the loading text.
        chart.hideLoading();
      });
    });
  });
});
