# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_db_views.db_view import DBView

class Interface(models.Model):
    eq_ip = models.OneToOneField('Equipment', models.DO_NOTHING, db_column='eq_ip', primary_key=True)
    if_index = models.IntegerField()
    name = models.CharField(max_length=254)
    mac_addr = models.CharField(max_length=64)
    alias = models.CharField(max_length=64)
    descr = models.CharField(unique=True, max_length=254)
    speed = models.TextField()
    if_ip = models.CharField(unique=True, max_length=64)
    admin_status = models.IntegerField()
    oper_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'interface'
        unique_together = (('eq_ip', 'if_index'),)


class Pretreatment(models.Model):
    pr_num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='eq_ip')
    index_pre = models.IntegerField()
    pr_date = models.DateTimeField()
    in_traffic = models.TextField()
    out_traffic = models.TextField()
    in_packet = models.TextField()
    out_packet = models.TextField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Pretreatment'


class AuthPermission(models.Model):
    user_id = models.CharField(unique=True, max_length=32, blank=True, null=True)
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    
    user_id = models.CharField(unique=True, max_length=32, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    charge = models.CharField(max_length=32, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    team = models.CharField(max_length=32, blank=True, null=True)
    position = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    grade = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    date_joined = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class DayPerformance(models.Model):
    num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='eq_ip')
    pr_date = models.DateTimeField()
    cpu_use = models.IntegerField()
    memory_use = models.IntegerField()
    disk_use = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'day_performance'


class DayStatistics(models.Model):
    num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='eq_ip')
    if_index = models.IntegerField()
    st_date = models.DateTimeField()
    now_in_traffic = models.TextField(blank=True, null=True)
    now_in_packet = models.TextField(blank=True, null=True)
    now_out_traffic = models.TextField(blank=True, null=True)
    now_out_packet = models.TextField(blank=True, null=True)
    max_in_traffic = models.TextField(blank=True, null=True)
    max_in_packet = models.TextField(blank=True, null=True)
    max_out_traffic = models.TextField(blank=True, null=True)
    max_out_packet = models.TextField(blank=True, null=True)
    avg_in_traffic = models.TextField(blank=True, null=True)
    avg_in_packet = models.TextField(blank=True, null=True)
    avg_out_traffic = models.TextField(blank=True, null=True)
    avg_out_packet = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'day_statistics'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EquipPerformance(models.Model):
    eq_pe_num = models.BigAutoField(primary_key=True)
    eq_ip = models.ForeignKey('Equipment', models.DO_NOTHING, db_column='eq_ip', blank=True, null=True)
    record_date = models.DateTimeField()
    cpu_use = models.CharField(max_length=63, blank=True, null=True)
    memory_use = models.IntegerField()
    disk_use = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'equip_performance'

class Equipment(models.Model):
    eq_ip = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=254)
    vendor = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    descr = models.CharField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=254)
    manage = models.CharField(max_length=64, blank=True, null=True)
    team = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment'

class Code(models.Model):
    num = models.AutoField(primary_key=True)
    codetype = models.CharField(max_length=32)
    code_value = models.CharField(max_length=64)
    name = models.CharField(max_length=128, blank=True, null=True)
    upper_codetype = models.CharField(max_length=32, blank=True, null=True)
    upper_code = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'code'

