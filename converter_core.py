import json
import pandas as pd
import os
def convert_json_file(filepath, save_path, target_format):
    with open(filepath, 'r', encoding='utf-8') as f: data = json.load(f)
    if isinstance(data, list) or isinstance(data, dict): df = pd.json_normalize(data)
    else: df = pd.DataFrame(data)
    if target_format == "CSV": df.to_csv(save_path, index=False, encoding='utf-8')
    elif target_format == "Excel (XLSX)": df.to_excel(save_path, index=False)
    elif target_format == "YAML":
        import yaml
        with open(save_path, 'w', encoding='utf-8') as f: yaml.dump(df.to_dict(orient="records"), f, allow_unicode=True, default_flow_style=False)
    elif target_format == "XML": df.to_xml(save_path, index=False)
    elif target_format == "HTML": df.to_html(save_path, index=False)
    elif target_format == "Markdown":
        with open(save_path, 'w', encoding='utf-8') as f: f.write(df.to_markdown(index=False))
