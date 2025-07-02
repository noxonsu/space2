/**
 * B2B SEO-Platform Admin Panel
 * Система управления SEO-страницами и генерации контента
 */

class SeoAdminPanel {
    constructor() {
        this.pages = [];
        this.filteredPages = [];
        this.stats = {
            totalPages: 0,
            totalKeywords: 0,
            avgKeywords: 0,
            lastGenerated: '-'
        };
        this.init();
    }

    init() {
        this.loadPages();
        this.setupEventListeners();
        this.updateStats();
    }

    setupEventListeners() {
        // Поиск по страницам
        document.getElementById('searchPages').addEventListener('input', (e) => {
            this.filterPages(e.target.value);
        });

        // Формы
        document.getElementById('singlePageForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSinglePageGeneration();
        });

        document.getElementById('bulkGenerateForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleBulkGeneration();
        });

        document.getElementById('clusterForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleClusterGeneration();
        });

        // Закрытие модальных окон по клику вне их
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    }

    async loadPages() {
        try {
            this.showLoading(true);
            const response = await fetch('/api/v1/seo_pages_list');
            if (!response.ok) throw new Error('Не удалось загрузить список страниц');
            
            this.pages = await response.json();
            this.filteredPages = [...this.pages];
            this.renderPages();
            this.updateStats();
        } catch (error) {
            console.error('Ошибка загрузки страниц:', error);
            this.showError('Не удалось загрузить список страниц');
        } finally {
            this.showLoading(false);
        }
    }

    renderPages() {
        const container = document.getElementById('pagesContainer');
        
        if (this.filteredPages.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; padding: 2rem; color: #666;">
                    <p>Страниц не найдено</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.filteredPages.map(page => `
            <div class="page-card">
                <div class="page-title">${page.title}</div>
                <div class="page-meta">
                    <span>🔗 /${page.slug}</span>
                    <span>🎯 ${page.meta_keywords.length} ключей</span>
                    <span>📝 ${page.main_keyword}</span>
                </div>
                <div style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">
                    ${page.meta_description || 'Нет описания'}
                </div>
                <div class="page-actions">
                    <a href="/${page.slug}" class="btn btn-primary btn-sm" target="_blank">👁️ Просмотр</a>
                    <button class="btn btn-warning btn-sm" onclick="seoAdmin.editPage('${page.slug}')">✏️ Редактировать</button>
                    <button class="btn btn-sm" onclick="seoAdmin.regeneratePage('${page.slug}')">🔄 Обновить</button>
                    <button class="btn btn-sm" onclick="seoAdmin.runPrompt('${page.slug}')" style="background-color: #9b59b6; color: white;">🤖 Промпт</button>
                </div>
            </div>
        `).join('');
    }

    filterPages(query) {
        if (!query.trim()) {
            this.filteredPages = [...this.pages];
        } else {
            const lowerQuery = query.toLowerCase();
            this.filteredPages = this.pages.filter(page => 
                page.title.toLowerCase().includes(lowerQuery) ||
                page.slug.toLowerCase().includes(lowerQuery) ||
                page.main_keyword.toLowerCase().includes(lowerQuery) ||
                page.meta_keywords.some(keyword => keyword.toLowerCase().includes(lowerQuery))
            );
        }
        this.renderPages();
    }

    updateStats() {
        if (this.pages.length === 0) {
            document.getElementById('totalPages').textContent = '0';
            document.getElementById('totalKeywords').textContent = '0';
            document.getElementById('avgKeywords').textContent = '0';
            document.getElementById('lastGenerated').textContent = '-';
            return;
        }

        const totalKeywords = this.pages.reduce((sum, page) => sum + page.meta_keywords.length, 0);
        const avgKeywords = Math.round(totalKeywords / this.pages.length);

        document.getElementById('totalPages').textContent = this.pages.length;
        document.getElementById('totalKeywords').textContent = totalKeywords;
        document.getElementById('avgKeywords').textContent = avgKeywords;
        document.getElementById('lastGenerated').textContent = new Date().toLocaleDateString('ru-RU');
    }

    async handleSinglePageGeneration() {
        const keyword = document.getElementById('singleKeyword').value.trim();
        if (!keyword) return;

        try {
            this.showLoading(true, 'Создание страницы...');
            
            // Используем существующий CLI скрипт через API
            const response = await fetch('/api/v1/generate_page', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ keyword })
            });

            if (!response.ok) throw new Error('Ошибка создания страницы');

            const result = await response.json();
            this.showSuccess(`Страница "${keyword}" успешно создана!`);
            this.closeModal('singlePageModal');
            document.getElementById('singleKeyword').value = '';
            await this.loadPages();
        } catch (error) {
            console.error('Ошибка создания страницы:', error);
            this.showError('Не удалось создать страницу');
        } finally {
            this.showLoading(false);
        }
    }

    async handleBulkGeneration() {
        const keywordsText = document.getElementById('bulkKeywords').value.trim();
        const delay = parseInt(document.getElementById('bulkDelay').value) || 2;
        const skipExisting = document.getElementById('skipExisting').checked;

        if (!keywordsText) return;

        const keywords = keywordsText.split('\n')
            .map(k => k.trim())
            .filter(k => k && !k.startsWith('#'));

        if (keywords.length === 0) {
            this.showError('Не найдено ключевых слов для обработки');
            return;
        }

        try {
            this.showBulkProgress(true);
            const response = await fetch('/api/v1/bulk_generate_pages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    keywords, 
                    delay, 
                    skipExisting 
                })
            });

            if (!response.ok) throw new Error('Ошибка массовой генерации');

            const result = await response.json();
            this.showSuccess(`Генерация завершена! Успешно: ${result.success}, Ошибок: ${result.failed}`);
            this.closeModal('bulkGenerateModal');
            await this.loadPages();
        } catch (error) {
            console.error('Ошибка массовой генерации:', error);
            this.showError('Ошибка при массовой генерации');
        } finally {
            this.showBulkProgress(false);
        }
    }

    async handleClusterGeneration() {
        const keyword = document.getElementById('clusterMainKeyword').value.trim();
        const size = parseInt(document.getElementById('clusterSizeModal').value) || 5;

        if (!keyword) return;

        try {
            this.showLoading(true, 'Генерация кластера...');
            
            const response = await fetch('/api/v1/generate_cluster', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ keyword, size })
            });

            if (!response.ok) throw new Error('Ошибка генерации кластера');

            const result = await response.json();
            this.showSuccess(`Кластер для "${keyword}" (${size} страниц) успешно создан!`);
            this.closeModal('clusterModal');
            document.getElementById('clusterMainKeyword').value = '';
            await this.loadPages();
        } catch (error) {
            console.error('Ошибка генерации кластера:', error);
            this.showError('Не удалось создать кластер');
        } finally {
            this.showLoading(false);
        }
    }

    showBulkProgress(show, text = '') {
        const progressDiv = document.getElementById('bulkProgress');
        const progressText = document.getElementById('bulkProgressText');
        
        progressDiv.style.display = show ? 'block' : 'none';
        if (text) progressText.textContent = text;
    }

    updateBulkProgress(percent, text) {
        const progressFill = document.getElementById('bulkProgressFill');
        const progressText = document.getElementById('bulkProgressText');
        
        progressFill.style.width = `${percent}%`;
        progressText.textContent = text;
    }

    showLoading(show, text = 'Загрузка...') {
        const loading = document.getElementById('pagesLoading');
        loading.style.display = show ? 'block' : 'none';
        if (show && text) {
            loading.innerHTML = `
                <div class="spinner"></div>
                <div>${text}</div>
            `;
        }
    }

    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'error');
    }

    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        document.body.insertBefore(alertDiv, document.body.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    // Дополнительные методы
    async editPage(slug) {
        // TODO: Реализовать редактирование страницы
        alert(`Редактирование страницы ${slug} будет реализовано в следующей версии`);
    }

    async regeneratePage(slug) {
        if (!confirm(`Вы уверены, что хотите обновить страницу "${slug}"? Это может перезаписать существующий контент.`)) {
            return;
        }
        
        try {
            this.showLoading(true, 'Обновление страницы...');
            
            const response = await fetch(`/api/v1/regenerate_page/${slug}`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Ошибка обновления страницы');

            this.showSuccess(`Страница "${slug}" успешно обновлена!`);
            await this.loadPages();
        } catch (error) {
            console.error('Ошибка обновления страницы:', error);
            this.showError('Не удалось обновить страницу');
        } finally {
            this.showLoading(false);
        }
    }

    async runPrompt(slug) {
        // TODO: Реализовать запуск промптов
        alert(`Запуск промпта для страницы ${slug} будет реализован в следующей версии`);
    }
}

// Глобальные функции для работы с модальными окнами
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Дополнительные функции для быстрых действий
function generateSinglePage() {
    const keyword = document.getElementById('quickKeyword').value.trim();
    if (!keyword) return;
    
    document.getElementById('singleKeyword').value = keyword;
    openModal('singlePageModal');
    document.getElementById('quickKeyword').value = '';
}

function generateCluster() {
    const keyword = document.getElementById('clusterKeyword').value.trim();
    const size = document.getElementById('clusterSize').value;
    
    if (!keyword) return;
    
    document.getElementById('clusterMainKeyword').value = keyword;
    document.getElementById('clusterSizeModal').value = size;
    openModal('clusterModal');
    document.getElementById('clusterKeyword').value = '';
}

function refreshPages() {
    seoAdmin.loadPages();
}

// Инициализация админ-панели
let seoAdmin;
document.addEventListener('DOMContentLoaded', () => {
    seoAdmin = new SeoAdminPanel();
});
