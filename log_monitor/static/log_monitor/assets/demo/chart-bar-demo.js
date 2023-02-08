//// Set new default font family and font color to mimic Bootstrap's default styling
//Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
//Chart.defaults.global.defaultFontColor = '#292b2c';
//
//// Bar Chart Example
//var ctx = document.getElementById("myBarChart");
//var myLineChart = new Chart(ctx, {
//  type: 'bar',
//  data: {
//    labels: ["January", "February", "March", "April", "May", "June"],
//    datasets: [{
//      label: "Revenue",
//      backgroundColor: "rgba(2,117,216,1)",
//      borderColor: "rgba(2,117,216,1)",
//      data: [4215, 5312, 6251, 7841, 9821, 14984],
//    }],
//  },
//  options: {
//    scales: {
//      xAxes: [{
//        time: {
//          unit: 'month'
//        },
//        gridLines: {
//          display: false
//        },
//        ticks: {
//          maxTicksLimit: 6
//        }
//      }],
//      yAxes: [{
//        ticks: {
//          min: 0,
//          max: 15000,
//          maxTicksLimit: 5
//        },
//        gridLines: {
//          display: true
//        }
//      }],
//    },
//    legend: {
//      display: false
//    }
//  }
//});
const retailers_URL = '/get_yesterday_today_imports/'
fetch(retailers_URL)
.then(function (response) {
    return response.json();
})
.then(function (data) {
    console.log(data)
    var ctx = document.getElementById("myBarChart");
    var chart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: data['retailer'],
        datasets: [
          {
            type: "bar",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
            label: "Today",
            data: data['today']
          },
          {
            type: "line",
            label: "Yesterday",
            data: data['yesterday'],
            lineTension: 0,
            fill: true
          }
        ]
      }
    });
    })
.catch(function (err) {
    console.log(err);
})
