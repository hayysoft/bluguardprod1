# Generated by Django 3.2 on 2021-06-18 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0008_delete_employee'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TblAcknowledgement',
        ),
        migrations.DeleteModel(
            name='TblAlert',
        ),
        migrations.DeleteModel(
            name='TblAlertCode',
        ),
        migrations.DeleteModel(
            name='TblCrestPatient',
        ),
        migrations.DeleteModel(
            name='TblDailySurvey',
        ),
        migrations.DeleteModel(
            name='TblDevice',
        ),
        migrations.DeleteModel(
            name='TblDeviceRawLength',
        ),
        migrations.DeleteModel(
            name='TblGateway',
        ),
        migrations.DeleteModel(
            name='TblIncoming',
        ),
        migrations.DeleteModel(
            name='TblMessage',
        ),
        migrations.DeleteModel(
            name='TblOrganization',
        ),
        migrations.DeleteModel(
            name='TblSubscription',
        ),
        migrations.DeleteModel(
            name='TblUser',
        ),
        migrations.DeleteModel(
            name='TblWearer',
        ),
    ]
