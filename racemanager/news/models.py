import datetime
from model_utils import Choices
from model_utils.models import StatusModel
from model_utils.fields import SplitField

from django.db import models



class Story(StatusModel):
    STATUS = Choices('draft', 'published')
    headline = models.CharField(
        max_length=200,
        help_text='Limited to 200 characters.',
        default=''
    )
    slug = models.SlugField(
        help_text='Will populate from title field.',
        unique_for_year='pub_date'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
    body = SplitField(
        help_text='No HTML allowed. Use Markdown for formatting.',
        default=''
    )

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.headline

    @models.permalink
    def get_absolute_url(self):
        return (
            'news_entry_detail',
            (),
            {'year': self.pub_date.strftime('%Y'),
            'month': self.pub_date.strftime('%b').lower(),
            'date': self.pub_date.strftime('%d'),
            'slug': self.slug})
