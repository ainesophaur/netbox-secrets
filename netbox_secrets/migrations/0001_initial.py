# Generated by Django 4.0.8 on 2022-12-28 11:35

from django.conf import settings
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0077_customlink_extend_text_and_url'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserKey',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('public_key', models.TextField()),
                ('master_key_cipher', models.BinaryField(blank=True, max_length=512, null=True)),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_key', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__username'],
            },
        ),
        migrations.CreateModel(
            name='SessionKey',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cipher', models.BinaryField(max_length=512)),
                ('hash', models.CharField(editable=False, max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('userkey', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='session_key', to='netbox_secrets.userkey')),
            ],
            options={
                'ordering': ['userkey__user__username'],
            },
        ),
        migrations.CreateModel(
            name='SecretRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('assigned_object_id', models.PositiveIntegerField()),
                ('name', models.CharField(blank=True, max_length=100)),
                ('ciphertext', models.BinaryField(max_length=65568)),
                ('hash', models.CharField(editable=False, max_length=128)),
                ('assigned_object_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='secrets', to='contenttypes.contenttype')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='secrets', to='netbox_secrets.secretrole')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('role', 'name', 'pk'),
                'unique_together': {('assigned_object_type', 'assigned_object_id', 'role', 'name')},
            },
        ),
    ]