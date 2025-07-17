document.addEventListener('DOMContentLoaded', () => {
    const contractUploadInput = document.getElementById('contract-upload');
    const analyzeButton = document.getElementById('analyze-button');
    const contractTextDisplayDiv = document.getElementById('contract-text-display');
    const analysisPanel = document.getElementById('analysis-results');
    const analysisProgressDiv = document.getElementById('analysis-progress');
    const progressBarContainer = document.getElementById('progress-bar-container');
    const progressBar = document.getElementById('progress-bar');

    // Elements that might not exist on SEO pages or are conditionally managed
    const mainContentSection = document.getElementById('main-content');
    const uploadSection = document.getElementById('upload-section');
    const productListContainer = document.getElementById('product-list-container'); // New element for product list

    let currentAnalysisData = null;
    let currentFullContractTextMd = "";
    let pollingIntervalId = null;
    let currentAnalysisTaskId = null;
    let currentSelectedParagraphIndex = null;

    // Function to log errors to server
    async function logErrorToServer(error, context = '') {
        try {
            const errorData = {
                message: error.message || error.toString(),
                stack: error.stack || '',
                url: window.location.href,
                context: context,
                timestamp: new Date().toISOString()
            };

            await fetch('/api/v1/log_browser_error', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(errorData)
            });
        } catch (logError) {
            console.error('Не удалось отправить ошибку на сервер:', logError);
        }
    }

    // Data from SEO page (if applicable), read from hidden div
    // Corrected: Use window.appConfig directly and ensure appConfigDiv is correctly referenced
    const appConfigDiv = document.getElementById('app-config-data'); // Corrected reference
    if (appConfigDiv && appConfigDiv.textContent) { // Corrected: use appConfigDiv
        try {
            window.appConfig = JSON.parse(appConfigDiv.textContent);
            console.log('appConfig загружен из DOM:', window.appConfig);
        } catch (e) {
            console.error("Ошибка парсинга appConfigData:", e);
        }
    }

    const isSeoPage = window.appConfig.isSeoPage || false;
    const seoPageContractTextRaw = window.appConfig.seoPageContractTextRaw;
    const seoPageAnalysisDataRaw = window.appConfig.analysis_results_raw;

    // Function to reset progress bar
    function resetProgressBar() {
        if (analysisProgressDiv) analysisProgressDiv.textContent = '';
        if (progressBar) {
            progressBar.style.width = '0%';
            progressBar.textContent = '0%';
        }
        if (progressBarContainer) progressBarContainer.style.display = 'none';
    }

    // Function to update progress bar
    function updateProgressBar(processed, total, percentage, statusText) {
        if (progressBarContainer) progressBarContainer.style.display = 'block';
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
            progressBar.textContent = `${percentage}%`;
        }
        if (analysisProgressDiv) analysisProgressDiv.textContent = statusText;
    }

    // Function to display contract text and its analysis
    // This function is now universal for the main page and SEO pages
    function displayContractAndAnalysis(contractTextMd, analysisResults) {
        console.log('displayContractAndAnalysis: Начало отображения. contractTextMd (первые 100):', contractTextMd ? contractTextMd.substring(0,100) : "N/A", 'analysisResults:', analysisResults);

        if (contractTextDisplayDiv) contractTextDisplayDiv.innerHTML = ''; // Clear previous text
        // Set initial text for analysis panel, which will be replaced if analysis exists
        if (analysisPanel) analysisPanel.innerHTML = '<p>Анализ не загружен или отсутствует.</p>';
        currentFullContractTextMd = contractTextMd || ""; // Save full text if needed elsewhere

        // Save analysis data BEFORE displaying, to use it for creating segments
        if (analysisResults && analysisResults.length > 0) {
            currentAnalysisData = analysisResults;
            console.log('displayContractAndAnalysis: Анализ данных загружен:', currentAnalysisData);
        } else {
            console.warn('displayContractAndAnalysis: analysisResults пуст или некорректен. Сегменты и анализ могут отсутствовать.');
            currentAnalysisData = [];
        }

        // Display segments based on analysisResults
        if (currentAnalysisData.length > 0) {
            currentAnalysisData.forEach((analysisItem, index) => {
                const span = document.createElement('span');
                span.classList.add('contract-paragraph');
                span.dataset.paragraphIndex = index;
                // Use 'paragraph_html' from analysisItem for HTML text of the segment
                span.innerHTML = (analysisItem.paragraph_html || analysisItem.paragraph || analysisItem.original_paragraph || `Пункт ${index + 1} (текст не найден)`) + ' '; // Added space
                
                span.addEventListener('mouseover', () => highlightParagraphAndShowAnalysis(index));
                span.addEventListener('mouseout', () => removeHighlightAndShowDefault(index)); // Changed
                span.addEventListener('click', () => selectParagraph(index)); // Added click handler
                
                if (contractTextDisplayDiv) contractTextDisplayDiv.appendChild(span);
            });

            // Add click listener to the container itself to "unselect"
            if (contractTextDisplayDiv) {
                contractTextDisplayDiv.addEventListener('click', (event) => {
                    // If click was not on a paragraph, reset selection
                    if (!event.target.classList.contains('contract-paragraph')) {
                        currentSelectedParagraphIndex = null;
                        highlightParagraph(-1); // Remove highlight from all
                        if (currentAnalysisData && currentAnalysisData.length > 0) {
                            showParagraphAnalysis(0); // Show analysis of the first item by default
                        } else {
                            analysisPanel.innerHTML = '<p>Наведите курсор на абзац слева, чтобы увидеть его анализ.</p>';
                        }
                    }
                });
            }

            // Display analysis of the first item by default if no item is selected
            if (currentSelectedParagraphIndex === null) {
                showParagraphAnalysis(0);
            } else {
                // If an item is selected, show its analysis
                showParagraphAnalysis(currentSelectedParagraphIndex);
                highlightParagraph(currentSelectedParagraphIndex); // Highlight the selected one
            }
        } else if (currentFullContractTextMd) {
            // If no analysis, but contract text exists, display it as one block (old behavior as fallback)
            // This might be useful if analysis hasn't arrived yet, but text is available
            const p = document.createElement('p');
            p.textContent = currentFullContractTextMd;
            if (contractTextDisplayDiv) contractTextDisplayDiv.appendChild(p);
            if (analysisPanel) analysisPanel.innerHTML = '<p>Анализ для этого договора отсутствует или еще не загружен.</p>';
        } else {
            if (contractTextDisplayDiv) contractTextDisplayDiv.innerHTML = '<p>Текст договора не загружен.</p>';
        }

        // For the main page, where upload/main-content sections exist
        if (mainContentSection && uploadSection) {
            mainContentSection.style.display = 'flex';
            uploadSection.style.display = 'block';
        }
        console.log('displayContractAndAnalysis: Отображение завершено.');
    }

    // Function to highlight a specific paragraph
    function highlightParagraph(index) {
        if (!contractTextDisplayDiv) return;
        const paragraphElements = contractTextDisplayDiv.querySelectorAll('.contract-paragraph');
        paragraphElements.forEach((el, i) => {
            if (i === index) {
                el.style.backgroundColor = '#e6f7ff'; // Highlight color
            } else {
                el.style.backgroundColor = 'transparent';
            }
        });
    }

    // Highlight paragraph and show analysis on hover
    function highlightParagraphAndShowAnalysis(index) {
        // If a paragraph is already selected, do not change highlight and analysis on hover
        if (currentSelectedParagraphIndex !== null) {
            return;
        }
        highlightParagraph(index);
        showParagraphAnalysis(index);
    }

    // Remove highlight and show default analysis on mouseout
    function removeHighlightAndShowDefault(index) {
        // If a paragraph is already selected, do not remove highlight or change analysis
        if (currentSelectedParagraphIndex !== null) {
            return;
        }
        highlightParagraph(-1); // Remove highlight from all
        // Show analysis of the first item by default
        if (currentAnalysisData && currentAnalysisData.length > 0) {
            showParagraphAnalysis(0);
        } else {
            if (analysisPanel) analysisPanel.innerHTML = '<p>Наведите курсор на абзац слева, чтобы увидеть его анализ.</p>';
        }
    }

    // Function for paragraph selection (click)
    function selectParagraph(index) {
        currentSelectedParagraphIndex = index;
        highlightParagraph(index); // Highlight the selected one
        showParagraphAnalysis(index); // Show its analysis
    }

    // Function to show analysis for a specific paragraph
    function showParagraphAnalysis(index) {
        if (!analysisPanel || !currentAnalysisData || currentAnalysisData.length === 0) {
            if (analysisPanel) analysisPanel.innerHTML = '<p>Анализ не доступен.</p>';
            return;
        }

        if (index < 0 || index >= currentAnalysisData.length) {
            analysisPanel.innerHTML = '<p>Некорректный индекс параграфа.</p>';
            return;
        }

        const analysisItem = currentAnalysisData[index];
        if (!analysisItem) {
            analysisPanel.innerHTML = '<p>Анализ для этого параграфа не найден.</p>';
            return;
        }

        // Create analysis HTML content
        let analysisHtml = `<h3>Анализ параграфа ${index + 1}</h3>`;
        
        // Add original paragraph text if available
        if (analysisItem.paragraph || analysisItem.original_paragraph) {
            analysisHtml += `<div class="original-paragraph"><strong>Оригинальный текст:</strong><br>${analysisItem.paragraph || analysisItem.original_paragraph}</div><br>`;
        }

        // Add analysis content
        if (analysisItem.analysis) {
            analysisHtml += `<div class="analysis-content"><strong>Анализ:</strong><br>${analysisItem.analysis}</div>`;
        } else if (analysisItem.issues && analysisItem.issues.length > 0) {
            analysisHtml += `<div class="analysis-issues"><strong>Выявленные проблемы:</strong><ul>`;
            analysisItem.issues.forEach(issue => {
                analysisHtml += `<li>${issue}</li>`;
            });
            analysisHtml += `</ul></div>`;
        } else {
            analysisHtml += `<div class="no-analysis">Анализ для этого параграфа пока не выполнен.</div>`;
        }

        // Add recommendations if available
        if (analysisItem.recommendations && analysisItem.recommendations.length > 0) {
            analysisHtml += `<div class="recommendations"><strong>Рекомендации:</strong><ul>`;
            analysisItem.recommendations.forEach(rec => {
                analysisHtml += `<li>${rec}</li>`;
            });
            analysisHtml += `</ul></div>`;
        }

        // Add risk level if available
        if (analysisItem.risk_level) {
            const riskClass = analysisItem.risk_level.toLowerCase();
            analysisHtml += `<div class="risk-level risk-${riskClass}"><strong>Уровень риска:</strong> ${analysisItem.risk_level}</div>`;
        }

        analysisPanel.innerHTML = analysisHtml;
    }

    // Function to start analysis and poll for status
    async function startAnalysisAndPollStatus(contractTextMd) {
        // If there's an active task, clear the previous polling interval
        if (pollingIntervalId) {
            clearInterval(pollingIntervalId);
            pollingIntervalId = null;
        }
        resetProgressBar();
        if (progressBarContainer) progressBarContainer.style.display = 'block'; // Make container visible immediately
        if (analysisProgressDiv) analysisProgressDiv.textContent = 'Запуск анализа...';
        if (analysisPanel) analysisPanel.innerHTML = '<p>Анализ в процессе. Пожалуйста, подождите...</p>';

        try {
            const startResponse = await fetch('/api/v1/start_analysis', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ full_contract_text: contractTextMd }),
            });
            const startData = await startResponse.json();

            if (startData.error) {
                console.error('Ошибка при запуске анализа:', startData.error);
                if (analysisProgressDiv) analysisProgressDiv.textContent = `Ошибка: ${startData.error}`;
                if (analysisPanel) analysisPanel.innerHTML = `<p>Ошибка при запуске анализа: ${startData.error}</p>`;
                return;
            }

            currentAnalysisTaskId = startData.task_id; // Save current task ID
            console.log('Анализ запущен, Task ID:', currentAnalysisTaskId);

            // If backend returned COMPLETED or PROCESSING/PENDING status (task is already active or completed)
            if (startData.status === "COMPLETED") {
                console.log("Анализ уже был в кэше, отображаем результаты.");
                displayContractAndAnalysis(contractTextMd, startData.results.analysis_results);
                resetProgressBar();
                return;
            } else if (startData.status === "PROCESSING" || startData.status === "PENDING") {
                console.log(`Анализ уже в процессе (Task ID: ${currentAnalysisTaskId}). Начинаем опрос статуса.`);
                // Continue polling the existing task
                // Progress will be updated by the first get_analysis_status request
            }

            // Start polling for status
            pollingIntervalId = setInterval(async () => {
                const statusResponse = await fetch(`/api/v1/get_analysis_status/${currentAnalysisTaskId}`);
                const statusData = await statusResponse.json();

                if (statusData.error) {
                    console.error('Ошибка при получении статуса:', statusData.error);
                    clearInterval(pollingIntervalId);
                    pollingIntervalId = null;
                    if (analysisProgressDiv) analysisProgressDiv.textContent = `Ошибка: ${statusData.error}`;
                    if (analysisPanel) analysisPanel.innerHTML = `<p>Ошибка при получении статуса: ${statusData.error}</p>`;
                    return;
                }

                const { status, processed_items, total_items, progress_percentage, results, error } = statusData; // Changed
                let statusText = `Статус: ${status}`;

                if (status === "PROCESSING" || status === "PENDING") {
                    statusText = `Прогресс: ${processed_items} из ${total_items} пунктов (${progress_percentage}%)`; // Changed
                    updateProgressBar(processed_items, total_items, progress_percentage, statusText); // Changed
                } else if (status === "COMPLETED") {
                    clearInterval(pollingIntervalId);
                    pollingIntervalId = null;
                    statusText = `Анализ завершен: ${processed_items} из ${total_items} пунктов (100%)`; // Changed
                    updateProgressBar(processed_items, total_items, 100, statusText); // Changed
                    console.log('Анализ завершен, результаты:', results);
                    displayContractAndAnalysis(contractTextMd, results.analysis_results);
                } else if (status === "FAILED") {
                    clearInterval(pollingIntervalId);
                    pollingIntervalId = null;
                    statusText = `Анализ провален: ${error}`;
                    if (analysisProgressDiv) analysisProgressDiv.textContent = statusText;
                    if (analysisPanel) analysisPanel.innerHTML = `<p>Анализ провален: ${error}</p>`;
                    if (progressBarContainer) progressBarContainer.style.display = 'none';
                }
            }, 3000); // Poll every 3 seconds (increased from 2 seconds)

        } catch (error) {
            console.error('Критическая ошибка при запуске анализа или опросе:', error);
            // Отправляем ошибку на сервер
            logErrorToServer(error, 'startAnalysisAndPollStatus');
            if (analysisProgressDiv) analysisProgressDiv.textContent = `Критическая ошибка: ${error.message}`;
            if (analysisPanel) analysisPanel.innerHTML = `<p>Критическая ошибка: ${error.message}</p>`;
            if (pollingIntervalId) {
                clearInterval(pollingIntervalId);
                pollingIntervalId = null;
            }
        }
    }

    // Load sample contract and display on startup
    async function loadSampleContract() {
        try {
            console.log('loadSampleContract: Запрос примера договора...');
            const response = await fetch('/api/v1/get_sample_contract');
            const data = await response.json();

            if (data.error || !data.contract_text) {
                console.error('loadSampleContract: Ошибка загрузки примера договора:', data.error || 'Текст не получен');
                if (contractTextDisplayDiv) contractTextDisplayDiv.textContent = 'Не удалось загрузить пример договора.';
                if (analysisPanel) analysisPanel.textContent = '';
                return;
            }

            const sampleContractText = data.contract_text;
            console.log('loadSampleContract: Получен текст примера договора (первые 200 символов):', sampleContractText.substring(0, 200));
            
            // Display text immediately
            // displayContractAndAnalysis(sampleContractText, []); // Removed, as analysis is started below and will call displayContractAndAnalysis itself
            
            // Start asynchronous analysis, which will call displayContractAndAnalysis with results on success
            startAnalysisAndPollStatus(sampleContractText);

        } catch (error) {
            console.error('loadSampleContract: Критическая ошибка при загрузке примера:', error);
            logErrorToServer(error, 'loadSampleContract');
            if (contractTextDisplayDiv) contractTextDisplayDiv.textContent = 'Критическая ошибка при загрузке примера договора.';
            if (analysisPanel) analysisPanel.innerHTML = `<p>Произошла ошибка: ${error.message}</p>`;
        }
    }

    // Initialize on page load
    const urlParams = new URLSearchParams(window.location.search);
    const testFileName = urlParams.get('test');

    // --- Check for /analyze/<contract_id> first ---
    const pathSegments = window.location.pathname.split('/');
    const analyzeIndex = pathSegments.indexOf('analyze');
    let contractIdFromUrl = null;

    if (analyzeIndex !== -1 && analyzeIndex < pathSegments.length - 1) {
        contractIdFromUrl = pathSegments[analyzeIndex + 1];
        console.log('Обнаружен contract_id в URL:', contractIdFromUrl);

        // Hide upload section and show main content section immediately
        if (uploadSection) uploadSection.style.display = 'none';
        if (mainContentSection) mainContentSection.style.display = 'flex';

        // Load contract text and start analysis
        loadContractAndAnalyze(contractIdFromUrl);
        return; // Exit initialization logic after handling /analyze page

    } else if (testFileName) {
        // Existing logic for ?test=...
        console.log('Обнаружен параметр test в URL:', testFileName);
        loadTestContractAndAnalyze(testFileName);
    } else if (isSeoPage) { // Check if it's an SEO page
        console.log('Обнаружены данные для SEO-страницы. Используем window.appConfig.');
        try {
            const contractTextForSeo = seoPageContractTextRaw;
            const analysisDataForSeo = seoPageAnalysisDataRaw;
            
            let resultsArray = [];
            if (analysisDataForSeo) {
                if (Array.isArray(analysisDataForSeo.paragraphs)) {
                    resultsArray = analysisDataForSeo.paragraphs;
                } else if (Array.isArray(analysisDataForSeo.analysis_results)) {
                    resultsArray = analysisDataForSeo.analysis_results;
                } else if (Array.isArray(analysisDataForSeo)) {
                     resultsArray = analysisDataForSeo;
                }
            }
            
            console.log('SEO Page: Contract Text:', contractTextForSeo ? contractTextForSeo.substring(0,100) : "N/A");
            console.log('SEO Page: Analysis Data (processed):', resultsArray);

            if (contractTextForSeo) {
                if (resultsArray && resultsArray.length > 0) {
                    displayContractAndAnalysis(contractTextForSeo, resultsArray);
                } else {
                    startAnalysisAndPollStatus(contractTextForSeo);
                }
            } else {
                console.warn('SEO Page: Текст договора отсутствует.');
                if(contractTextDisplayDiv) contractTextDisplayDiv.innerHTML = "<p>Ошибка: Текст договора для этой страницы не найден.</p>";
                if(analysisPanel) analysisPanel.innerHTML = "<p>Анализ невозможен без текста договора.</p>";
            }

        } catch (e) {
            console.error('Ошибка при обработке данных SEO-страницы:', e);
            if(contractTextDisplayDiv) contractTextDisplayDiv.innerHTML = `<p>Ошибка при загрузке данных страницы: ${e.message}</p>`;
            if(analysisPanel) analysisPanel.innerHTML = "";
        }
    } else {
        // Original logic for the main page
        loadSampleContract();
        // Fetch and display product list for the main page
        fetchProductList(); // Call the new function to fetch product list
    }

    // Function to fetch and display the product list
    async function fetchProductList() {
        if (!productListContainer) return; // Exit if the container doesn't exist

        try {
            console.log('fetchProductList: Запрос списка продуктов...');
            const response = await fetch('/api/products/list');
            const data = await response.json();

            if (data.success && data.products && data.products.length > 0) {
                console.log('fetchProductList: Получен список продуктов:', data.products);
                productListContainer.innerHTML = ''; // Clear the "Loading..." message

                const productList = document.createElement('ul');
                productList.classList.add('product-list'); // Add a class for potential styling
                // Add some basic inline styles for better visibility if CSS is not applied
                productList.style.listStyle = 'none';
                productList.style.padding = '0';

                data.products.forEach(product => {
                    const listItem = document.createElement('li');
                    // Corrected template literal syntax and variable interpolation
                    listItem.innerHTML = `
                        <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px; background-color: #fff;">
                            <strong>${product.name}</strong> (${product.category || 'Без категории'})
                            <p>${product.description || 'Нет описания'}</p>
                            <a href="/products/${product.product_id}" style="color: #007bff; text-decoration: none;">Подробнее</a>
                        </div>
                    `;
                    productList.appendChild(listItem);
                });
                productListContainer.appendChild(productList);

            } else if (data.success && data.products && data.products.length === 0) {
                console.log('fetchProductList: Список продуктов пуст.');
                productListContainer.innerHTML = '<p>На данный момент продукты отсутствуют.</p>';
            } else {
                console.error('fetchProductList: Ошибка при получении списка продуктов:', data.error);
                productListContainer.innerHTML = `<p>Ошибка загрузки списка продуктов: ${data.error || 'Неизвестная ошибка'}</p>`;
            }
        } catch (error) {
            console.error('fetchProductList: Критическая ошибка при запросе списка продуктов:', error);
            logErrorToServer(error, 'fetchProductList');
            if (productListContainer) {
                productListContainer.innerHTML = `<p>Критическая ошибка при загрузке списка продуктов: ${error.message}</p>`;
            }
        }
    }


    async function loadTestContractAndAnalyze(fileName) {
        try {
            console.log(`loadTestContractAndAnalyze: Запрос данных для тестового файла: ${fileName}`);
            // Запрос на специальный эндпоинт, который вернет только текст договора
            const response = await fetch(`/api/v1/get_test_contract?file=${encodeURIComponent(fileName)}`);
            const data = await response.json();

            if (data.error || !data.contract_text) {
                console.error(`loadTestContractAndAnalyze: Ошибка загрузки тестового файла ${fileName}:`, data.error || 'Текст не получен');
                if (contractTextDisplayDiv) contractTextDisplayDiv.textContent = `Не удалось загрузить тестовый файл: ${fileName}. Ошибка: ${data.error || 'Текст не получен'}`;
                if (analysisPanel) analysisPanel.textContent = '';
                if (mainContentSection) mainContentSection.style.display = 'flex';
                if (uploadSection) uploadSection.style.display = 'block';
                return;
            }
            
            const contractTextMd = data.contract_text; // Changed from contract_text_md to contract_text
            console.log(`loadTestContractAndAnalyze: Получен текст договора для тестового файла ${fileName} (первые 200 символов):`, contractTextMd.substring(0, 200));

            // Start analysis with the loaded text
            startAnalysisAndPollStatus(contractTextMd);

        } catch (error) {
            console.error(`loadTestContractAndAnalyze: Критическая ошибка при загрузке тестового файла ${fileName}:`, error);
            logErrorToServer(error, 'loadTestContractAndAnalyze');
            if (contractTextDisplayDiv) contractTextDisplayDiv.textContent = `Критическая ошибка при обработке тестового файла: ${fileName}.`;
            if (analysisPanel) analysisPanel.innerHTML = `<p>Произошла ошибка: ${error.message}</p>`;
        }
    }


    // Event listener for "Analyze" button for user files
    if (analyzeButton) {
        analyzeButton.addEventListener('click', async () => {
            const file = contractUploadInput.files[0];
            if (!file) {
                alert('Пожалуйста, выберите файл для загрузки.');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            try {
                console.log('analyzeButton: Отправка файла на загрузку...');
                // 1. Upload file
                const uploadResponse = await fetch('/api/v1/upload_contract', {
                    method: 'POST',
                    body: formData,
                });
                const uploadData = await uploadResponse.json();

                if (uploadData.error) {
                    console.error('analyzeButton: Ошибка загрузки файла:', uploadData.error);
                    alert('Ошибка загрузки файла: ' + uploadData.error);
                    if (contractTextDisplayDiv) contractTextDisplayDiv.textContent = 'Ошибка при загрузке файла.';
                    if (analysisPanel) analysisPanel.innerHTML = `<p>Ошибка: ${uploadData.error}</p>`;
                    return;
                }
                
                const contractId = uploadData.contract_id; // Get the contract_id from the response
                console.log('analyzeButton: Файл успешно загружен, Contract ID:', contractId);
                
                // Redirect to the new analysis page
                window.location.href = `/analyze/${contractId}`;

            } catch (error) {
                console.error('analyzeButton: Критическая ошибка при загрузке файла:', error);
                logErrorToServer(error, 'analyzeButton');
                alert('Критическая ошибка при загрузке файла: ' + error.message);
                if (contractTextDisplayDiv) contractTextDisplayDiv.textContent = 'Ошибка при обработке файла.';
                if (analysisPanel) analysisPanel.innerHTML = `<p>Произошла ошибка: ${error.message}</p>`;
            }
        });
    }

    // Function to load contract text by ID and start analysis
    async function loadContractAndAnalyze(contractId) {
        try {
            console.log(`loadContractAndAnalyze: Запрос текста договора для ID: ${contractId}`);
            const response = await fetch(`/api/v1/get_contract/${contractId}`);
            const data = await response.json();

            if (data.error || !data.contract_text) {
                console.error(`loadContractAndAnalyze: Ошибка загрузки текста договора для ID ${contractId}:`, data.error || 'Текст не получен');
                if (contractTextDisplayDiv) contractTextDisplayDiv.textContent = `Не удалось загрузить текст договора для ID ${contractId}. Ошибка: ${data.error || 'Текст не получен'}`;
                if (analysisPanel) analysisPanel.textContent = '';
                return;
            }

            const contractTextMd = data.contract_text;
            console.log(`loadContractAndAnalyze: Получен текст договора для ID ${contractId} (первые 200 символов):`, contractTextMd.substring(0, 200));

            // Start analysis with the loaded text
            startAnalysisAndPollStatus(contractTextMd);

        } catch (error) {
            console.error(`loadContractAndAnalyze: Критическая ошибка при загрузке текста договора для ID ${contractId}:`, error);
            logErrorToServer(error, 'loadContractAndAnalyze');
            if (contractTextDisplayDiv) contractTextDisplayDiv.textContent = `Критическая ошибка при загрузке текста договора для ID ${contractId}.`;
            if (analysisPanel) analysisPanel.innerHTML = `<p>Произошла ошибка: ${error.message}</p>`;
        }
    }

    // Event listener for the test error button
    const testErrorButton = document.getElementById('test-error-button');
    if (testErrorButton) {
        testErrorButton.addEventListener('click', () => {
            console.log('Вызываем тестовую ошибку...');
            // Намеренно вызываем ошибку, чтобы проверить сборщик логов
            throw new Error('Это тестовая ошибка JavaScript из браузера!');
        });
    }

});
