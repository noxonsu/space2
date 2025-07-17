document.addEventListener('DOMContentLoaded', () => {
    const seoPagesContainer = document.getElementById('seo-pages-container');
    const openaiPromptTextarea = document.getElementById('openai-prompt');
    const outputFilenamePrefixInput = document.getElementById('output-filename-prefix');
    const runSinglePromptButton = document.getElementById('run-single-prompt-button');
    const runAllPromptsButton = document.getElementById('run-all-prompts-button');
    const loadingSpinner = document.getElementById('loading-spinner');
    const promptOutputDiv = document.getElementById('prompt-output');
    const promptErrorDiv = document.getElementById('prompt-error');
    const llmModelSelect = document.getElementById('llm-model-select');

    // Template buttons
    const templateAudienceChannelsButton = document.getElementById('template-audience-channels');
    const templateAdTextButton = document.getElementById('template-ad-text');
    const templateImageIdeaButton = document.getElementById('template-image-idea');
    const templateFindChannelsForAdsButton = document.getElementById('template-find-channels-for-ads'); // Новая кнопка

    let allSeoPages = [];
    let selectedPageSlug = null;
    let selectedLlmModel = localStorage.getItem('selectedLlmModel') || 'openai'; // По умолчанию OpenAI

    function showLoading(isLoading) {
        if (isLoading) {
            loadingSpinner.style.display = 'inline-block';
            runSinglePromptButton.disabled = true;
            runAllPromptsButton.disabled = true;
            llmModelSelect.disabled = true; // Отключаем выбор модели во время загрузки
        } else {
            loadingSpinner.style.display = 'none';
            runSinglePromptButton.disabled = false;
            runAllPromptsButton.disabled = false;
            llmModelSelect.disabled = false; // Включаем выбор модели
        }
    }

    function showOutput(message, isError = false) {
        promptOutputDiv.style.display = 'none';
        promptErrorDiv.style.display = 'none';

        if (isError) {
            promptErrorDiv.textContent = message;
            promptErrorDiv.style.display = 'block';
        } else {
            promptOutputDiv.textContent = message;
            promptOutputDiv.style.display = 'block';
        }
    }

    async function fetchSeoPages() {
        showLoading(true);
        try {
            const response = await fetch('/admin/seo_pages_list');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            allSeoPages = await response.json();
            displaySeoPages(allSeoPages);
        } catch (error) {
            console.error('Ошибка при загрузке списка SEO-страниц:', error);
            seoPagesContainer.innerHTML = `<p class="error-output">Не удалось загрузить список страниц: ${error.message}</p>`;
        } finally {
            showLoading(false);
        }
    }

    function displaySeoPages(pages) {
        seoPagesContainer.innerHTML = '';
        if (pages.length === 0) {
            seoPagesContainer.innerHTML = '<p>SEO-страницы не найдены.</p>';
            return;
        }

        pages.forEach(page => {
            const pageItem = document.createElement('div');
            pageItem.classList.add('page-item');
            pageItem.dataset.slug = page.slug;
            pageItem.innerHTML = `
                <h3><a href="/${page.slug}" target="_blank">${page.title}</a></h3>
                <p><strong>Slug:</strong> ${page.slug}</p>
                <p><strong>Ключевые слова:</strong> ${page.meta_keywords.join(', ')}</p>
                <p><strong>Описание:</strong> ${page.meta_description}</p>
                <p><strong>Основное ключевое слово:</strong> ${page.main_keyword}</p>
                <p><strong>Файл договора:</strong> ${page.contract_file}</p>
                <div class="page-prompt-results" id="results-${page.slug}"></div>
            `;
            pageItem.addEventListener('click', () => {
                // Снимаем выделение со всех
                document.querySelectorAll('.page-item').forEach(item => {
                    item.style.backgroundColor = '#f9f9f9';
                    item.style.border = '1px solid #eee';
                });
                // Выделяем выбранный
                pageItem.style.backgroundColor = '#e6f7ff';
                pageItem.style.border = '1px solid #007bff';
                selectedPageSlug = page.slug;
                runSinglePromptButton.disabled = false;
                loadPagePromptResults(page.slug); // Загружаем результаты для выбранной страницы
            });
            seoPagesContainer.appendChild(pageItem);
        });
    }

    async function loadPagePromptResults(slug) {
        const resultsDiv = document.getElementById(`results-${slug}`);
        resultsDiv.innerHTML = '<p>Загрузка существующих результатов промптов...</p>';
        try {
            const response = await fetch(`/api/v1/get_page_prompt_results?slug=${slug}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const results = await response.json();
            if (results.status === 'ok' && results.results.length > 0) {
                resultsDiv.innerHTML = '<h4>Существующие результаты промптов:</h4>';
                results.results.forEach(result => {
                    const resultItem = document.createElement('div');
                    resultItem.classList.add('result-item');
                    resultItem.innerHTML = `
                        <p><strong>Префикс:</strong> ${result.prefix}</p>
                        <p><strong>Файл:</strong> ${result.file_path}</p>
                        <p><strong>Содержание:</strong> ${result.content.substring(0, 200)}...</p>
                    `;
                    resultsDiv.appendChild(resultItem);
                });
            } else {
                resultsDiv.innerHTML = '<p>Для этой страницы нет сохраненных результатов промптов.</p>';
            }
        } catch (error) {
            console.error('Ошибка при загрузке результатов промптов для страницы:', error);
            resultsDiv.innerHTML = `<p class="error-output">Не удалось загрузить результаты промптов: ${error.message}</p>`;
        }
    }

    async function runOpenAIPrompt(pageData, forceNewRun = false) {
        let prompt = openaiPromptTextarea.value;
        const outputPrefix = outputFilenamePrefixInput.value;
        const currentLlmModel = llmModelSelect.value; // Получаем текущую выбранную модель

        if (!prompt) {
            showOutput('Пожалуйста, введите промпт.', true);
            return;
        }
        if (!outputPrefix) {
            showOutput('Пожалуйста, введите префикс имени файла для результата.', true);
            return;
        }

        showLoading(true);
        showOutput('Проверка наличия существующего результата для ' + pageData.slug + '...');

        try {
            // Обработка нового заполнителя {{FILE_LLM_RESULT:префикс_имени_файла}}
            const fileLlmResultPlaceholderRegex = /\{\{FILE_LLM_RESULT:([a-zA-Z0-9_]+)\}\}/g;
            const matches = [...prompt.matchAll(fileLlmResultPlaceholderRegex)];

            for (const match of matches) {
                const prefix = match[1];
                showOutput(`Загрузка предыдущего LLM-результата с префиксом "${prefix}" для страницы "${pageData.slug}"...`);
                const fileResultResponse = await fetch(`/api/v1/get_prompt_result?slug=${pageData.slug}&output_filename_prefix=${prefix}`);
                const fileResult = await fileResultResponse.json();

                if (fileResultResponse.ok && fileResult.status === 'ok') {
                    prompt = prompt.replace(match[0], fileResult.llm_output);
                    showOutput(`LLM-результат для "${prefix}" загружен.`);
                } else {
                    showOutput(`Внимание: Не удалось загрузить LLM-результат для префикса "${prefix}". Промпт будет выполнен без этого заполнителя. Ошибка: ${fileResult.error || 'Неизвестная ошибка'}`, true);
                    prompt = prompt.replace(match[0], ''); // Заменяем на пустую строку, если файл не найден
                }
            }

            // Если forceNewRun истинно, сразу запускаем новый промпт
            if (forceNewRun) {
                showOutput('Запуск нового промпта (сброс кэша) для ' + pageData.slug + '...');
                const response = await fetch('/api/v1/run_openai_prompt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        slug: pageData.slug,
                        prompt: prompt, // Используем обновленный промпт
                        output_filename_prefix: outputPrefix,
                        page_data: pageData, // Передаем все данные страницы
                        force_new_run: true, // Указываем, что нужно сбросить кэш
                        selected_model: currentLlmModel // Передаем выбранную модель
                    }),
                });

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.error || `Ошибка HTTP: ${response.status}`);
                }

                showOutput(`Промпт для страницы "${pageData.title}" выполнен успешно. Результат сохранен в: ${result.output_file_path}\n\nВывод LLM:\n${result.llm_output}`);
                return result;
            }

            // Иначе, сначала пытаемся получить существующий результат для текущего промпта
            const checkResponse = await fetch(`/api/v1/get_prompt_result?slug=${pageData.slug}&output_filename_prefix=${outputPrefix}`);
            const checkResult = await checkResponse.json();

            if (checkResponse.ok && checkResult.status === 'ok') {
                showOutput(`Найден существующий результат для страницы "${pageData.title}". Результат загружен из кэша: ${checkResult.output_file_path}\n\nВывод LLM:\n${checkResult.llm_output}`);
                return checkResult; // Возвращаем существующий результат
            } else if (checkResult.status === 'not_found') {
                showOutput('Существующий результат не найден. Запуск нового промпта для ' + pageData.slug + '...');
                // Если результат не найден, продолжаем выполнение нового промпта
                const response = await fetch('/api/v1/run_openai_prompt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        slug: pageData.slug,
                        prompt: prompt, // Используем обновленный промпт
                        output_filename_prefix: outputPrefix,
                        page_data: pageData, // Передаем все данные страницы
                        selected_model: currentLlmModel // Передаем выбранную модель
                    }),
                });

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.error || `Ошибка HTTP: ${response.status}`);
                }

                showOutput(`Промпт для страницы "${pageData.title}" выполнен успешно. Результат сохранен в: ${result.output_file_path}\n\nВывод LLM:\n${result.llm_output}`);
                return result; // Возвращаем результат для массовой обработки
            } else {
                // Обработка других ошибок при проверке
                throw new Error(checkResult.error || `Ошибка при проверке существующего результата: ${checkResponse.status}`);
            }
        } catch (error) {
            console.error(`Ошибка при выполнении промпта для ${pageData.slug}:`, error);
            showOutput(`Ошибка при выполнении промпта для "${pageData.title}": ${error.message}`, true);
            throw error; // Перебрасываем ошибку для массовой обработки
        } finally {
            showLoading(false);
        }
    }

    runSinglePromptButton.addEventListener('click', async () => {
        if (!selectedPageSlug) {
            showOutput('Пожалуйста, выберите страницу из списка.', true);
            return;
        }
        const pageData = allSeoPages.find(p => p.slug === selectedPageSlug);
        if (pageData) {
            // При клике на кнопку "Запустить промпт" всегда сбрасываем кэш
            await runOpenAIPrompt(pageData, true); 
        } else {
            showOutput('Выбранная страница не найдена.', true);
        }
    });

    runAllPromptsButton.addEventListener('click', async () => {
        const prompt = openaiPromptTextarea.value;
        const outputPrefix = outputFilenamePrefixInput.value;

        if (!prompt) {
            showOutput('Пожалуйста, введите промпт для OpenAI.', true);
            return;
        }
        if (!outputPrefix) {
            showOutput('Пожалуйста, введите префикс имени файла для результата.', true);
            return;
        }

        showLoading(true);
        showOutput('Запуск промпта для ВСЕХ страниц...');

        let successfulRuns = 0;
        let failedRuns = 0;
        let detailedResults = [];

        for (const pageData of allSeoPages) {
            try {
                // Для массового запуска не сбрасываем кэш по умолчанию, если не указано иное
                const result = await runOpenAIPrompt(pageData, false); 
                successfulRuns++;
                detailedResults.push(`✅ ${pageData.title}: ${result.output_file_path}`);
            } catch (error) {
                failedRuns++;
                detailedResults.push(`❌ ${pageData.title}: ${error.message}`);
            }
        }

        showLoading(false);
        showOutput(`Массовый запуск завершен.\nУспешно: ${successfulRuns}\nОшибок: ${failedRuns}\n\nПодробности:\n${detailedResults.join('\n')}`);
    });

    // Add event listeners for template buttons
    templateAudienceChannelsButton.addEventListener('click', () => {
        openaiPromptTextarea.value = 'Собери, пожалуйста, целевую аудиторию для этой страницы: {{PAGE_TITLE}} и предложи 5-7 телеграм каналов, где эта аудитория может находиться. ИспоТекст договора: {{CONTRACT_TEXT}}';
        outputFilenamePrefixInput.value = 'target_audience_telegram_channels';
        showOutput('Шаблон "Собрать аудиторию и Telegram-каналы" применен.');
    });

    templateAdTextButton.addEventListener('click', () => {
        openaiPromptTextarea.value = 'Используя собранную аудиторию (из предыдущего шага), сделай объявление до 140 символов (только текст).';
        outputFilenamePrefixInput.value = 'ad_text_140_chars';
        showOutput('Шаблон "Сделать объявление (до 140 символов)" применен.');
    });

    templateImageIdeaButton.addEventListener('click', () => {
        openaiPromptTextarea.value = 'Придумай, какую картинку поставить на фоне сео статьи. Опиши идею картинки, ее стиль и содержание.';
        outputFilenamePrefixInput.value = 'seo_article_image_idea';
        showOutput('Шаблон "Придумать картинку для статьи" применен.');
    });

    templateFindChannelsForAdsButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/content/seo_prompts/find_channels_for_ads.txt');
            if (!response.ok) {
                throw new Error(`Не удалось загрузить шаблон промпта: ${response.statusText}`);
            }
            const promptContent = await response.text();
            openaiPromptTextarea.value = promptContent;
            outputFilenamePrefixInput.value = 'find_channels_for_ads';
            showOutput('Шаблон "Найти каналы для рекламы" применен.');
        } catch (error) {
            showOutput(`Ошибка при загрузке шаблона "Найти каналы для рекламы": ${error.message}`, true);
        }
    });

    // Initial fetch
    fetchSeoPages();
    fetchLlmModels(); // Загружаем доступные модели LLM

    // Обработчик изменения выбранной модели
    llmModelSelect.addEventListener('change', (event) => {
        selectedLlmModel = event.target.value;
        localStorage.setItem('selectedLlmModel', selectedLlmModel);
        showOutput(`Выбрана модель LLM: ${selectedLlmModel}`);
    });

    // Функция для загрузки доступных LLM моделей
    async function fetchLlmModels() {
        try {
            const response = await fetch('/admin/get_llm_models');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const models = await response.json();
            
            llmModelSelect.innerHTML = ''; // Очищаем существующие опции

            if (models.length === 0) {
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'Нет доступных моделей';
                llmModelSelect.appendChild(option);
                llmModelSelect.disabled = true;
                showOutput('Нет доступных LLM моделей. Проверьте ключи API в .env', true);
                return;
            }

            models.forEach(model_full_id => {
                const option = document.createElement('option');
                option.value = model_full_id;
                // Отображаем полный идентификатор модели, например "openai:gpt-4o"
                option.textContent = model_full_id; 
                llmModelSelect.appendChild(option);
            });

            // Устанавливаем ранее выбранную модель или модель по умолчанию
            if (models.includes(selectedLlmModel)) {
                llmModelSelect.value = selectedLlmModel;
            } else if (models.length > 0) {
                llmModelSelect.value = models[0]; // Выбираем первую доступную, если сохраненной нет
                selectedLlmModel = models[0];
                localStorage.setItem('selectedLlmModel', selectedLlmModel);
            }
            showOutput(`Доступные модели LLM загружены. Текущая: ${selectedLlmModel}`);

        } catch (error) {
            console.error('Ошибка при загрузке LLM моделей:', error);
            showOutput(`Не удалось загрузить LLM модели: ${error.message}`, true);
            llmModelSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
            llmModelSelect.disabled = true;
        }
    }
});
