from datetime import date, timedelta
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from Register_Login.models import *

# Create your views here.

def distributor_dashboard(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
    # dash_details = DistributorDetails.objects.get(id=pk,superadmin_approval=1)
    context = {
        'distributor_details': distributor_det
    }
    return render(request, 'distributor_dash.html', context)

def dist_clients(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
    return render(request,'dist_clients.html',{'distributor_details':distributor_det})

def dist_client_requests(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        clients = CompanyDetails.objects.filter(Distributor_approval=0,distributor=distributor_det).order_by('-id')
    return render(request,'dist_client_requests.html',{'distributor_details':distributor_det,'clients':clients})

def dist_client_accept(request,id):
  data=CompanyDetails.objects.filter(id=id).update(Distributor_approval=1,superadmin_approval=1)
  return redirect('dist_client_requests')

def dist_client_reject(request,id):
  data=CompanyDetails.objects.get(id=id)
  data.login_details.delete()
  data.delete()
  return redirect('dist_client_requests')

def dist_client_request_overview(request,id):
  if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        data=CompanyDetails.objects.get(id=id)
        allmodules=ZohoModules.objects.get(company=data,status='New')
        return render(request,'dist_client_request_overview.html',{'company':data,'allmodules':allmodules,'distributor_details':distributor_det})

def dist_all_clients(request):
  if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        clients=CompanyDetails.objects.filter(Distributor_approval=1,distributor=distributor_det)
        
        return render(request,'dist_all_clients.html',{'clients':clients,'distributor_details':distributor_det})

def dist_client_details(request,id):
  if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')   
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        data=CompanyDetails.objects.get(id=id)
        allmodules=ZohoModules.objects.get(company=data,status='New')
        return render(request,'dist_client_details.html',{'company':data,'allmodules':allmodules,'distributor_details':distributor_det})

def distributor_profile(request):
   if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor= DistributorDetails.objects.get(login_details=log_det)
        terms=PaymentTerms.objects.all()
   print(terms)
   return render(request,'distributor_profile.html',{'distributor_details':distributor,'terms':terms})

def dist_edit_profilePage(request,id):
  
  distributor = DistributorDetails.objects.get(id=id)
  terms=PaymentTerms.objects.all()
  print(terms)
  return render(request,'edit_distributor_profile.html',{'terms':terms,'distributor_details':distributor})

def update_distributor_profile(request,id):
    distributor = DistributorDetails.objects.get(id=id)

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['eid']
        username = request.POST['uname']
        phone = request.POST['phone']
        pic = request.FILES.get('profile_pic')


        login_data = LoginDetails.objects.get(id=distributor.login_details_id)
        login_data.first_name = fname
        login_data.last_name = lname
        login_data.email = email
        login_data.username = username
        login_data.save()

        distributor.contact = phone
        if pic:
            distributor.image = pic
        distributor.save()

    return redirect('distributor_profile')

# notifications------------------------------------

def distributor_notification(request):
  if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)

        end_date = distributor_det.End_date
        dist_days_remaining = (end_date - date.today()).days
        print('d',dist_days_remaining)

        companies = CompanyDetails.objects.filter(reg_action='distributor')

        for c in companies:
            c.days_remaining = (c.End_date - date.today()).days
            
        pterm_updation = PaymentTermsUpdates.objects.filter(update_action=1,status='Pending')
        data= ZohoModules.objects.filter(update_action=1,status='Pending')

        context ={'data':data,
                  'pterm_updation':pterm_updation,
                  'distributor_details':distributor_det,
                  'companies':companies,
                  'dist_days_remaining':dist_days_remaining
                  }
        
        return render(request,'distributor_notification.html',context)

def dist_module_updation_details(request,mid):
   if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        data= ZohoModules.objects.get(id=mid)
        allmodules= ZohoModules.objects.get(company=data.company,status='Pending')
        old_modules = ZohoModules.objects.get(company=data.company,status='New')

        return render(request,'module_updation_details.html',{'data':data,'allmodules':allmodules,'old_modules':old_modules,'distributor_details':distributor_det})

def dist_module_updation_ok(request,mid):
  
  old=ZohoModules.objects.get(company=mid,status='New')
  old.delete()

  data=ZohoModules.objects.get(company=mid,status='Pending')  
  data.status='New'
  data.save()
  data1=ZohoModules.objects.filter(company=mid).update(update_action=0)
  return redirect('distributor_notification')

def dist_pterm_updation_details(request,pid):
   if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)
        term= PaymentTermsUpdates.objects.get(id=pid)
        new_term= PaymentTermsUpdates.objects.get(company=term.company,status='Pending')
        old_term = PaymentTermsUpdates.objects.get(company=term.company,status='New')
        start_date = term.company.start_date
        end_date = term.company.End_date 
        current_date = date.today()
        difference_in_days = (end_date - current_date).days
        print(term)
        print(new_term)
        print(old_term)

        context = {
            'new_term':new_term,
            'old_term':old_term,
            'term':term,
            'difference_in_days':difference_in_days,
            'distributor_details':distributor_det
            }
        return render(request,'dist_pterm_updation_details.html',context)

def dist_pterm_updation_ok(request,cid):
  
  old_term=PaymentTermsUpdates.objects.get(company=cid,status='New')
  old_term.delete()

  new_term=PaymentTermsUpdates.objects.get(company=cid,status='Pending')  
  new_term.status='New'
  new_term.update_action=0
  new_term.save()

  terms = new_term.payment_term

  start_date=date.today()
  days=int(terms.days)
    
  end= date.today() + timedelta(days=days)
  End_date=end
  
  company = CompanyDetails.objects.get(id=cid)
  company.payment_term=terms
  company.start_date=start_date
  company.End_date=End_date
  company.save()
  return redirect('distributor_notification')


def dist_term_update_request(request):
    if 'login_id' in request.session:
        login_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/') 
        log_det = LoginDetails.objects.get(id=login_id)
        distributor_det = DistributorDetails.objects.get(login_details=log_det)

        tid = request.GET['term_id']
        new_payment_term = PaymentTerms.objects.get(id=tid)
        pterm_update = PaymentTermsUpdates(
            distributor = distributor_det,
            payment_term = new_payment_term,
            update_action = 1,
            status = 'Pending'
        )
        pterm_update.save()
        
        terms=PaymentTerms.objects.all()
        messages.success(request, 'Request has been sent successfully.')
        return redirect('distributor_profile')
    
