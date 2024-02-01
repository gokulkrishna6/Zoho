from django.db import models

# Create your models here.

# models for distributor, company, staff registration and payment terms

class LoginDetails(models.Model):
    first_name = models.CharField(max_length=100,null=True,blank=True) 
    last_name = models.CharField(max_length=100,null=True,blank=True) 
    email = models.CharField(max_length=100,null=True,blank=True) 
    username = models.CharField(max_length=100,null=True,blank=True) 
    password = models.CharField(max_length=100,null=True,blank=True) 
    user_type = models.CharField(max_length=100,null=True,blank=True) 
    self_distributor = models.CharField(max_length=100,null=True,blank=True,default='self')
    distributor_id = models.CharField(max_length=100,null=True,blank=True,default='')


class PaymentTerms(models.Model):
    payment_terms_number = models.IntegerField(null=True,blank=True)  
    payment_terms_value = models.CharField(max_length=100,null=True,blank=True) 
    days = models.CharField(max_length=100,null=True,blank=True) 


class DistributorDetails(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    payment_term = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True) 
    distributor_code = models.CharField(max_length=100,null=True,blank=True) 
    start_date = models.DateField(max_length=255,null=True,blank=True)
    End_date = models.DateField(max_length=255,null=True,blank=True)
    image = models.ImageField(null=True,blank = True,upload_to = 'image/distributor') 
    log_action = models.IntegerField(null=True,default=0)
    superadmin_approval = models.IntegerField(null=True,default=0)


class CompanyDetails(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    distributor = models.ForeignKey(DistributorDetails, on_delete=models.CASCADE,null=True,blank=True)
    payment_term = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True) 
    contact = models.CharField(max_length=100,null=True,blank=True)
    company_code = models.CharField(max_length=100,null=True,blank=True) 
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    pan_number = models.CharField(max_length=255,null=True,blank=True)
    start_date = models.DateField(max_length=255,null=True,blank=True)
    End_date = models.DateField(max_length=255,null=True,blank=True)
    gst_type = models.CharField(max_length=255,null=True,blank=True)
    gst_no = models.CharField(max_length=255,null=True,blank=True)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/company')
    superadmin_approval = models.IntegerField(null=True,default=0)  
    Distributor_approval = models.IntegerField(null=True,default=0) 
    reg_action = models.CharField(max_length=255,null=True,blank=True,default='self')
    position = models.CharField(max_length=255,null=True,blank=True,default='company')


class StaffDetails(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE,null=True,blank=True)
    contact = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(null=True,blank = True,upload_to = 'image/staff')    
    company_approval = models.IntegerField(null=True,default=0)    
    position = models.CharField(max_length=255,null=True,blank=True,default='staff')

class PaymentTermsUpdates(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE,null=True,blank=True) 
    distributor = models.ForeignKey(DistributorDetails, on_delete=models.CASCADE,null=True,blank=True) 
    payment_term = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE,null=True,blank=True)
    update_action = models.IntegerField(null=True,default=0) 
    status = models.CharField(max_length=100,null=True,default='New')

class ZohoModules(models.Model):
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE,null=True,blank=True) 

    # ITEMS
    items = models.IntegerField(null=True, default=0)
    price_list = models.IntegerField(null=True, default=0)
    stock_adjustment = models.IntegerField(null=True, default=0)
    godown = models.IntegerField(null=True, default=0)

    # CASH & BANK
    cash_in_hand = models.IntegerField(null=True, default=0)
    offline_banking = models.IntegerField(null=True, default=0)
    upi = models.IntegerField(null=True, default=0)
    bank_holders = models.IntegerField(null=True, default=0)
    cheque = models.IntegerField(null=True, default=0)
    loan_account = models.IntegerField(null=True, default=0)

    # SALES MODULE
    customers = models.IntegerField(null=True, default=0)
    invoice = models.IntegerField(null=True, default=0)
    estimate = models.IntegerField(null=True, default=0)
    sales_order = models.IntegerField(null=True, default=0)
    recurring_invoice = models.IntegerField(null=True, default=0)
    retainer_invoice = models.IntegerField(null=True, default=0)
    credit_note = models.IntegerField(null=True, default=0)
    payment_received = models.IntegerField(null=True, default=0)
    delivery_challan = models.IntegerField(null=True, default=0)

    # PURCHASE MODULE
    vendors = models.IntegerField(null=True, default=0)
    bills = models.IntegerField(null=True, default=0)
    recurring_bills = models.IntegerField(null=True, default=0)
    vendor_credit = models.IntegerField(null=True, default=0)
    purchase_order = models.IntegerField(null=True, default=0)
    expenses = models.IntegerField(null=True, default=0)
    recurring_expenses = models.IntegerField(null=True, default=0)
    payment_made = models.IntegerField(null=True, default=0)

    # TIME TRACKING
    projects = models.IntegerField(null=True, default=0)

    # ACCOUNTS
    chart_of_accounts = models.IntegerField(null=True, default=0)
    manual_journal = models.IntegerField(null=True, default=0)

    # E WAY BILL
    eway_bill = models.IntegerField(null=True, default=0)

    # PAYROLL
    employees = models.IntegerField(null=True, default=0)
    employees_loan = models.IntegerField(null=True, default=0)
    holiday = models.IntegerField(null=True, default=0)
    attendance = models.IntegerField(null=True, default=0)
    salary_details = models.IntegerField(null=True, default=0)

    # REPORTS
    reports = models.IntegerField(null=True, default=0)

    update_action = models.IntegerField(null=True,default=0) 
    status = models.CharField(max_length=100,null=True,default='New')      

