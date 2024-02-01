from datetime import date, timedelta
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login as auth_login
from . models import *
from Company_Staff.views import company_dashboard
from Distributor.views import distributor_dashboard
from Admin.views import admindash
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
import random
import string




# Create your views here.
def landing_page(request):
    return render(request,'landpage.html')


# ------------------Distributor registration and save---------------------


def distributor_register_page(request):
  terms = PaymentTerms.objects.all()
  return render(request, 'distributor_register.html',{'terms':terms})

def register(request):
  if request.method == 'POST':
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['eid']
    username = request.POST['uname']
    phone = request.POST['ph']
    password = request.POST['pass']
    confirm_pass = request.POST['cpass']
    pterm = request.POST['select']
    pic = request.FILES.get('image')

    terms=PaymentTerms.objects.get(id=pterm)
    start_date=date.today()
    days=int(terms.days)

    
    end= date.today() + timedelta(days=days)
    End_date=end

    code_length = 8  
    characters = string.ascii_letters + string.digits  # Letters and numbers
    while True:
      unique_code = ''.join(random.choice(characters) for _ in range(code_length))
        
      # Check if the code already exists in the table
      if not DistributorDetails.objects.filter(distributor_code=unique_code).exists():
        break
    
    if password == confirm_pass:
      if LoginDetails.objects.filter(username = username).exists():
        messages.info(request, 'Sorry, Username already exists')
        return redirect('distributor_register_page')
      

      elif not LoginDetails.objects.filter(email = email).exists():
      
        login_data =LoginDetails(
          first_name = fname,
          last_name = lname,
          username = username,
          email = email,
          password = password,
          user_type = 'Distributor'
        )
        login_data.save()
        
        data = LoginDetails.objects.get(id = login_data.id)
        distributor_data = DistributorDetails(
          login_details=data,
          payment_term=terms,
          contact=phone,
          distributor_code=unique_code,
          image=pic,
          start_date=start_date,
          End_date=End_date,
        )
        distributor_data.save()

        pterm_update = PaymentTermsUpdates(
          distributor = distributor_data,
          payment_term = terms
        )
        pterm_update.save()
        
        return redirect('login_page')
      else:
        messages.info(request, 'Sorry, Email already exists')
        return redirect('distributor_register_page')
    return redirect('distributor_register_page')



# ------------------Company registration and save-------------------------

def company_register_page1(request):
  return render(request, 'company_register.html')



def company_registration_save1(request):
  if request.method == 'POST':
    # Get data from the form
    first_name = request.POST.get('fname')
    last_name = request.POST.get('lname')
    email = request.POST.get('eid')
    username = request.POST.get('uname')
    password = request.POST.get('pass')
    cpassword = request.POST.get('cpass')
    self_distributor=request.POST.get('self_distributor')
    distributor_id = request.POST.get('did', None)  # It will be none  if not provided
    user_type = 'Company'

    if distributor_id != '':
      if DistributorDetails.objects.filter(distributor_code=distributor_id).exists():
        distributor_id=distributor_id
      else :
        messages.info(request, 'Sorry, Distributor id does not exists')
        return redirect('company_register_page1')

    if password == cpassword:
      if LoginDetails.objects.filter(email=email).exists():
        messages.info(request,'Email id exists')
        return redirect('company_register_page1')
      elif LoginDetails.objects.filter(username=username).exists():
        messages.info(request,'Username exists')
        return redirect('company_register_page1')
      else:
        # Save data to the database
        user = LoginDetails(
          first_name=first_name,
          last_name=last_name,
          email=email,
          username=username,
          password=password,  # Note: Hash the password before saving in a real-world scenario
          user_type=user_type,
          self_distributor=self_distributor,
          distributor_id=distributor_id
        )
        user.save()
        # Redirect to a success page or home page
        return redirect('company_register_page2',user.id)  
    else:
      return redirect('company_register_page1')
  return render(request, 'company_register.html')  

def company_register_page2(request,pk):
  terms=PaymentTerms.objects.all()
  context={
    'terms':terms,
    'company_id':pk
  }
  return render(request,'company_register2.html', context) 

