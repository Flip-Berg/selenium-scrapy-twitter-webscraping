import json
import os

class JsonManager:

    def __init__(self):
        self.data_dir = "all_posts_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_json_path(self, tag):
        return os.path.join(self.data_dir, f"{tag}_posts_data.json")

    def delete_previous_json(self, tag):
        json_filename = self.get_json_path(tag)

        if os.path.exists(json_filename):
            os.remove(json_filename)
            print(f"Arquivo {json_filename} antigo foi apagado.")

    def delete_previous_jsons(self, tags):
        for tag in tags:
            self.delete_previous_json(tag)

    def save_on_json(self, tag, post_data):
        json_filename = self.get_json_path(tag)
        if os.path.exists(json_filename):
            with open(json_filename, "r", encoding="utf-8") as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    all_data = []
        else:
            all_data = []

        # adiciona o novo post se já não estiver presente
        if post_data["descricao"] not in [saved["descricao"] for saved in all_data]:
            all_data.append(post_data)
        else:
            print("Post já existe no arquivo, não será salvo novamente.")
            return

        # salva de volta
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"Post salvo em {json_filename}.")


    def check_if_post_is_saved(self, tag, post_description, tag_saver):
        tags = tag_saver.get_saved_tags()
        for tag in tags: #checa se o post já existe em qualquer json já feito
            json_filename = self.get_json_path(tag)
            if os.path.exists(json_filename):
                with open(json_filename, "r", encoding="utf-8") as f:
                    try:
                        all_data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Erro ao ler o arquivo {json_filename}.")
                        return False
                    except Exception as e:
                        print(f"Erro inesperado ao ler o arquivo {json_filename}: {e}")
                        return False
                for saved_post in all_data:
                    if saved_post["descricao"] == post_description:
                        return True
        return False
    
    #pega todos os jsons e junta em um só
    def merge_jsons(self, tags, output_filename="merged_posts_data.json"):
        merged_data = []
        for tag in tags:
            json_filename = self.get_json_path(tag)
            if os.path.exists(json_filename):
                with open(json_filename, "r", encoding="utf-8") as f:
                    try:
                        all_data = json.load(f)
                        merged_data.extend({"tag": tag, "posts": all_data})
                    except json.JSONDecodeError:
                        print(f"Erro ao ler o arquivo {json_filename}, pulando.")
                    except Exception as e:
                        print(f"Erro inesperado ao ler o arquivo {json_filename}: {e}, pulando.")
        
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"Todos os posts mesclados salvos em {output_filename}.")