from datetime import datetime, date, timedelta
from fees.models import Payment, FeesItem
from users.models import User
from django.conf import settings


def adjust_date_and_months(from_month=None, to_month=None, from_year=None, to_year=None):
  start_date = datetime.strptime(settings.START_DATE, '%Y-%m-%d')
  from_year = int(from_year) if from_year else datetime.now().year
  to_year = int(to_year) if to_year else datetime.now().year
  from_month = int(from_month) if from_month else 1 if int(from_year) > start_date.year else start_date.month
  to_month = int(to_month) if to_month else 12
  return from_month, to_month, from_year, to_year


# return list of user's paid months
def list_of_paid_months(user, from_year, to_year):
  paid_months = []
  for i in range(from_year, to_year+1):
    paid_months = paid_months + list(Payment.objects.filter(
        user=user, payment_year=str(i)).values('payment_month', 'payment_year'))
  return paid_months


# return list of years for which data will be fetched.
def list_of_years(from_year, to_year):
  if(not from_year and not to_year):
    years = [datetime.now().year]
  elif(not from_year and to_year):
    years = [int(to_year)]
  elif(from_year and not to_year):
    years = [int(from_year)]
  else:
    years = []
    for i in range(int(from_year), int(to_year)+1):
      years.append(i)
  return years


# return list of all months
# from from_date to to_date
def list_of_months(from_month, to_month, from_year, to_year):
  if not from_year and not to_year:
    from_year, to_year = datetime.now().year, datetime.now().year
  
  from_date = datetime(int(from_year), from_month, 1)
  to_date = datetime(int(to_year), to_month, 1)
  num_months = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)
  num_months_arr = []
  for j in range(num_months+1):
    num_months_arr.append(
        (((from_month+j-1) % 12)+1))
  return num_months_arr


# return list of user's payment details from the provided dates  
def users_payment_data(user, from_month=None, from_year=None, to_month=None, to_year=None):
  years = list_of_years(from_year, to_year)
  user_payments = []
  
  if(from_month or to_month):
    num_months_arr = list_of_months(from_month, to_month, from_year, to_year)
    k = 0
    for i in num_months_arr:
      payment = Payment.objects.filter(user=user, payment_month=str(i), payment_year=str(years[k]))
      if payment:
        user_payments.append(payment[0])
      if(i == 12):
        k += 1
  else:
    for i in years:
      payment = Payment.objects.filter(
          user=user, payment_year=str(i))
      if payment:
          user_payments = payment
  return user_payments


# return list of user's payment details of paid months
# from the provided dates  
def users_paid_payment_data(user, from_month=None, from_year=None, to_month=None, to_year=None):
  years = list_of_years(from_year, to_year)
  user_payments = []
  
  if(from_month or to_month):
    num_months_arr = list_of_months(from_month, to_month, from_year, to_year)
    k = 0
    for i in num_months_arr:
      payment = Payment.objects.filter(user=user, payment_month=str(i), payment_year=str(years[k]), status=Payment.Status.PAID)
      if payment:
        user_payments.append(payment[0])
      if(i == 12):
        k += 1
  else:
    for i in years:
      payment = Payment.objects.filter(
          user=user, payment_year=str(i), status=Payment.Status.PAID)
      if payment:
          user_payments = payment
  return user_payments


# return list of user's unpaid months.
def get_user_due_months(user, from_month=None, from_year=None, to_month=None, to_year=None):
  paid_months = list_of_paid_months(user, from_year, to_year)
  all_months = list_of_months(from_month, to_month, from_year, to_year)
  years = list_of_years(from_year, to_year)

  unpaid_months = []
  k = 0
  for i in all_months:
    if {'payment_month': str(i), 'payment_year': str(years[k])} not in paid_months and datetime.strptime(settings.START_DATE, '%Y-%m-%d') <= datetime(years[k], i, 1):
      unpaid_months.append({
          'month': i,
          'year': years[k]
      })
    if i == 12:
      k += 1

  return unpaid_months


# return list of user's payment details
# including unpaid and paid months from the provided details
def get_modified_payment_details(user, new_serializer_data, from_month=None, from_year=None, to_month=None, to_year=None):
  due_months = get_user_due_months(user, from_month, from_year, to_month, to_year)
  user = User.objects.get(id=user)
  fees = FeesItem.objects.first()
  fees_amount = 0
  for key in fees.fields:
    fees_amount += int(fees.fields[key])
  if(len(new_serializer_data) > 0):
    for i in range(len(new_serializer_data)):
      new_serializer_data[i]['payment_status'] = True
  # for i in due_months:
  #   if datetime(to_year,to_month,1) >= datetime(i['year'], i['month'], 1):
  #     new_serializer_data.append({
  #       'user': user.id,
  #       'full_name': user.full_name,
  #       'amount': str(fees_amount) if fees else '',
  #       'amount_break_up': fees.fields if fees else {},
  #       'payment_month': str(i['month']),
  #       'payment_year': str(i['year']),
  #       'payment_status': False
  #     })
  new_serializer_data = sorted(
      new_serializer_data, key=lambda i: datetime(int(i['payment_year']) , int(i['payment_month']), 1))
  return new_serializer_data

# payment scheduler function to store user's data 
# automatically on first day of every month
def update_payment_scheduler():
  active_users = User.objects.exclude(
      role=User.Role.ADMIN).filter(is_active=True)
  fees = FeesItem.objects.first()
  fees_amount = 0
  for key in fees.fields:
    fees_amount += int(fees.fields[key])
  
  for user in active_users:
    if not Payment.objects.filter(user=user.id, payment_month=str(datetime.now().month), payment_year=str(datetime.now().year)):
      try:
        new_payment = Payment()
        new_payment.user = user
        new_payment.amount = str(fees_amount) if fees else ''
        new_payment.amount_break_up = fees.fields if fees else {}
        new_payment.payment_month = str(datetime.now().month)
        new_payment.payment_year = str(datetime.now().year)
        new_payment.save()
      except:
        pass
  else:
    pass

