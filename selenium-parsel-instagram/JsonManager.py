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
        for saved in all_data:
            if post_data["descricao"] not in saved["descricao"]:
                all_data.append(post_data)
            else:
                print("Post já existe no arquivo, não será salvo novamente.")
                print(saved["descricao"])
                print(post_data["descricao"])
                print("repr do salvo:", repr(saved["descricao"]))
                print("repr do novo:", repr(post_data["descricao"]))
                print("iguais?", self.normalize_text(saved["descricao"]) == self.normalize_text(post_data["descricao"]))
                return

        # salva de volta
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"Post salvo em {json_filename}.")

    def check_all_tags_with_json(self):
        # checa em \all_posts_data todos os jsons e retorna as tags que já tem json
        tags_with_json = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith("_posts_data.json"):
                tag = filename.replace("_posts_data.json", "")
                tags_with_json.append(tag)
        return tags_with_json


    def normalize_text(self, text):
        import unicodedata
        if not isinstance(text, str):
            return ""
        # Remove espaços extras, normaliza unicode e quebra de linha
        text = text.strip().replace('\r\n', '\n').replace('\r', '\n')
        text = unicodedata.normalize('NFC', text)
        return text

    def check_if_post_is_saved(self, tag, post_description, return_post=False):
        for tag in self.check_all_tags_with_json():  # checa se o post já existe em qualquer json já feito
            json_filename = self.get_json_path(tag)
            if os.path.exists(json_filename):
                with open(json_filename, "r", encoding="utf-8") as f:
                    try:
                        all_data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Erro ao ler o arquivo {json_filename}.")
                        return False
                    except Exception as e:
                        print(
                            f"Erro inesperado ao ler o arquivo {json_filename}: {e}")
                        return False
                for saved_post in all_data:
                    if repr(self.normalize_text(saved_post["descricao"])) == repr(self.normalize_text(post_description)):
                        print("repr do salvo:", repr(saved_post["descricao"]))
                        print("repr do novo:", repr(post_description))
                        print("iguais?", self.normalize_text(saved_post["descricao"]) == self.normalize_text(post_description))
                        print("Post já existe em um json")
                        print(saved_post["descricao"])
                        print(post_description)
                        if return_post:
                            return saved_post
                        return True
        return False

    def substitute_post(self, new_post_data, old_post_data):
        # substitui old_post_data por new_post_data no json correto
        for tag in self.check_all_tags_with_json():
            json_filename = self.get_json_path(tag)
            if os.path.exists(json_filename):
                with open(json_filename, "r", encoding="utf-8") as f:
                    try:
                        all_data = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Erro ao ler o arquivo {json_filename}.")
                        return
                    except Exception as e:
                        print(
                            f"Erro inesperado ao ler o arquivo {json_filename}: {e}")
                        return
                for i, saved_post in enumerate(all_data):
                    if saved_post["descricao"] == old_post_data["descricao"]:
                        all_data[i] = new_post_data
                        with open(json_filename, "w", encoding="utf-8") as f:
                            json.dump(
                                all_data, f, ensure_ascii=False, indent=4)
                        print(f"Post substituído no arquivo {json_filename}.")
                        return
        print("Post antigo não encontrado para substituição.")

    # pega todos os jsons e junta em um só

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
                        print(
                            f"Erro ao ler o arquivo {json_filename}, pulando.")
                    except Exception as e:
                        print(
                            f"Erro inesperado ao ler o arquivo {json_filename}: {e}, pulando.")

        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"Todos os posts mesclados salvos em {output_filename}.")
