# Generated by Django 4.2.2 on 2023-09-04 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_conversation_id_alter_message_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='conversation',
            new_name='conversation_id',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='sender',
            new_name='sender_id',
        ),
    ]