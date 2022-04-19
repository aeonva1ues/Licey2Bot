class CreatingAdminsNews:
    def __init__(self):
        self.news_header = 'None'
        self.news_body = 'None'
        self.news_head_emoji = 'None'
        self.news_body_emoji = 'None'
        self.news_tag = '#новости_лицея'
        self.news_content = 'None'
        self.news_author = 'None'
        self.news_image_path = 'None'
    def createNews(self):
        self.news_content = f'{str(self.news_head_emoji)} {str(self.news_header)}\n{str(self.news_body_emoji)} {str(self.news_body)}\n\n\n✏️ Автор: {str(self.news_author)}\n{str(self.news_tag)}'