def company_registration_save2(request,pk):
  if request.method == 'POST':
    user=LoginDetails.objects.get(id=pk)
    register_action = 'distributor' if user.self_distributor == 'distributor' else 'self'
    distributor_approve = 0 if user.self_distributor == 'distributor' else 1

    distributor_details = DistributorDetails.objects.get(distributor_code=user.distributor_id) if user.self_distributor == 'distributor' else None



    # Retrieve data from the POST request
    company_name = request.POST.get('cname')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    country = request.POST.get('country')
    pincode = request.POST.get('pincode')
    pannumber = request.POST.get('pannumber')
    gsttype = request.POST.get('gsttype')
    gstno = request.POST.get('gstno')
    profile_pic=  request.FILES.get('image')
    select=request.POST['select']
    terms=PaymentTerms.objects.get(id=select)
    s_date=date.today()
    days=int(terms.days)
    end=date.today() + timedelta(days=days)
    e_date=end
    code_length = 8  
    characters = string.ascii_letters + string.digits  # Letters and numbers

    while True:
      unique_code = ''.join(random.choice(characters) for _ in range(code_length))
        
      # Check if the code already exists in the table
      if not CompanyDetails.objects.filter(company_code=unique_code).exists():
        break
       
  
    # Create a new CompanyDetails instance and populate it with form data
    company_details_instance = CompanyDetails(
      login_details=user,
      distributor=distributor_details,
      company_name=company_name,
      contact=phone,
      address=address,
      city=city,
      state=state,
      country=country,
      pincode=pincode,
      pan_number=pannumber,
      gst_type=gsttype,
      gst_no=gstno,
      profile_pic=profile_pic,
      payment_term=terms,
      start_date=s_date,
      End_date=e_date,
      company_code=unique_code,
      reg_action=register_action,
      Distributor_approval=distributor_approve
      # Add more fields as needed
    )

    company_details_instance.save()  # Save the instance to the database

    # Create a new paymentterm instance and populate it with form data
    active_plan=PaymentTermsUpdates(
      company=company_details_instance,
      payment_term=terms, 
    )
    active_plan.save() # Save the instance to the database

    messages.info=(request,'Company Details Saved')
    return redirect('modules_select_page', company_details_instance.id)

  return render(request,'company_register2.html')


#--------------- Staff registration and save-------------------------

def staff_register_page(request):
  return render(request, 'staff_register.html')


def staff_registration(request):
  if request.method == 'POST':
    # Get data from the form
    first_name = request.POST.get('fname')
    last_name = request.POST.get('lname')
    email = request.POST.get('eid')
    username = request.POST.get('uname')
    phone = request.POST.get('ph')
    password = request.POST.get('pass')
    cpassword = request.POST.get('cpass')
    user_type = 'Staff'
    profile_pic=  request.FILES.get('image')
    code = request.POST.get('code')

    if code != '':
      if CompanyDetails.objects.filter(company_code=code).exists():
        company=CompanyDetails.objects.get(company_code=code)
      else :
        messages.info(request, 'Sorry, company id does not exists')
        return redirect('staff_register_page')

    # Check if the username is unique within the same company
    if StaffDetails.objects.filter(login_details__username=username, company=company).exists():
      messages.warning(request, 'Username already exists for staff in the same company')
      return redirect('staff_register_page')

    if password == cpassword:
      if LoginDetails.objects.filter(email=email).exists():
        messages.success(request,'Email id exists')
        return redirect('staff_register_page')
      if LoginDetails.objects.filter(password=password).exists():
        messages.error(request,'Use another password')
        return redirect('staff_register_page')
      else:
        # Save data to the database
        user = LoginDetails(
          first_name=first_name,
          last_name=last_name,
          email=email,
          username=username,
          password=password,  # Note: Hash the password before saving in a real-world scenario
          user_type=user_type,
        )
        user.save()

        staff_details_instance= StaffDetails(
          login_details=user,
          company=company,
          contact=phone,
          image=profile_pic,
          position='staff'
        )
        staff_details_instance.save()

        # Redirect to a success page or home page
        return redirect('login_page')  
    else:
      return redirect('staff_register_page')
  return render(request, 'staff_register.html')  


#------------------Company Modules Select Section-------------------------

def modules_select_page(request,pk):
  company_id=pk
  context={
    'company':company_id,
  }
  return render(request, 'modules.html',context)


