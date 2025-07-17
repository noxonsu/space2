#!/usr/bin/env python3
import os
import sys
sys.path.append('/workspaces/space2/hababru/src')

from backend.services.llms_txt_service import LlmsTxtService

try:
    service = LlmsTxtService()
    
    # Тестируем SEO страницы
    print("=== SEO PAGES ===")
    seo_pages = service._get_seo_pages_from_products()
    for page in seo_pages:
        print(f"- {page}")
    
    print("\n=== DEMO EXAMPLES ===")
    demo_examples = service._get_demo_examples_from_products()
    for example in demo_examples:
        print(f"- {example}")
    
    print("\n=== FULL LLMS.TXT ===")
    llms_content = service.generate_llms_txt()
    print(llms_content[:500] + "..." if len(llms_content) > 500 else llms_content)
            
except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()
