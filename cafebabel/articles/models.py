import datetime
import os
from hashlib import md5
from pathlib import Path

from mongoengine import signals

from .. import app, db
from ..core.helpers import slugify
from ..users.models import User


class Article(db.Document):
    title = db.StringField(required=True)
    slug = db.StringField(required=True)
    language = db.StringField(max_length=2, required=True)
    category = db.StringField()
    summary = db.StringField()
    body = db.StringField(required=True)
    image = db.StringField()
    status = db.StringField(default='draft')
    uid = db.UUIDField(binary=False, required=True)
    editor = db.ReferenceField(User, reverse_delete_rule=db.NULLIFY)
    author = db.ReferenceField(User, reverse_delete_rule=db.NULLIFY)
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)
    publication_date = db.DateTimeField()
    _upload_image = None

    def __str__(self):
        return self.title

    @property
    def is_draft(self):
        return self.status == 'draft'

    @property
    def is_published(self):
        return self.status == 'published'

    @property
    def image_url(self):
        if self.image:
            return f'{app.config.get("ARTICLES_IMAGES_URL")}/{self.image}'

    def delete_image(self):
        if not self.image:
            return
        Path(f'{app.config.get("ARTICLES_IMAGES_PATH")}/{self.image}').unlink()
        self.image = None
        self.save()

    def attach_image(self, image):
        if not image:
            return
        self._upload_image = image

    @classmethod
    def update_publication_date(cls, sender, article, **kwargs):
        if article.status == 'published' and not article.publication_date:
            article.publication_date = datetime.datetime.utcnow()

    @classmethod
    def update_slug(cls, sender, article, **kwargs):
        article.slug = slugify(article.title)

    @classmethod
    def generate_uid(cls, sender, article, **kwargs):
        if not article.uid:
            article.uid = os.urandom(16).hex()

    @classmethod
    def store_image(cls, sender, article, **kwargs):
        if article._upload_image:
            article.image = article.id
            article._upload_image.save(
                f'{app.config.get("ARTICLES_IMAGES_PATH")}/{article.image}')
            article._upload_image = None
            article.save()


signals.pre_save.connect(Article.generate_uid, sender=Article)
signals.pre_save.connect(Article.update_publication_date, sender=Article)
signals.pre_save.connect(Article.update_slug, sender=Article)
signals.post_save.connect(Article.store_image, sender=Article)
