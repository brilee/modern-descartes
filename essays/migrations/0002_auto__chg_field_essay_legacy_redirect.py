# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Essay.legacy_redirect'
        db.alter_column(u'essays_essay', 'legacy_redirect', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'Essay.legacy_redirect'
        db.alter_column(u'essays_essay', 'legacy_redirect', self.gf('django.db.models.fields.IntegerField')(default=None))

    models = {
        u'essays.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'essays.essay': {
            'Meta': {'ordering': "['-date_written']", 'object_name': 'Essay'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['essays.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_written': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_redirect': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['essays']