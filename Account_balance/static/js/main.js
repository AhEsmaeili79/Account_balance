// const date = new Date();
// document.querySelector('.year').innerHTML = date.getFullYear();

// setTimeout(function(){
//     $('#message').fadeOut('slow');
// }, 3000);

document.addEventListener('DOMContentLoaded', () => {

const updateClock = () => {
    document.getElementById('current-date').textContent = new Date().toLocaleDateString('fa-IR');
    document.getElementById('current-time').textContent = new Date().toLocaleTimeString('fa-IR');
};


updateClock();
setInterval(updateClock, 1000);


    // Sample data for the chart
    const months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'];
    const incomeData = [12000, 15000, 17000, 20000, 21000, 22000, 25000, 27000, 29000, 30000, 31000, 33000];
    const outcomeData = [8000, 9000, 11000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000];

    const ctx = document.getElementById('timeSeriesChart').getContext('2d');
    const timeSeriesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'درآمد',
                data: incomeData,
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1,
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'مقدار (تومان)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'ماه'
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeOutBounce'
            },
            onClick: (event, elements) => {
                if (elements.length > 0) {
                    const chartElement = elements[0];
                    const monthIndex = chartElement.index;
                    const month = months[monthIndex];
                    // Redirect to the details page with the month as a parameter
                    const dataType = timeSeriesChart.data.datasets[0].label === 'درآمد' ? 'income' : 'outcome';
                    window.location.href = `details/month=${monthIndex}/type=${dataType}`;
                }
            }
        }
    });

    // Update chart and details based on button click
    document.getElementById('showIncome').addEventListener('click', () => {
        timeSeriesChart.data.datasets[0].data = incomeData;
        timeSeriesChart.data.datasets[0].label = 'درآمد';
        timeSeriesChart.update();
        document.getElementById('detailsContent').innerHTML = '<div class="card-container">' + 
            months.map((month, index) => `<div class="card"><h5>${month}</h5><p>مقدار: ${incomeData[index]} تومان</p></div>`).join('') +
            '</div>';
    });

    document.getElementById('showOutcome').addEventListener('click', () => {
        timeSeriesChart.data.datasets[0].data = outcomeData;
        timeSeriesChart.data.datasets[0].label = 'خرج';
        timeSeriesChart.update();
        document.getElementById('detailsContent').innerHTML = '<div class="card-container">' + 
            months.map((month, index) => `<div class="card"><h5>${month}</h5><p>مقدار: ${outcomeData[index]} تومان</p></div>`).join('') +
            '</div>';
    });
});
