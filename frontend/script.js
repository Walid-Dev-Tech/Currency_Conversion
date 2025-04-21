const fromCurrency = document.getElementById('fromCurrency');
const toCurrency = document.getElementById('toCurrency');
const amountInput = document.getElementById('amount');
const convertBtn = document.getElementById('convertBtn');
const resultDiv = document.getElementById('result');

// Load available currencies
async function loadCurrencies() {
    const response = await fetch('http://127.0.0.1:8000/symbols');
    const data = await response.json();
    const symbols = data.symbols;

    for (let code in symbols) {
        let option1 = document.createElement('option');
        let option2 = document.createElement('option');

        let description = symbols[code];  // << correct here!!

        option1.value = code;
        option1.text = `${code} - ${description}`;

        option2.value = code;
        option2.text = `${code} - ${description}`;

        fromCurrency.appendChild(option1);
        toCurrency.appendChild(option2);
    }

    fromCurrency.value = 'GBP';
    toCurrency.value = 'HUF';
}


// Convert Currency
async function convertCurrency() {
    const from = fromCurrency.value;
    const to = toCurrency.value;
    const amount = amountInput.value;

    const response = await fetch('http://127.0.0.1:8000/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from_currency: from, to_currency: to, amount: parseFloat(amount) })
    });

    if (!response.ok) {
        resultDiv.innerText = "Conversion failed.";
        return;
    }

    const data = await response.json();
    resultDiv.innerText = `Converted Amount: ${data.converted_amount} ${to}`;
}

convertBtn.addEventListener('click', convertCurrency);

// Initialize
loadCurrencies();
