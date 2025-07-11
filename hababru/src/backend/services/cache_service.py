import os
import json
import hashlib
import uuid
import threading
import glob # Добавляем импорт glob

class CacheService:
    def __init__(self, cache_dir=None):
        if cache_dir:
            self.CACHE_DIR = cache_dir
        else:
            self.CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'cache')
        
        os.makedirs(self.CACHE_DIR, exist_ok=True)

        self._analysis_tasks_status = {}
        self._status_lock = threading.Lock()

        # Директория для кэша результатов промптов LLM для SEO-страниц
        # Исправленный путь: подняться на 3 уровня вверх (services -> backend -> src -> hababru), затем content/seo_pages
        self.SEO_PROMPT_RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'content', 'seo_pages')
        os.makedirs(self.SEO_PROMPT_RESULTS_DIR, exist_ok=True) # Убедимся, что базовая директория существует

        self.SEO_CACHE_DIR = os.path.join(self.CACHE_DIR, 'seo_content') # Это для общего SEO-кэша, не для промптов
        os.makedirs(self.SEO_CACHE_DIR, exist_ok=True)

        self.SEGMENTATION_CACHE_DIR = os.path.join(self.CACHE_DIR, 'segmentations')
        os.makedirs(self.SEGMENTATION_CACHE_DIR, exist_ok=True)

    def _generate_hash(self, text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def get_file_cache_dir(self, file_hash):
        file_cache_path = os.path.join(self.CACHE_DIR, file_hash)
        os.makedirs(file_cache_path, exist_ok=True)
        return file_cache_path

    def get_cached_paragraph_analysis(self, file_hash, paragraph_text):
        paragraph_hash = self._generate_hash(paragraph_text)
        file_specific_cache_dir = self.get_file_cache_dir(file_hash)
        cache_file_path = os.path.join(file_specific_cache_dir, f"{paragraph_hash}.json")

        if os.path.exists(cache_file_path):
            try:
                with open(cache_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f).get("analysis")
            except Exception as e:
                print(f"Ошибка при чтении кэша абзаца из {cache_file_path}: {e}")
                return None
        return None

    def save_paragraph_analysis_to_cache(self, file_hash, paragraph_text, analysis_html):
        paragraph_hash = self._generate_hash(paragraph_text)
        file_specific_cache_dir = self.get_file_cache_dir(file_hash)
        cache_file_path = os.path.join(file_specific_cache_dir, f"{paragraph_hash}.json")
        
        data_to_save = {
            "paragraph": paragraph_text,
            "analysis": analysis_html,
            "paragraph_hash": paragraph_hash,
            "file_hash": file_hash
        }

        try:
            with open(cache_file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
            print(f"Результаты анализа абзаца сохранены в кэш: {cache_file_path}")
        except Exception as e:
            print(f"Ошибка при сохранении кэша абзаца в {cache_file_path}: {e}")

    def check_all_paragraphs_cached(self, file_hash, paragraphs_texts_list):
        cached_analysis_results_list = []
        for p_text in paragraphs_texts_list:
            analysis_html = self.get_cached_paragraph_analysis(file_hash, p_text)
            if analysis_html is None:
                return None
            cached_analysis_results_list.append({
                "paragraph": p_text,
                "analysis": analysis_html
            })
        
        full_contract_text_md = "\n\n".join(paragraphs_texts_list)
        return {"analysis_results": cached_analysis_results_list, "contract_text_md": full_contract_text_md}

    def create_analysis_task(self, file_hash, total_items, item_type="paragraph"):
        task_id = str(uuid.uuid4())
        with self._status_lock:
            self._analysis_tasks_status[task_id] = {
                "status": "PENDING",
                "total_items": total_items,
                "processed_items": 0,
                "progress_percentage": 0,
                "results": None,
                "error": None,
                "file_hash": file_hash,
                "item_type": item_type
            }
        return task_id

    def update_analysis_task_progress(self, task_id, processed_items):
        with self._status_lock:
            if task_id in self._analysis_tasks_status:
                status_data = self._analysis_tasks_status[task_id]
                status_data["processed_items"] = processed_items
                if status_data["total_items"] > 0:
                    status_data["progress_percentage"] = int((processed_items / status_data["total_items"]) * 100)
                status_data["status"] = "PROCESSING"
            else:
                print(f"Ошибка: Задача с ID {task_id} не найдена для обновления прогресса.")

    def complete_analysis_task(self, task_id, results):
        with self._status_lock:
            if task_id in self._analysis_tasks_status:
                status_data = self._analysis_tasks_status[task_id]
                status_data["status"] = "COMPLETED"
                status_data["processed_items"] = status_data["total_items"]
                status_data["progress_percentage"] = 100
                status_data["results"] = results
            else:
                print(f"Ошибка: Задача с ID {task_id} не найдена для завершения.")

    def fail_analysis_task(self, task_id, error_message):
        with self._status_lock:
            if task_id in self._analysis_tasks_status:
                status_data = self._analysis_tasks_status[task_id]
                status_data["status"] = "FAILED"
                status_data["error"] = error_message
            else:
                print(f"Ошибка: Задача с ID {task_id} не найдена для отметки как проваленной.")

    def get_analysis_task_status(self, task_id):
        with self._status_lock:
            return self._analysis_tasks_status.get(task_id)

    def get_active_analysis_task_by_file_hash(self, file_hash):
        with self._status_lock:
            for task_id, status_data in self._analysis_tasks_status.items():
                if status_data.get("file_hash") == file_hash and \
                   status_data["status"] in ["PENDING", "PROCESSING"]:
                    return task_id
            return None

    def get_seo_cached_analysis(self, content_key_text):
        cache_key = self._generate_hash(content_key_text)
        cache_file_path = os.path.join(self.SEO_CACHE_DIR, f"{cache_key}.json")

        if os.path.exists(cache_file_path):
            try:
                with open(cache_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка при чтении SEO кэша из {cache_file_path}: {e}")
                return None
        return None

    def save_seo_analysis_to_cache(self, content_key_text, analysis_data):
        cache_key = self._generate_hash(content_key_text)
        cache_file_path = os.path.join(self.SEO_CACHE_DIR, f"{cache_key}.json")

        try:
            with open(cache_file_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, ensure_ascii=False, indent=2)
            print(f"Результаты SEO анализа сохранены в кэш: {cache_file_path}")
        except Exception as e:
            print(f"Ошибка при сохранении SEO кэша в {cache_file_path}: {e}")

    def get_cached_segmentation(self, text_content_hash):
        cache_file_path = os.path.join(self.SEGMENTATION_CACHE_DIR, f"{text_content_hash}.json")

        if os.path.exists(cache_file_path):
            try:
                with open(cache_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка при чтении кэша сегментации из {cache_file_path}: {e}")
                return None
        return None

    def save_segmentation_to_cache(self, text_content_hash, paragraphs_list):
        cache_file_path = os.path.join(self.SEGMENTATION_CACHE_DIR, f"{text_content_hash}.json") # Corrected variable name

        try:
            with open(cache_file_path, 'w', encoding='utf-8') as f:
                json.dump(paragraphs_list, f, ensure_ascii=False, indent=2)
            print(f"Результаты сегментации сохранены в кэш: {cache_file_path}")
        except Exception as e:
            print(f"Ошибка при сохранении кэша сегментации в {cache_file_path}: {e}")

    def delete_prompt_result(self, slug, output_filename_prefix):
        """
        Удаляет файл результата промпта LLM для конкретной SEO-страницы.
        """
        page_dir = os.path.join(self.SEO_PROMPT_RESULTS_DIR, slug)
        if not os.path.exists(page_dir):
            print(f"Директория страницы {slug} не найдена: {page_dir}")
            return False

        # Ищем файл, который начинается с output_filename_prefix и заканчивается .txt
        # Используем glob для более надежного поиска
        search_pattern = os.path.join(page_dir, f"{output_filename_prefix}*.txt")
        found_files = glob.glob(search_pattern)

        if found_files:
            for file_path in found_files:
                try:
                    os.remove(file_path)
                    print(f"Удален файл кэша промпта: {file_path}")
                    return True # Удаляем только первый найденный файл, если их несколько
                except Exception as e:
                    print(f"Ошибка при удалении файла кэша промпта {file_path}: {e}")
                    return False
        else:
            print(f"Файл кэша промпта с префиксом '{output_filename_prefix}' для страницы '{slug}' не найден.")
            return False

    def get_all_prompt_results_for_page(self, slug):
        """
        Возвращает список всех сохраненных результатов промптов LLM для данной SEO-страницы.
        """
        page_dir = os.path.join(self.SEO_PROMPT_RESULTS_DIR, slug)
        results = []

        if not os.path.exists(page_dir):
            print(f"Директория страницы {slug} не найдена: {page_dir}")
            return results

        for filename in os.listdir(page_dir):
            if filename.endswith('.txt') and filename != 'generated_contract.txt' and filename != 'source.md':
                file_path = os.path.join(page_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Извлекаем префикс из имени файла
                    # Предполагаем формат: prefix_timestamp.txt
                    parts = filename.split('_')
                    if len(parts) > 2 and parts[-1].endswith('.txt') and parts[-2].isdigit():
                        prefix = '_'.join(parts[:-2])
                    else:
                        prefix = filename.replace('.txt', '')

                    results.append({
                        "prefix": prefix,
                        "file_path": file_path,
                        "content": content
                    })
                except Exception as e:
                    print(f"Ошибка при чтении файла результата промпта {file_path}: {e}")
                    continue
        return results