class User_Code(DBView):
    user_id = models.CharField(unique=True, max_length=32, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    charge = models.CharField(max_length=32, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    team = models.CharField(max_length=32, blank=True, null=True)
    position = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    grade = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    date_joined = models.CharField(max_length=32, blank=True, null=True)

    view_definition = """
        create view user_code as
        select a.user_id, a.password, a.username, a.position, a.email, a.grade, a.phone, a.date_joined,
        a.charge, a.team
        from auth_user a
        left outer join code cmanage on a.charge = cmanage.code_value 
        and cmanage.codetype = 'com_manage'
        left outer join code cteam on a.team = cteam.code_value 
        and cteam.codetype = 'com_team'
        left outer join code cposition on a.position = cposition.code_value 
        and cposition.codetype = 'com_rank'
        left outer join code cgrade on a.grade = cgrade.code_value 
        and cgrade.codetype ='com_admin';
        """
        
    class Meta:
        managed = False
        db_table = 'user_code'


class Equipment_Code(DBView):
    eq_ip = models.CharField(primary_key=True, max_length=64)
    vnd_name = models.CharField(max_length=254)
    mdl_name = models.CharField(max_length=254)
    vendor = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    vnd_codetype = models.CharField(max_length=32)
    mdl_codetype = models.CharField(max_length=32)
    descr = models.CharField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=254)
    equip_manage = models.CharField(max_length=64, blank=True, null=True)
    equip_team = models.CharField(max_length=64, blank=True, null=True)
    equip_name = models.CharField(max_length=32)


    view_definition = """
        create view equip_code as
        select equipment.eq_ip, vnd.name as vnd_name, vnd.codetype as vnd_codetype, 
        mdl.name as mdl_name, mdl.codetype as mdl_codetype, equipment.descr, equipment.location,
        equipment.name as equip_name, equipment.vendor, equipment.manage, equipment.team, equipment.model
        from equipment 
        left outer join code vnd on equipment.vendor = vnd.code_value
        and vnd.codetype = 'com_vender' 
        left outer join code mdl on equipment.model = mdl.code_value
        and mdl.codetype = 'com_model';
        """

    class Meta:
        managed = False
        db_table = 'equip_code'

class Day_Traffic(DBView):
    st_date = models.DateTimeField()
    eq_ip = models.CharField(primary_key=True, max_length=64)
    descr = models.CharField(max_length=254, blank=True, null=True)
    if_index = models.IntegerField()
    now_in_traffic = models.TextField(blank=True, null=True)
    now_in_packet = models.TextField(blank=True, null=True)
    now_out_traffic = models.TextField(blank=True, null=True)
    now_out_packet = models.TextField(blank=True, null=True)
    max_in_traffic = models.TextField(blank=True, null=True)
    max_in_packet = models.TextField(blank=True, null=True)
    max_out_traffic = models.TextField(blank=True, null=True)
    max_out_packet = models.TextField(blank=True, null=True)
    avg_in_traffic = models.TextField(blank=True, null=True)
    avg_in_packet = models.TextField(blank=True, null=True)
    avg_out_traffic = models.TextField(blank=True, null=True)
    avg_out_packet = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'day_traffic'

class Traffic(DBView):
      eq_ip = models.CharField(primary_key=True, max_length=64)
      tr_date = models.DateTimeField(blank=True, null=True)
      in_traffic = models.IntegerField(max_length=254)

      class Meta:
          managed = False
          db_table = 'traffic'

class EquipmentSnmpsetting(models.Model):
    eq_ip = models.OneToOneField(Equipment, models.DO_NOTHING, db_column='eq_ip', primary_key=True)
    read_community = models.CharField(max_length=8)
    write_community = models.CharField(max_length=8)
    snmp_port = models.IntegerField()
    snmptrap_port = models.IntegerField()
    snmp_version = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipment_snmpsetting'

class Event(models.Model):
    num = models.AutoField(primary_key=True)
    type = models.CharField(max_length=64)
    grade = models.CharField(max_length=64)
    ev_contents = models.CharField(max_length=256)
    occur = models.DateTimeField()
    count = models.IntegerField()
    id = models.CharField(max_length=64, blank=True, null=True)
    eq_ip = models.CharField(max_length=64)
    if_index = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'event'


class MonthPerformance(models.Model):
    num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='eq_ip')
    pr_date = models.DateTimeField()
    cpu_use = models.IntegerField()
    memory_use = models.IntegerField()
    disk_use = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'month_performance'