def choose_modules(request, pk):
  if request.method == 'POST':

    # Get the company based on the id
    company = CompanyDetails.objects.get(id=pk)

    # Retrieve values
    items = request.POST.get('items', 0)
    price_list = request.POST.get('price_list', 0)
    stock_adjustment = request.POST.get('stock_adjustment', 0)
    godown = request.POST.get('godown', 0)

    cash_in_hand = request.POST.get('cash_in_hand', 0)
    offline_banking = request.POST.get('offline_banking', 0)
    upi = request.POST.get('upi', 0)
    bank_holders = request.POST.get('bank_holders', 0)
    cheque = request.POST.get('cheque', 0)
    loan_account = request.POST.get('loan_account', 0)

    customers = request.POST.get('customers', 0)
    invoice = request.POST.get('invoice', 0)
    estimate = request.POST.get('estimate', 0)
    sales_order = request.POST.get('sales_order', 0)
    recurring_invoice = request.POST.get('recurring_invoice', 0)
    retainer_invoice = request.POST.get('retainer_invoice', 0)
    credit_note = request.POST.get('credit_note', 0)
    payment_received = request.POST.get('payment_received', 0)
    delivery_challan = request.POST.get('delivery_challan', 0)

    vendors = request.POST.get('vendors', 0)
    bills = request.POST.get('bills', 0)
    recurring_bills = request.POST.get('recurring_bills', 0)
    vendor_credit = request.POST.get('vendor_credit', 0)
    purchase_order = request.POST.get('purchase_order', 0)
    expenses = request.POST.get('expenses', 0)
    recurring_expenses = request.POST.get('recurring_expenses', 0)
    payment_made = request.POST.get('payment_made', 0)

    projects = request.POST.get('projects', 0)

    chart_of_accounts = request.POST.get('chart_of_accounts', 0)
    manual_journal = request.POST.get('manual_journal', 0)

    eway_bill = request.POST.get('ewaybill', 0)

    employees = request.POST.get('employees', 0)
    employees_loan = request.POST.get('employees_loan', 0)
    holiday = request.POST.get('holiday', 0)
    attendance = request.POST.get('attendance', 0)
    salary_details = request.POST.get('salary_details', 0)

    reports = request.POST.get('reports', 0)


    # Create a new ZohoModules instance and save it to the database
    data = ZohoModules(
      company=company,
      items=items, price_list=price_list, stock_adjustment=stock_adjustment, godown=godown,
      cash_in_hand=cash_in_hand, offline_banking=offline_banking, upi=upi, bank_holders=bank_holders,
      cheque=cheque, loan_account=loan_account,
      customers=customers, invoice=invoice, estimate=estimate, sales_order=sales_order,
      recurring_invoice=recurring_invoice, retainer_invoice=retainer_invoice, credit_note=credit_note,
      payment_received=payment_received, delivery_challan=delivery_challan,
      vendors=vendors, bills=bills, recurring_bills=recurring_bills, vendor_credit=vendor_credit,
      purchase_order=purchase_order, expenses=expenses, recurring_expenses=recurring_expenses,
      payment_made=payment_made,
      projects=projects,
      chart_of_accounts=chart_of_accounts, manual_journal=manual_journal,
      eway_bill=eway_bill,
      employees=employees, employees_loan=employees_loan, holiday=holiday,
      attendance=attendance, salary_details=salary_details,
      reports=reports,    
    )
    data.save()
    return redirect('login_page')
  return render(request, 'modules.html.html')




#------------------ Login Section-------------------------

def login_page(request):
  return render(request, 'login.html')



def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None and user.is_staff:
      auth_login(request, user)
      return redirect('admindash')

    try:
      log_user = LoginDetails.objects.get(username=username, password=password)
    except ObjectDoesNotExist:
      messages.error(request, 'Invalid Username or Password. Try Again.')
      return redirect('login_page')

    # Distributor login session
    if log_user.user_type == 'Distributor':
      request.session["login_id"] = log_user.id
      if 'login_id' in request.session:
        distributor_id = request.session['login_id']
      else:
        return redirect('login_page')

      try:
        distributor = LoginDetails.objects.get(id=distributor_id)
        current_date=date.today()
      except LoginDetails.DoesNotExist:
        return redirect('login_page')

      try:
        dash_details = DistributorDetails.objects.get(login_details=distributor, superadmin_approval=1)
        if current_date > dash_details.End_date:
          messages.success(request,'Payment Terms validity expired')
          return redirect('login_page')
        else:
          return redirect('distributor_dashboard')
      except DistributorDetails.DoesNotExist:
        messages.info(request, 'Approval is Pending..')
        return redirect('login_page')

    # Company login session
    
    elif log_user.user_type == 'Company':
      request.session["login_id"] = log_user.id
      if 'login_id' in request.session:
        company_id = request.session['login_id']
      else:
        return redirect('login_page')

      try:
        company = LoginDetails.objects.get(id=company_id)
        current_date=date.today()
      except LoginDetails.DoesNotExist:
        return redirect('login_page')

      try:
        dash_details = CompanyDetails.objects.get(
          login_details=company,
          superadmin_approval=1,
          Distributor_approval=1,
        )
        if current_date > dash_details.End_date:
          messages.success(request,'Payment Terms validity expired')
          return redirect('login_page')
        else:
          return redirect('company_dashboard')
      except CompanyDetails.DoesNotExist:
        messages.warning(request, 'Approval is Pending')
        return redirect('login_page')

    # Staff login session
    elif log_user.user_type == 'Staff':
      request.session["login_id"] = log_user.id
      if 'login_id' in request.session:
        staff_id = request.session['login_id']
      else:
        return redirect('login_page')

      try:
        staff = LoginDetails.objects.get(id=staff_id)
      except LoginDetails.DoesNotExist:
        return redirect('login_page')

      try:
        dash_details = StaffDetails.objects.get(login_details=staff, company_approval=1)
        return redirect('staff_dashboard')
      except StaffDetails.DoesNotExist:
        messages.error(request, 'Approval is Pending..')
        return redirect('login_page')

    else:
      return render(request, 'error-404.html')

  # Handle GET requests
  else:
    return redirect('login_page')


#------------------ Logout Section-------------------------

def admin_logout(request):
  auth.logout(request)
  return redirect('login_page')

def logout(request):
  request.session.pop('login_id', None)
  return redirect('login_page')   