from parsel import Selector
import JsonManager

class Scraper:

    def get_credentials(self):
        #credenciais
        with open("credenciais.xml", "r", encoding="utf-8") as f:
            credenciais = f.read()

        sel = Selector(text=credenciais)
        # Extrai o texto das tags <email> e <senha>
        email = sel.xpath("//instagram/email/text()").get()
        senha =sel.xpath("//instagram/senha/text()").get()
        return email, senha
    

    def scrape_post_text(self, post_html, tag, JsonManager):
        post_selector = Selector(text=post_html)

        post_description = post_selector.xpath('string(.//h1)').get() #[role="presentation"] div > h1::text

        comment_blocks = post_selector.css(':not(li) > ul')[1:] 

        comments = []
        for comment_block in comment_blocks:
            comment_text = comment_block.xpath('string(.//h3/following-sibling::div/span)').get()
            if comment_text.endswith("ResponderOpções de comentários"): #ignora não comentários
                continue
            # respostas associadas a esse comentário
            replies_block = comment_block.xpath('.//ul[1]')
            replies_text = []
            for reply in replies_block.xpath('.//h3/following-sibling::div/span'):
                reply_text = reply.xpath('string()').get()
                if reply_text and not reply_text.endswith("ResponderOpções de comentários"):  # ignora vazios e não comentários
                    replies_text.append(reply_text)

            if comment_text: #ignora comentários vazios
                comments.append({
                    "comentario": comment_text,
                    "respostas": replies_text
                })

        post_data = {
            "descricao": post_description if post_description else "",
            "comentarios": comments if comments else ""
        }
        if post_data["descricao"] == "" and post_data["comentarios"] == "":
            return #post vazio, não é salvo.
        JsonManager.save_on_json(tag, post_data)