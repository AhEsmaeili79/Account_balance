
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

        function formatNumber(number) {
            // Format the number using Arabic numerals
            return new Intl.NumberFormat('ar-EG').format(number);
        }
    
        function updateChart() {
            document.getElementById('showIncome').addEventListener('click', () => {
                setActiveButton('showIncome');
                timeSeriesChart.data.datasets[0].data = incomeData;
                timeSeriesChart.data.datasets[0].label = 'درآمد';
                timeSeriesChart.update();
                
                const filteredMonths = months.filter((month, index) => incomeData[index] > 0);
                const filteredIncomeData = incomeData.filter(value => value > 0);
                
                document.getElementById('detailsContent').innerHTML = '<div class="card-container">' + 
                    filteredMonths.map((month, index) => `
                        <a href="/reports/month=${months.indexOf(month) + 1}" class="card-link">
                            <div class="card">
                                <h5>${month}</h5>
                                <p>مقدار: ${formatNumber(filteredIncomeData[index])} تومان</p>
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
                
                const filteredMonths = months.filter((month, index) => outcomeData[index] > 0);
                const filteredOutcomeData = outcomeData.filter(value => value > 0);
                
                document.getElementById('detailsContent').innerHTML = '<div class="card-container">' + 
                    filteredMonths.map((month, index) => `
                        <a href="/reports/month=${months.indexOf(month) + 1}" class="card-link">
                            <div class="card">
                                <h5>${month}</h5>
                                <p>مقدار: ${formatNumber(filteredOutcomeData[index])} تومان</p>
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
                            text: 'مقدار (تومان)',
                            font: {
                                size: window.innerWidth < 440 ? 10 : 14,
                                family: 'Qs Iranyekan' // for title
                            }
                        },
                        ticks: {
                            callback: value => formatNumber(value),
                            font: {
                                size: window.innerWidth < 440 ? 10 : 14,
                                family: 'Qs Iranyekan' // for each number
                            }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'ماه',
                            font: {
                                size: window.innerWidth < 440 ? 10 : 14,
                                family: 'Qs Iranyekan' // for title
                            }
                        },
                        ticks: {
                            font: {
                                size: window.innerWidth < 440 ? 10 : 14,
                                family: 'Qs Iranyekan' // for each month
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: window.innerWidth < 440 ? 12 : 14,
                                family: 'Qs Iranyekan' // for head title
                            }
                        }
                    },
                    tooltip: {
                        titleFont: {
                            family: 'Qs Iranyekan', // for tooltip title
                        },
                        bodyFont: {
                            family: 'Qs Iranyekan', // for tooltip body
                        },
                        footerFont: {
                            family: 'Qs Iranyekan', // for tooltip footer
                        },
                        callbacks: {
                            label: function(context) {
                                // for tooltip label format to have persian number
                                return `${context.label}: ${formatNumber(context.raw)} تومان`;
                            }
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


if (document.getElementById('transactions-container')) {
    // Modal Delete alert
    function showConfirmModal(transactionId) {
        document.getElementById('modalTransactionId').value = transactionId;
        document.getElementById('confirmModal').style.display = 'block';
    }}
if (document.getElementById('modalCatId')) {
    function showDelete_Cat(CatId) {
        document.getElementById('modalCatId').value = CatId;
        document.getElementById('confirmCatModal').style.display = 'block';
    }}
    
if (document.getElementById('transactions-container')) {
    function closeConfirmModal() {
        document.getElementById('confirmModal').style.display = 'none';
    }}
    
if (document.getElementById('transactions-container')) {
    function showEditModal(id, amount, date, time, category, description) {
        document.getElementById('editTransactionId').value = id;
        document.getElementById('editAmount').value = amount;
        document.getElementById('editTransactionDate').value = date;
        document.getElementById('editTransactionTime').value = time;
        document.getElementById('editCategory').value = category;
        document.getElementById('editDescription').value = description;
        document.getElementById('editModal').style.display = 'block';
    }}
if (document.getElementById('editCatModal')) {
    function showEditCatModal(cat_id ,category_name) {
        document.getElementById('editCategoryId').value = cat_id;
        document.getElementById('category_name').value = category_name;
        document.getElementById('editCatModal').style.display = 'block';
    }}
if (document.getElementById('transactions-container')) {
    function closeEditModal() {
        document.getElementById('editModal').style.display = 'none';
    }}
if (document.getElementById('editCatModal')) {
    function closeEditModal() {
        document.getElementById('editCatModal').style.display = 'none';
    }}

// // show pass
// // Select both password fields and their corresponding toggle icons
if (document.getElementById('form-input')) {
    const togglePassword1 = document.querySelector('#togglePassword1');
    const password1 = document.querySelector('#password');

    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#password2');

    // Function to toggle password visibility
    function togglePasswordVisibility(toggleButton, passwordField) {
        // Toggle the type attribute
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);

        // Toggle the eye icon
        toggleButton.classList.toggle('bi-eye');
        toggleButton.classList.toggle('bi-eye-slash');
    }
    if (document.getElementById('togglePassword1')) {
    // Event listeners for each toggle button
    togglePassword1.addEventListener('click', () => {
        togglePasswordVisibility(togglePassword1, password1);
    });
    }
    if (document.getElementById('togglePassword2')) {
    togglePassword2.addEventListener('click', () => {
        togglePasswordVisibility(togglePassword2, password2);
    });
    }
}

