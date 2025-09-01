import json
import os

class JsonManager:

    def delete_previous_json(self, tag):
        json_filename = f"{tag}_posts_data.json"

        if os.path.exists(json_filename):
            os.remove(json_filename)
            print(f"Arquivo {json_filename} antigo foi apagado.")

    def delete_previous_jsons(self, tags):
        for tag in tags:
            self.delete_previous_json(tag)

    def save_on_json(self, tag, post_data):
        json_filename = f"{tag}_posts_data.json"

        if os.path.exists(json_filename):
            with open(json_filename, "r", encoding="utf-8") as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    all_data = []
        else:
            all_data = []

        # adiciona o novo post
        all_data.append(post_data)

        # salva de volta
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)