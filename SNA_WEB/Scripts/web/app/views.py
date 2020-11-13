from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from app.models import Equipment, EquipmentSnmpsetting, Interface, AuthUser, Code, EquipPerformance, SnmpTraffic, Equipment_Code, User_Code, Day_Traffic, MonthStatistics, WeekStatistics, YearStatistics, DayStatistics, Traffic


from django.http import JsonResponse # JSON 응답
from django.forms.models import model_to_dict

def index(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        try:    
            auth_user = AuthUser.objects.get(user_id = user_id, password = password)
            request.session['user_id'] = user_id
            
            return render(request, 'app/login_success.html')
        except:
            return render(request, 'app/login_fail.html')
    return render(request, 'app/index.html')
    
def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        username = request.POST.get('username')
        last_login = request.POST.get('last_login')
        charge = request.POST.get('charge')
        team = request.POST.get('team')
        position = request.POST.get('position')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        phone = request.POST.get('phone')
        date_joined = request.POST.get('date_joined')
        try:
            auth_user = AuthUser(user_id=user_id, password=password, username=username,
            last_login=last_login, charge=charge, team=team, position=position, email=email, grade=grade, phone=phone, date_joined=date_joined)
            request.session['username'] = username
            auth_user.save()
            request.session['username'] = username
            return render(request, 'app/index.html')
        except:
            return render(request, 'app/signup.html')
    return render(request, 'app/signup.html')

def dashboard(request):
    # auth_user = AuthUser.objects.order_by('-id')
    # context = {
    #     'auth_user' : auth_user
    # }
    # template = loader.get_template('app/dashboard.html')
    # return HttpResponse(template.render(context, request))
    # equipment = Equipment.objects.first()
    traffic = Traffic.objects.order_by('-tr_date')
    equipment = Equipment.objects.order_by('-eq_ip')
    context = {
        'traffic' : traffic,
        'equipment' : equipment
    }
    template = loader.get_template('app/dashboard.html')
    return HttpResponse(template.render(context, request))


def user(request):
    user_code = User_Code.objects.order_by('-user_id')
    context = {
        'user_code' : user_code,
    }
    template = loader.get_template('app/user.html')
    return HttpResponse(template.render(context, request))

def sidebar(request):
    auth_user = AuthUser.objects.order_by('-id')
    context = {
        'auth_user' : auth_user
    }
    template = loader.get_template('app/sidbar.html')
    return HttpResponse(template.render(context, request))

def vendor_model(request):
    code = Code.objects.order_by('-num')
    context = {
        'code' : code
    }
    template = loader.get_template('app/vendor_model.html')
    return HttpResponse(template.render(context, request))

def team(request):
    user_code = User_Code.objects.order_by('-user_id')
    context = {
        'user_code' : user_code,
    }
    template = loader.get_template('app/team.html')
    return HttpResponse(template.render(context, request))


def interface(request):
    interface = Interface.objects.order_by('-eq_ip')
    context = {
        'interface' : interface
    }
    template = loader.get_template('app/interface.html')
    return HttpResponse(template.render(context, request))

def device_performance(request):
    equip_performance = EquipPerformance.objects.prefetch_related('eq_pe_num').all()
    equip_performance = EquipPerformance.objects.order_by('-eq_ip')
    context = {
        'equip_performance' : equip_performance
    }
    template = loader.get_template('app/device_performance.html')
    return HttpResponse(template.render(context, request))

def traffic(request):
    # day_traffic = Day_Traffic.objects.order_by('-eq_ip')
    day_statistics = DayStatistics.objects.order_by('-eq_ip')
    # month_statistics = MonthStatistics.objects.order_by('-eq_ip')
    week_statistics = WeekStatistics.objects.order_by('-eq_ip')
    # year_statistics = YearStatistics.objects.order_by('-eq_ip')
    context = {
        # 'day_traffic' : day_traffic,
        'day_statistics' : day_statistics,
        # 'month_statistics' : month_statistics,
        'week_statistics' : week_statistics,
        # 'year_statistics' : year_statistics
    }
    template = loader.get_template('app/traffic.html')
    return HttpResponse(template.render(context, request))

def cur_faults(request):
    context = {}
    template = loader.get_template('app/cur_faults.html')
    return HttpResponse(template.render(context, request)) 

def faults_history(request):
    context = {}
    template = loader.get_template('app/faults_history.html')
    return HttpResponse(template.render(context, request)) 

def critical(request):
    context = {}
    template = loader.get_template('app/critical.html')
    return HttpResponse(template.render(context, request)) 

def vendor_model_register(request):
    if request.method == 'POST':
        codetype = request.POST.get('codetype')
        code_value = request.POST.get('code_value')
        # name = request.POST.get('name')
        # upper_codetype = request.POST.get('upper_codetype')
        # upper_code = request.POST.get('upper_code')

        try:
            code = Code(codetype=codetype, code_value=code_value)
            # name=name, upper_codetype=upper_codetype, upper_code=upper_code)
            code.save()
            return render(request, 'app/vendor_model.html')
        except:
            return render(request, 'app/index.html')
    return render(request, 'app/vendor_model_register.html')

def team_register(request):
    if request.method == 'POST':   
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        username = request.POST.get('username')
        # last_login = request.POST.get('last_login')
        charge = request.POST.get('charge')
        team = request.POST.get('team')
        position = request.POST.get('position')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        phone = request.POST.get('phone')
        date_joined = request.POST.get('date_joined')
        try:
            auth_user = AuthUser(user_id=user_id, password=password, username=username, charge=charge, team=team, position=position, email=email, grade=grade, phone=phone, date_joined=date_joined)
            auth_user.save()
            return render(request, 'app/team.html')
        except:
            return render(request, 'app/dashboard.html')
    return render(request, 'app/team_register.html')

def user_register(request):
    if request.method == 'POST':   
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        username = request.POST.get('username')
        # last_login = request.POST.get('last_login')
        charge = request.POST.get('charge')
        team = request.POST.get('team')
        position = request.POST.get('position')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        phone = request.POST.get('phone')
        date_joined = request.POST.get('date_joined')
        try:
            auth_user = AuthUser(user_id=user_id, password=password, username=username, charge=charge, team=team, 
            position=position, email=email, grade=grade, phone=phone, date_joined=date_joined)
            auth_user.save()
            return render(request, 'app/user_register_success.html')
        except:
            return render(request, 'app/user_register_fail.html')
    return render(request, 'app/user_register.html')



def device_register(request):
    if request.method == 'POST':
        eq_ip = request.POST.get('eq_ip')
        name = request.POST.get('name')
        vendor = request.POST.get('vendor')
        model = request.POST.get('model')
        descr = request.POST.get('descr')
        location = request.POST.get('location')
        manage = request.POST.get('manage')
        team = request.POST.get('team')

        try:
            equipment = Equipment(eq_ip=eq_ip, name=name, vendor=vendor, model=model, manage=manage, team=team, descr=descr, location=location)
            equipment.save()
            
            return render(request, 'app/device.html')
        except:
            return render(request, 'app/index.html')
    return render(request, 'app/device_register.html')

def vendor_model_change(request, num):
    code = Code.objects.get(num=num)

    if request.method == 'POST':
        codetype = request.POST.get('codetype')
        code_value = request.POST.get('code_value')
        name = request.POST.get('name')
        # upper_codetype = request.POST.get('upper_codetype')
        # upper_code = request.POST.get('upper_code')

        try:
            code.codetype = codetype
            code.code_value = code_value
            code.name = name
            # code.upper_codetype = upper_codetype
            # code.upper_code = upper_code
            code.save()
            return render(request, 'app/vendor_model.html')
        except:
            return render(request, 'app/index.html')
    context = {
        'code' : code
    }
    return render(request, 'app/vendor_model_change.html', context)

def device_change(request, eq_ip):
    equipment = Equipment.objects.get(eq_ip=eq_ip)
    # equipment_snmpsetting = EquipmentSnmpsetting(eq_ip=eq_ip)

    if request.method == 'POST':
        eq_ip = request.POST.get('eq_ip')
        name = request.POST.get('name')
        vendor = request.POST.get('vendor')
        model = request.POST.get('model')
        descr = request.POST.get('descr')
        location = request.POST.get('location')
        manage = request.POST.get('manage')
        team = request.POST.get('team')

        # eq_ip = request.POST.get('eq_ip')
        # read_community = request.POST.get('read_community')
        # write_community = request.POST.get('write_community')
        # snmp_port = request.POST.get('snmp_port')
        # snmptrap_port = request.POST.get('snmptrap_port')
        # snmp_version = request.POST.get('snmp_version')
        try:
            equipment.eq_ip = eq_ip
            equipment.name = name
            equipment.vendor = vendor
            equipment.model = model
            equipment.descr = descr
            equipment.location = location
            equipment.manage = manage
            equipment.team = team
            equipment.save()

            # equipment_snmpsetting.eq_ip = eq_ip
            # equipment_snmpsetting.read_community = read_community
            # equipment_snmpsetting.write_community = write_community
            # equipment_snmpsetting.snmp_port = snmp_port
            # equipment_snmpsetting.snmptrap_port = snmptrap_port
            # equipment_snmpsetting.snmp_version = snmp_version
            
            # equipment_snmpsetting.save()
            return render(request, 'app/device.html')
        except:
            return render(request, 'app/index.html')
    context = {
        'equipment' : equipment
    }
    return render(request, 'app/device_change.html', context)

def user_change(request, user_id):
    user_code = User_Code.objects.get(user_id=user_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        username = request.POST.get('username')
        charge = request.POST.get('charge')
        team = request.POST.get('team')
        position = request.POST.get('position')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        phone = request.POST.get('phone')
        date_joined = request.POST.get('date_joined')
        try:
            user_code.user_id = user_id
            user_code.password = password
            user_code.username = username
            user_code.charge = charge
            user_code.team = team
            user_code.position = position
            user_code.email = email
            user_code.grade = grade
            user_code.phone = phone
            user_code.date_joined = date_joined
            user_code.save()
            return render(request, 'app/u_change.html')
        except:
            return render(request, 'app/user.html')
    context = {
        'user_code' : user_code
    }
    return render(request, 'app/user_change.html', context)

def user_delete(request, user_id):
    try:
        auth_user = AuthUser.objects.get(user_id = user_id)
        auth_user.delete()
        return render(request, 'app/u_delete.html')
    except:
        return render(request, 'app/user.html')

def device_delete(request, eq_ip):
    try:
        equipment = Equipment.objects.get(eq_ip=eq_ip)
        equipment.delete()
        return render(request, 'app/device.html')
    except:
        return render(request, 'app/index.html')

def vendor_model_delete(request, num):
    try:
        code = Code.objects.get(num=num)
        code.delete()
        return render(request, 'app/vendor_model.html')
    except:
        return render(request, 'app/index.html')

def equip_code(request):
    # try:
        equip_code = Equipment_Code.objects.raw('''
        select equipment.eq_ip, vnd.name, vnd.codetype, mdl.name, mdl.codetype, equipment.descr, equipment.location,
        equipment.name, equipment.vendor, equipment.manage, equipment.team
        from equipment 
        left outer join code vnd on equipment.vendor = vnd.code_value
        and vnd.codetype = 'com_vender' 
        left outer join code mdl on equipment.model = mdl.code_value
        and mdl.codetype = 'com_model';
        ''')
        print(equip_code)
        context = {
            'equip_code' : equip_code
        }
        template = loader.get_template('app/device.html')
        return HttpResponse(template.render(context, request))
    # except:
    #     return render(request, 'app/device.html')

        
def device(request):
    equipment = Equipment.objects.order_by('-eq_ip')
    context = {
        'equipment' : equipment
    }
    template = loader.get_template('app/device.html')
    return HttpResponse(template.render(context, request))

def team_change(request, user_id):
    user_code = User_Code.objects.get(user_id=user_id)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        username = request.POST.get('username')
        # last_login = request.POST.get('last_login')
        charge = request.POST.get('charge')
        team = request.POST.get('team')
        position = request.POST.get('position')
        email = request.POST.get('email')
        grade = request.POST.get('grade')
        phone = request.POST.get('phone')
        date_joined = request.POST.get('date_joined')
        try:
            user_code.user_id = user_id
            user_code.password = password
            user_code.username = username
            # auth_user.last_login = last_login
            user_code.charge = charge
            user_code.team = team
            user_code.position = position
            user_code.email = email
            user_code.grade = grade
            user_code.phone = phone
            user_code.date_joined = date_joined
            user_code.save()
            return render(request, 'app/team.html')
        except:
            return render(request, 'app/dashboard.html')
    context = {
        'user_code' : user_code
    }
    return render(request, 'app/team_change.html', context)

def team_delete(request, user_id):
    try:
        auth_user = AuthUser.objects.get(user_id=user_id)
        auth_user.delete()
        return render(request, 'app/delete.html')
    except:
        return render(request, 'app/index.html')