# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'essays_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'essays', ['Category'])

        # Adding model 'Essay'
        db.create_table(u'essays_essay', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['essays.Category'])),
            ('date_written', self.gf('django.db.models.fields.DateField')()),
            ('legacy_redirect', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal(u'essays', ['Essay'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'essays_category')

        # Deleting model 'Essay'
        db.delete_table(u'essays_essay')


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
            'legacy_redirect': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['essays']