class MonthStatistics(models.Model):
    num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='eq_ip')
    index_month = models.IntegerField()
    date = models.DateTimeField()
    now_in_traffic = models.TextField(blank=True, null=True)
    now_in_packet = models.TextField(blank=True, null=True)
    now_out_traffic = models.TextField(blank=True, null=True)
    now_out_packet = models.TextField(blank=True, null=True)
    max_in_traffic = models.TextField(blank=True, null=True)
    max_in_packet = models.TextField(blank=True, null=True)
    max_out_traffic = models.TextField(blank=True, null=True)
    max_out_packet = models.TextField(blank=True, null=True)
    avg_in_traffic = models.TextField(blank=True, null=True)
    avg_in_packet = models.TextField(blank=True, null=True)
    avg_out_traffic = models.TextField(blank=True, null=True)
    avg_out_packet = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'month_statistics'


class Notice(models.Model):
    no_num = models.AutoField(primary_key=True)
    id = models.CharField(max_length=64)
    write_date = models.DateTimeField()
    title = models.CharField(max_length=32)
    no_contents = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'notice'


class NoticeReply(models.Model):
    re_num = models.AutoField(primary_key=True)
    no_num = models.IntegerField()
    id = models.CharField(max_length=64)
    write_date = models.DateTimeField()
    no_re_num = models.IntegerField(blank=True, null=True)
    re_contents = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'notice_reply'


class SnmpTraffic(models.Model):
    tr_num = models.BigAutoField(primary_key=True)
    eq_ip = models.CharField(max_length=64, blank=True, null=True)
    if_index = models.IntegerField()
    tr_date = models.DateTimeField(blank=True, null=True)
    in_traffic = models.TextField()
    in_packet = models.TextField()
    out_traffic = models.TextField()
    out_packet = models.TextField()

    class Meta:
        managed = False
        db_table = 'snmp_traffic'
        unique_together = (('eq_ip', 'if_index', 'tr_date'),)


class WeekPerformance(models.Model):
    num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='eq_ip')
    pr_date = models.DateTimeField()
    cpu_use = models.IntegerField()
    memory_use = models.IntegerField()
    disk_use = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'week_performance'


class WeekStatistics(models.Model):
    num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='eq_ip')
    if_index = models.IntegerField()
    st_date = models.DateTimeField()
    now_in_traffic = models.TextField(blank=True, null=True)
    now_in_packet = models.TextField(blank=True, null=True)
    now_out_traffic = models.TextField(blank=True, null=True)
    now_out_packet = models.TextField(blank=True, null=True)
    max_in_traffic = models.TextField(blank=True, null=True)
    max_in_packet = models.TextField(blank=True, null=True)
    max_out_traffic = models.TextField(blank=True, null=True)
    max_out_packet = models.TextField(blank=True, null=True)
    avg_in_traffic = models.TextField(blank=True, null=True)
    avg_in_packet = models.TextField(blank=True, null=True)
    avg_out_traffic = models.TextField(blank=True, null=True)
    avg_out_packet = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'week_statistics'


class YearPerformance(models.Model):
    num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='eq_ip')
    pr_date = models.DateTimeField()
    cpu_use = models.IntegerField()
    memory_use = models.IntegerField()
    disk_use = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'year_performance'


class YearStatistics(models.Model):
    num = models.AutoField(primary_key=True)
    eq_ip = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='eq_ip')
    index_year = models.IntegerField()
    date = models.DateTimeField()
    now_in_traffic = models.TextField(blank=True, null=True)
    now_in_packet = models.TextField(blank=True, null=True)
    now_out_traffic = models.TextField(blank=True, null=True)
    now_out_packet = models.TextField(blank=True, null=True)
    max_in_traffic = models.TextField(blank=True, null=True)
    max_in_packet = models.TextField(blank=True, null=True)
    max_out_traffic = models.TextField(blank=True, null=True)
    max_out_packet = models.TextField(blank=True, null=True)
    avg_in_traffic = models.TextField(blank=True, null=True)
    avg_in_packet = models.TextField(blank=True, null=True)
    avg_out_traffic = models.TextField(blank=True, null=True)
    avg_out_packet = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'year_statistics'
