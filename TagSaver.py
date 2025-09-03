class TagSaver:
    def __init__(self):
        self.saved_tags = []

    def save_tag(self, tag):
        self.saved_tags.append(tag.text)
        self.saved_tags.append(tag)

    def is_tag_saved(self, tag):
        # Lógica para verificar se a tag já foi salva
        for saved_tag in self.saved_tags:
            if saved_tag == tag:
                return True
        return False
