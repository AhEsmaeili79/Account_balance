document.addEventListener('DOMContentLoaded', () => {

    // message function
    if (document.getElementById('message')) {
        setTimeout(function(){
            $('#message').fadeOut('slow');
        }, 3000);
    }
    

    // clock and time 
    const updateClock = () => {
        document.getElementById('current-date').textContent = new Date().toLocaleDateString('fa-IR');
        document.getElementById('current-time').textContent = new Date().toLocaleTimeString('fa-IR');
    };

    updateClock();
    setInterval(updateClock, 1000);
    // chart 

    if (document.getElementById('chartPage')) {
        const months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'];
    
        // Initial empty data
        let incomeData = Array(12).fill(0);
        let outcomeData = Array(12).fill(0);
    
        // Fetch data from the API
        fetch('/api/transactions/')
            .then(response => response.json())
            .then(data => {
                incomeData = data.income;
                outcomeData = data.outcome;
                updateChart();
            })
            .catch(error => console.error('Error fetching data:', error));
    
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
                responsive: true,
                maintainAspectRatio: false,
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
                        window.location.href = `reports/month=${monthIndex + 1}`;
                    }
                }
            }
        });
    
        function updateChart() {
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
                timeSeriesChart.data.datasets[0].label = 'هزینه';
                timeSeriesChart.update();
                document.getElementById('detailsContent').innerHTML = '<div class="card-container">' + 
                    months.map((month, index) => `<div class="card"><h5>${month}</h5><p>مقدار: ${outcomeData[index]} تومان</p></div>`).join('') +
                    '</div>';
            });
        }
    
        // Initialize chart with default data
        updateChart();
    }

    
    // transaction
    if (document.getElementById('transactions-container')) {
        document.getElementById('showIncome').addEventListener('click', function() {
            document.querySelectorAll('.transaction-card').forEach(function(card) {
                card.style.display = 'none';
            });
            document.querySelectorAll('.income').forEach(function(card) {
                card.style.display = 'block';
            });
        });

        document.getElementById('showOutcome').addEventListener('click', function() {
            document.querySelectorAll('.transaction-card').forEach(function(card) {
                card.style.display = 'none';
            });
            document.querySelectorAll('.outcome').forEach(function(card) {
                card.style.display = 'block';
            });
        });

        document.getElementById('addTransactionBtn').addEventListener('click', function() {
            var form = document.getElementById('transactionForm');
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
        });
    }
});

function convertNumbersToArabic(text) {
    const arabicNumerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
    return text.replace(/\d/g, (match) => arabicNumerals[parseInt(match, 10)]);
}

function convertNumbersToArabic(text) {
    const arabicNumerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
    return text.replace(/\d/g, (match) => arabicNumerals[parseInt(match, 10)]);
}

function convertElementNumbersToArabic(element) {
    if (element.tagName === 'TEXTAREA' || element.tagName === 'INPUT') {
        if (element.type === 'text' || element.type === 'password' || element.type === 'email' || element.type === 'tel' || element.type === 'number') {
            element.value = convertNumbersToArabic(element.value);
        }
    } else if (element.nodeType === Node.TEXT_NODE) {
        element.textContent = convertNumbersToArabic(element.textContent);
    }
}

function convertAllNumbersToArabic() {
    const elements = document.querySelectorAll('*');
    elements.forEach(element => {
        if (element.childNodes.length) {
            element.childNodes.forEach(node => {
                convertElementNumbersToArabic(node);
            });
        }
        // Handle the case where element itself might contain numbers (like inputs)
        convertElementNumbersToArabic(element);
    });
}

// Convert numbers on page load
document.addEventListener('DOMContentLoaded', convertAllNumbersToArabic);
