#!/bin/bash

# Скрипт для комплексного запуска тестов
# Использование: ./scripts/run-tests.sh [type] [options]

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода заголовков
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Функция для вывода успеха
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Функция для вывода ошибки
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Функция для вывода предупреждения
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Проверка окружения
check_environment() {
    print_header "Проверка окружения"
    
    # Проверка Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js не установлен"
        exit 1
    fi
    print_success "Node.js: $(node --version)"
    
    # Проверка npm
    if ! command -v npm &> /dev/null; then
        print_error "npm не установлен"
        exit 1
    fi
    print_success "npm: $(npm --version)"
    
    # Проверка зависимостей
    if [ ! -d "node_modules" ]; then
        print_warning "Зависимости не установлены, устанавливаю..."
        npm install
    fi
    print_success "Зависимости проверены"
    
    # Проверка тестовых файлов
    if [ ! -f ".env.test" ]; then
        print_warning "Файл .env.test не найден, создаю базовый..."
        cat > .env.test << EOF
NODE_ENV=test
LOG_LEVEL=silent
YANDEX_CLIENT_ID=test_client_id
YANDEX_CLIENT_SECRET=test_client_secret
YANDEX_REDIRECT_URI=http://localhost:3000/auth/yandex/callback
OPENAI_API_KEY=test_openai_key
EOF
    fi
    print_success "Конфигурация тестов готова"
}

# Функция для запуска конкретного типа тестов
run_test_type() {
    local test_type=$1
    local start_time=$(date +%s)
    
    print_header "Запуск $test_type тестов"
    
    case $test_type in
        "unit")
            npm run test:unit
            ;;
        "integration")
            npm run test:integration
            ;;
        "e2e")
            npm run test:e2e
            ;;
        "performance")
            npm run test:performance
            ;;
        "security")
            npm run test:security
            ;;
        "all")
            npm run test:ci
            ;;
        *)
            print_error "Неизвестный тип тестов: $test_type"
            exit 1
            ;;
    esac
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    print_success "$test_type тесты завершены за ${duration}s"
}

# Функция для генерации отчета
generate_reports() {
    print_header "Генерация отчетов"
    
    # Генерация отчета о покрытии
    if [ -d "coverage" ]; then
        print_success "Отчет о покрытии: coverage/lcov-report/index.html"
        
        # Извлечение статистики покрытия
        if [ -f "coverage/lcov-report/index.html" ]; then
            echo -e "${BLUE}Статистика покрытия:${NC}"
            grep -A 5 "headerCovTableEntryHi" coverage/lcov-report/index.html | \
                sed 's/<[^>]*>//g' | grep -E '[0-9]+\.[0-9]+%' | head -4
        fi
    else
        print_warning "Отчет о покрытии не сгенерирован"
    fi
    
    # Генерация сводного отчета
    echo -e "${BLUE}Создание сводного отчета...${NC}"
    cat > test-report.md << EOF
# Отчет о тестировании

Дата: $(date)
Версия: $(npm pkg get version | tr -d '"')

## Результаты тестирования

### Покрытие кода
- Функции: $(grep -o 'Functions.*[0-9]\+\.[0-9]\+%' coverage/lcov-report/index.html | head -1 || echo "N/A")
- Строки: $(grep -o 'Lines.*[0-9]\+\.[0-9]\+%' coverage/lcov-report/index.html | head -1 || echo "N/A")
- Ветки: $(grep -o 'Branches.*[0-9]\+\.[0-9]\+%' coverage/lcov-report/index.html | head -1 || echo "N/A")

### Файлы отчетов
- Покрытие кода: \`coverage/lcov-report/index.html\`
- Логи тестов: \`test.log\`
- Сводка: \`test-report.md\`

### Рекомендации
- Добавить тесты для файлов с низким покрытием
- Проверить производительность медленных тестов
- Обновить моки при изменении внешних API
EOF
    
    print_success "Сводный отчет: test-report.md"
}

# Функция для очистки
cleanup() {
    print_header "Очистка"
    
    # Остановка возможных зависших процессов
    pkill -f "node.*test" || true
    
    # Очистка временных файлов
    rm -rf .jest-cache || true
    rm -f test.log || true
    
    print_success "Очистка завершена"
}

# Главная функция
main() {
    local test_type=${1:-"all"}
    local start_time=$(date +%s)
    
    echo -e "${GREEN}🧪 Запуск тестов проекта Yandex Direct Service${NC}"
    echo -e "${BLUE}Тип тестов: $test_type${NC}"
    echo
    
    # Проверка окружения
    check_environment
    echo
    
    # Очистка перед запуском
    cleanup
    echo
    
    # Запуск тестов
    if run_test_type "$test_type"; then
        echo
        generate_reports
        echo
        
        local end_time=$(date +%s)
        local total_duration=$((end_time - start_time))
        print_success "Все тесты завершены успешно за ${total_duration}s"
        exit 0
    else
        echo
        print_error "Тесты завершились с ошибками"
        exit 1
    fi
}

# Справка
show_help() {
    echo "Использование: $0 [TYPE] [OPTIONS]"
    echo
    echo "TYPE:"
    echo "  unit         - Только юнит-тесты"
    echo "  integration  - Только интеграционные тесты"
    echo "  e2e          - Только E2E тесты"
    echo "  performance  - Только тесты производительности"
    echo "  security     - Только тесты безопасности"
    echo "  all          - Все тесты (по умолчанию)"
    echo
    echo "OPTIONS:"
    echo "  -h, --help   - Показать эту справку"
    echo
    echo "Примеры:"
    echo "  $0                    # Запустить все тесты"
    echo "  $0 unit              # Только юнит-тесты"
    echo "  $0 performance       # Только тесты производительности"
}

# Обработка аргументов
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
