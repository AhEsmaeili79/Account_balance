
document.addEventListener('DOMContentLoaded', () => {
    
    var messageElement = document.getElementById('message');
    if (messageElement) {
        setTimeout(function() {
            messageElement.style.transition = 'opacity 0.8s ease-out';
            messageElement.style.opacity = 0;
            setTimeout(function() {
                messageElement.style.display = 'none';
            }, 500); // Match the transition duration
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
    
        const yearSelector = document.getElementById('yearSelector');
        
        function fetchData(year) {
            fetch(`/api/transactions/?year=${year}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                        return;
                    }
                    incomeData = data.income;
                    outcomeData = data.outcome;
                    updateChart();
                    const allZeros = incomeData.every(value => value === 0);
                    if (allZeros){
                        document.getElementById('showOutcome').click();
                    }
                    else{
                        document.getElementById('showIncome').click();
                    }                
                })
                .catch(error => console.error('Error fetching data:', error));
        }
    
        function updateChart() {
            document.getElementById('showIncome').addEventListener('click', () => {
                setActiveButton('showIncome');
                timeSeriesChart.data.datasets[0].data = incomeData;
                timeSeriesChart.data.datasets[0].label = 'درآمد';
                timeSeriesChart.update();
                document.getElementById('detailsContent').innerHTML = '<div class="card-container">' + 
                    months.map((month, index) => `
                        <a href="/reports/month=${index + 1}" class="card-link">
                            <div class="card">
                                <h5>${month}</h5>
                                <p>مقدار: ${incomeData[index]} تومان</p>
                                <p>واریزی</p>
                            </div>
                        </a>
                    `).join('') +
                    '</div>';
            });
        
            document.getElementById('showOutcome').addEventListener('click', () => {
                setActiveButton('showOutcome');
                timeSeriesChart.data.datasets[0].data = outcomeData;
                timeSeriesChart.data.datasets[0].label = 'هزینه';
                timeSeriesChart.update();
                document.getElementById('detailsContent').innerHTML = '<div class="card-container">' + 
                    months.map((month, index) => `
                        <a href="/reports/month=${index + 1}" class="card-link">
                            <div class="card">
                                <h5>${month}</h5>
                                <p>مقدار: ${outcomeData[index]} تومان</p>
                                <p>کسری</p>
                            </div>
                        </a>
                    `).join('') +
                    '</div>';
            });
        }
    
        function setActiveButton(buttonId) {
            // Remove active class from all buttons
            document.querySelectorAll('.btn').forEach(button => button.classList.remove('active'));
    
            // Add active class to the clicked button
            document.getElementById(buttonId).classList.add('active');
        }
    
        // Handle year change
        yearSelector.addEventListener('change', () => {
            const selectedYear = yearSelector.value;
            fetchData(selectedYear);
        });
    
        // Initialize chart with default data and trigger the default view
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
    
        // Fetch data for the default year
        fetchData(yearSelector.value);
    }
    

    
    // transaction Page
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

        if (document.getElementById('addTransactionBtn')) {
            document.getElementById('addTransactionBtn').addEventListener('click', function() {
                var form = document.getElementById('transactionForm');
                form.style.display = form.style.display === 'none' ? 'block' : 'none';
            });
        }

        // Automatically trigger the 'Show Income' button on page load
        document.getElementById('showIncome').click();
    }
    
    // General Report 
    if (document.getElementById('report-container')) {
        var toggles = document.querySelectorAll('.btn');

        toggles.forEach(function (button) {
            button.addEventListener('click', function () {
                var target = document.querySelector(this.getAttribute('data-target'));
                // Toggle the clicked content
                target.classList.toggle('show');
            });
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


// Modal Delete alert
function showConfirmModal(transactionId) {
    console.log(transactionId)
    document.getElementById('modalTransactionId').value = transactionId;
    document.getElementById('confirmModal').style.display = 'block';
}

function closeConfirmModal() {
    document.getElementById('confirmModal').style.display = 'none';
}


function showEditModal(id, amount, date, time, category, description) {
    document.getElementById('editTransactionId').value = id;
    document.getElementById('editAmount').value = amount;
    document.getElementById('editTransactionDate').value = date;
    document.getElementById('editTransactionTime').value = time;
    document.getElementById('editCategory').value = category;
    document.getElementById('editDescription').value = description;
    document.getElementById('editModal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}