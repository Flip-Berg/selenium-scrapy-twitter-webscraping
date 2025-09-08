class TagSaver:
    def __init__(self):
        self.saved_tags = []

    def save_tag(self, tag):
        self.saved_tags.append(tag)

    def is_tag_saved(self, tag):
        # Lógica para verificar se a tag já foi salva
        for saved_tag in self.saved_tags:
            if saved_tag == tag:
                return True
        return False
    
    def get_saved_tags(self):
        return self.saved_tags
    
    def get_current_tag(self):
        if self.saved_tags:
            return self.saved_tags[-1]
        return None
