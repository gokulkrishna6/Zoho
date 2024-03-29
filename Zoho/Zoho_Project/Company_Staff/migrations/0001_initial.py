# Generated by Django 4.2.6 on 2024-02-01 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Register_Login', '0009_paymenttermsupdates'),
    ]

    operations = [
        migrations.CreateModel(
            name='payroll_employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('alias', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('joindate', models.DateField(null=True)),
                ('salary_type', models.CharField(default='Fixed', max_length=100, null=True)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('emp_number', models.CharField(max_length=100, null=True)),
                ('designation', models.CharField(max_length=100, null=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('dob', models.DateField(null=True)),
                ('age', models.PositiveIntegerField(default=0)),
                ('blood', models.CharField(max_length=10, null=True)),
                ('parent', models.CharField(max_length=100, null=True)),
                ('spouse_name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=250, null=True)),
                ('permanent_address', models.CharField(max_length=250, null=True)),
                ('Phone', models.BigIntegerField(null=True)),
                ('emergency_phone', models.BigIntegerField(blank=True, default=1, null=True)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('Income_tax_no', models.CharField(max_length=255, null=True)),
                ('Aadhar', models.CharField(default='', max_length=250, null=True)),
                ('UAN', models.CharField(max_length=255, null=True)),
                ('PFN', models.CharField(max_length=255, null=True)),
                ('PRAN', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(default='Active', max_length=200, null=True)),
                ('isTDS', models.CharField(max_length=200, null=True)),
                ('TDS_percentage', models.IntegerField(default=0, null=True)),
                ('salaryrange', models.CharField(choices=[('1-10', '1-10'), ('10-15', '10-15'), ('15-31', '15-31')], default='1-10', max_length=10, null=True)),
                ('amountperhr', models.IntegerField(blank=True, default=0, null=True)),
                ('workhr', models.IntegerField(blank=True, default=0, null=True)),
                ('uploaded_file', models.FileField(null=True, upload_to='images/')),
                ('acc_no', models.CharField(max_length=255, null=True)),
                ('IFSC', models.CharField(max_length=100, null=True)),
                ('bank_name', models.CharField(max_length=100, null=True)),
                ('branch', models.CharField(max_length=100, null=True)),
                ('transaction_type', models.CharField(max_length=100, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Register_Login.companydetails')),
                ('login_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Register_Login.logindetails')),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('holiday_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Register_Login.companydetails')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Register_Login.logindetails')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('reason', models.CharField(max_length=255, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Register_Login.companydetails')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Company_Staff.payroll_employee')),
                ('login_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Register_Login.logindetails')),
            ],
        ),
    ]
