from parsel import Selector
import JsonManager


class Scraper:

    def get_credentials(self):
        # credenciais
        with open("credenciais.xml", "r", encoding="utf-8") as f:
            credenciais = f.read()

        sel = Selector(text=credenciais)
        # Extrai o texto das tags <email> e <senha>
        email = sel.xpath("//instagram/email/text()").get()
        senha = sel.xpath("//instagram/senha/text()").get()
        return email, senha

    def scrape_post_text(self, post_html, tag, JsonManager, saved_post=None):
        post_selector = Selector(text=post_html)

        # [role="presentation"] div > h1::text
        post_description = post_selector.xpath('string(.//h1)').get()
        # Mantém espaços e apenas limpa quebras de linha excessivas
        #print("Descrição do post(scraper):")
        #print(repr(post_description))
        comment_blocks = post_selector.css(':not(li) > ul')[1:]

        comments = []
        for comment_block in comment_blocks:
            comment_text = comment_block.xpath(
                'string(.//h3/following-sibling::div/span)').get()
            # ignora não comentários
            if comment_text.endswith("ResponderOpções de comentários"):
                continue
            # respostas associadas a esse comentário
            replies_block = comment_block.xpath('.//ul[1]')
            replies_text = []
            for reply in replies_block.xpath('.//h3/following-sibling::div/span'):
                reply_text = reply.xpath('string()').get()
                # ignora vazios e não comentários
                if reply_text and not reply_text.endswith("ResponderOpções de comentários"):
                    replies_text.append(reply_text)

            if comment_text:  # ignora comentários vazios
                comments.append({
                    "comentario": comment_text,
                    "respostas": replies_text
                })

        post_data = {
            "descricao": post_description if post_description else "",
            "comentarios": comments if comments else []
        }
        if post_data["descricao"] == "" and post_data["comentarios"] == "":
            print("Post vazio, não será salvo.")
            return  
        if saved_post:
            is_post_bigger = self.check_if_post_is_bigger(
                post_data, saved_post)
            if is_post_bigger is True:
                print(
                    "Post é maior que o salvo anteriormente, substituindo post antigo.")
                JsonManager.substitute_post(post_data, saved_post)
            else: 
                print("Post atual não é maior que o salvo anteriormente, não será salvo.")
        else:
            return JsonManager.save_on_json(tag, post_data)

    def check_if_post_is_bigger(self, current_post, saved_post):
        # Compara o total de comentários + respostas
        def total_comments_and_replies(comments):
            if not comments:
                return 0
            total = 0
            for c in comments:
                total += 1  # conta o comentário principal
                respostas = c.get("respostas", [])
                if respostas:
                    total += len(respostas)
            return total

        current_comments = current_post["comentarios"]
        saved_comments = saved_post["comentarios"]
        return total_comments_and_replies(current_comments) > total_comments_and_replies(saved_comments)
