# Generated by Django 3.0.8 on 2020-11-12 06:31

from django.db import migrations
import django_db_views.migration_functions
import django_db_views.operations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20201111_1739'),
    ]

    operations = [
        django_db_views.operations.ViewRunPython(
            code=django_db_views.migration_functions.ForwardViewMigration("create view user_code as\n        select a.user_id, a.password, a.username, a.position, a.email, a.grade, a.phone, a.date_joined,\n        a.charge, a.team\n        from auth_user a\n        left outer join code cmanage on a.charge = cmanage.code_value \n        and cmanage.codetype = 'com_manage'\n        left outer join code cteam on a.team = cteam.code_value \n        and cteam.codetype = 'com_team'\n        left outer join code cposition on a.position = cposition.code_value \n        and cposition.codetype = 'com_rank'\n        left outer join code cgrade on a.grade = cgrade.code_value \n        and cgrade.codetype ='com_admin'", 'user_code'),
            reverse_code=django_db_views.migration_functions.BackwardViewMigration('', 'user_code'),
            atomic=False,
        ),
    ]