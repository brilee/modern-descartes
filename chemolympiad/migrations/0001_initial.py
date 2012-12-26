# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Competition'
        db.create_table('chemolympiad_competition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('chemolympiad', ['Competition'])

        # Adding model 'Question'
        db.create_table('chemolympiad_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chemolympiad.Competition'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('chemolympiad', ['Question'])

        # Adding M2M table for field topics on 'Question'
        db.create_table('chemolympiad_question_topics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm['chemolympiad.question'], null=False)),
            ('topic', models.ForeignKey(orm['chemolympiad.topic'], null=False))
        ))
        db.create_unique('chemolympiad_question_topics', ['question_id', 'topic_id'])

        # Adding model 'Subfield'
        db.create_table('chemolympiad_subfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('chemolympiad', ['Subfield'])

        # Adding model 'Topic'
        db.create_table('chemolympiad_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('chemolympiad', ['Topic'])

        # Adding M2M table for field subfield on 'Topic'
        db.create_table('chemolympiad_topic_subfield', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topic', models.ForeignKey(orm['chemolympiad.topic'], null=False)),
            ('subfield', models.ForeignKey(orm['chemolympiad.subfield'], null=False))
        ))
        db.create_unique('chemolympiad_topic_subfield', ['topic_id', 'subfield_id'])


    def backwards(self, orm):
        # Deleting model 'Competition'
        db.delete_table('chemolympiad_competition')

        # Deleting model 'Question'
        db.delete_table('chemolympiad_question')

        # Removing M2M table for field topics on 'Question'
        db.delete_table('chemolympiad_question_topics')

        # Deleting model 'Subfield'
        db.delete_table('chemolympiad_subfield')

        # Deleting model 'Topic'
        db.delete_table('chemolympiad_topic')

        # Removing M2M table for field subfield on 'Topic'
        db.delete_table('chemolympiad_topic_subfield')


    models = {
        'chemolympiad.competition': {
            'Meta': {'object_name': 'Competition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'chemolympiad.question': {
            'Meta': {'ordering': "['competition', '-year']", 'object_name': 'Question'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chemolympiad.Competition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['chemolympiad.Topic']", 'symmetrical': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'chemolympiad.subfield': {
            'Meta': {'object_name': 'Subfield'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'chemolympiad.topic': {
            'Meta': {'ordering': "['name']", 'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'subfield': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['chemolympiad.Subfield']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['chemolympiad']