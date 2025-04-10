import os
import yaml


def load_yaml_data(file_name):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            if not data:
                raise ValueError("Yaml没有加载数据")

            return data
    except Exception as e:
        print(f"读取 YAML 文件 {file_name} 时发生错误: {e}")
        return []