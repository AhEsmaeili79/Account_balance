from transactions.models import Category, Transactions

def has_transaction(am,Tr_T,Tr_d,Tr_Cat,U_id,Tr_Time,Desc):
    has_transacion = Transactions.objects.filter(amount=am,
                                                     transaction_type=Tr_T,
                                                     transaction_date=Tr_d,
                                                     user_id=U_id,
                                                     category_id=Tr_Cat,
                                                     transaction_time=Tr_Time,
                                                     description=Desc).exists()
    return has_transacion


def check_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False
    
def filter_by_type(req,type):
    transaction_type = Transactions.objects.order_by('-transaction_date','-transaction_time').filter(user_id=req.user.id, transaction_type=type)
    return transaction_type

def get_from_post(req,amnt,Tr_date,Tr_time,Cat,U_id,Desc):
    amount = req.POST.get(amnt)
    trans_date = req.POST.get(Tr_date)
    trans_time = req.POST.get(Tr_time)
    trans_cat = req.POST.get(Cat)
    user_id = req.POST.get(U_id)
    desc = req.POST.get(Desc)

    return amount,trans_date,trans_time,trans_cat,user_id,desc


def update_trans(transaction,amount,transaction_date,transaction_time,transaction_category,user_id,description):
    if amount:
        transaction.amount = amount
    if transaction_date:
        transaction_date = transaction_date.replace('/', '-')
        transaction.transaction_date = transaction_date
    if transaction_time:
        transaction.transaction_time = transaction_time
    if transaction_category:
        transaction.category_id = Category.objects.get(id=transaction_category, user_id__in=[user_id, 0])
    if description or description == "":
        transaction.description = description

    return transaction

def create_trans(amt,tr_type,tr_date,tr_time,tr_cat,user_id,desc):
    transaction = Transactions(amount=amt,transaction_type=tr_type,
                               transaction_date=tr_date,tr_time=tr_time,
                               category_id= Category.objects.get(id=tr_cat, user_id__in=[user_id, 0]),
                               user_id=user_id,description=desc)
    return transaction