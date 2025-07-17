#!/usr/bin/env python3
import yaml
import sys
import os

os.chdir('/workspaces/space2/hababru')

try:
    with open('content/products/contract_analysis.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    print('demo_examples type:', type(data.get('demo_examples')))
    print('demo_examples value:', data.get('demo_examples'))
    
    # Проверим также тип элемента
    demo_examples = data.get('demo_examples')
    if demo_examples and isinstance(demo_examples, list) and len(demo_examples) > 0:
        print('First example type:', type(demo_examples[0]))
        print('First example value:', demo_examples[0])
        
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
