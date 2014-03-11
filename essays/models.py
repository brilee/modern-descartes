from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode(self.name)


class Essay(models.Model):
    title = models.CharField(max_length=100, help_text="Title of essay")
    slug = models.SlugField(max_length=100, help_text="URL to be used for essay. Must not contain spaces")
    content = models.TextField()
    category = models.ForeignKey(Category)
    date_written = models.DateField()
    legacy_redirect = models.IntegerField(blank=True, null=True, unique=True)

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return unicode("/essays/%s" % self.slug)

    class Meta:
        ordering = ['-date_written']
