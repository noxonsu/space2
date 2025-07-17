#!/usr/bin/env python3
import yaml
import sys
import os

os.chdir('/workspaces/space2/hababru')

try:
    with open('content/products/news_analysis.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    print('demo_examples type:', type(data.get('demo_examples')))
    print('demo_examples value:', data.get('demo_examples'))
    
    # Проверим также полную структуру
    print('All keys:', list(data.keys()))
        
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
