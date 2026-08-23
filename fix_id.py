import json

def fix_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    for product in data['products']:
        product['id'] = int(product['id'])
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

fix_json('frontend/src/lib/initialProducts.json')
fix_json('backend/internal/store/final_products.json')
