document.getElementById('scan-button').addEventListener('click', async () => {
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    
    loading.classList.remove('hidden');
    results.innerHTML = '';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        results.innerHTML = data.map(item => `
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-start justify-between">
                    <div>
                        <h3 class="text-lg font-medium text-gray-900">${item.email.subject}</h3>
                        <p class="text-sm text-gray-500">From: ${item.email.from}</p>
                        <p class="text-sm text-gray-500">Date: ${item.email.date}</p>
                    </div>
                    <div class="ml-4">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium
                            ${item.analysis.risk_score > 70 ? 'bg-red-100 text-red-800' :
                              item.analysis.risk_score > 30 ? 'bg-yellow-100 text-yellow-800' :
                                                             'bg-green-100 text-green-800'}">
                            Risk: ${item.analysis.risk_score}%
                        </span>
                    </div>
                </div>
                
                <div class="mt-4">
                    <h4 class="text-sm font-medium text-gray-900">Suspicious Indicators:</h4>
                    <ul class="mt-2 text-sm text-gray-600">
                        ${item.analysis.indicators.map(indicator => 
                            `<li class="flex items-start">
                                <span class="text-red-500 mr-2">•</span>
                                ${indicator}
                            </li>`
                        ).join('')}
                    </ul>
                </div>
                
                <div class="mt-4 text-sm text-gray-600">
                    <p>${item.analysis.explanation}</p>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        results.innerHTML = `
            <div class="bg-red-50 p-4 rounded-md">
                <p class="text-red-800">Error scanning emails: ${error.message}</p>
            </div>
        `;
    } finally {
        loading.classList.add('hidden');
    }
});