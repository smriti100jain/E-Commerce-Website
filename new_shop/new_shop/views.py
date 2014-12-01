from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail
from product.models import product, transaction, comments
from userprofile.models import user_hist
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone



def extract_cart(request):
    usr_hist_temp=user_hist.objects.all().filter(user_id=request.user.id)
    usr_hist_temp=list(reversed(usr_hist_temp))
    count_check=0
    usr_hist=[]
    for i in usr_hist_temp:
        if i.u_hist in usr_hist:
            continue
        usr_hist.append(i.u_hist)
        count_check=count_check+1
        if count_check>=5:
            break
    
    try:
        cart=request.user.cart.kart
    except:
        return ([],[],[],0,[],"")
    if cart=="" :
        return ([],[],[],0,usr_hist,request.user)
    cart=cart.split(',')
    prod_name=[]
    prod_quantity=[]
    prod_price=[]
    while(len(cart)>0):
        temp=cart[0]
        if (temp==''):
            cart.remove(temp)
            continue
        t1=product.objects.all().get(id=int(temp))
        prod_name.append([t1,cart.count(temp)])
        prod_quantity.append(cart.count(temp))
        prod_price.append(t1.price)
        cart=filter(lambda i: i != temp, cart)
    tot=0
    for i in prod_name:
        tot=tot + int(i[0].price)*int(i[1])

    usr_hist_temp=user_hist.objects.all().filter(user_id=request.user.id)
    count_check=0
    usr_hist=[]
    for i in usr_hist_temp:
        if i.u_hist in usr_hist:
            continue
        usr_hist.append(i.u_hist)
        count_check=count_check+1
        if count_check>=5:
            break
    
    #rel_s=request.user.related_search
    return (prod_name, prod_quantity, prod_price,tot,usr_hist,request.user)

def home(request):
    prod=product.objects.all()
    cat=[]
    for i in prod:
        cat.append(i.category)
    cat=list(set(cat))
    usr=request.user.username
    if len(usr)==0:
        flg=0
    else:
        flg=1
    (prod_name,prod_quantity,prod_price,tot,usr_hist,usr)=extract_cart(request)
    c={}
    c.update(csrf(request))
    c["cat_list"]=cat
    c["prod_list"]=prod
    c["flag"]=flg
    c["prod_name"]=prod_name
    c["prod_quantity"]=prod_quantity
    c["prod_price"]=prod_price
    c["count"]=len(prod_quantity)
    c["tot"]=tot
    c["usr_hist"]=usr_hist
    c["usr"]=usr
    
    return render_to_response('home.html',c)

def prd(request,product_id):
    prod=product.objects.all()
    cat=[]
    usr=request.user.username
    if len(usr)==0:
        flg=0
    else:
        flg=1
    for i in prod:
        cat.append(i.category)
    cat=list(set(cat))
    
    prdct=product.objects.all().get(id=product_id)    
    related_lst1=list(prdct.related_prod)
    related_lst=[]
    for i in related_lst1:
        try:
            related_lst.append(product.objects.all().get(id=int(i)))
        except:
            continue

    (prod_name,prod_quantity,prod_price,tot,usr_hist,usr)=extract_cart(request)
    buy_list=transaction.objects.all().filter(product_id=product_id)
    buy_list=list(reversed(list(buy_list)))
    com_lst=comments.objects.all().filter(product_id=product_id)    
    try:
        user_hist_temp=user_hist()
        user_hist_temp.user=request.user
        user_hist_temp.u_hist=product.objects.all().get(id=product_id)
        user_hist_temp.save()
    except:
        pass
    c={}
    c.update(csrf(request))
    c["cat_list"]=cat
    c["prod_id"]=prdct
    c["flag"]=flg
    c["prod_name"]=prod_name
    c["prod_quantity"]=prod_quantity
    c["prod_price"]=prod_price
    c["tot"]=tot
    c["count"]=len(prod_quantity)
    c["related_lst"]=related_lst
    c["com_lst"]=com_lst
    c["usr_hist"]=usr_hist
    c["buy_list"]=buy_list
    c["usr"]=usr
    return render_to_response('product.html',c)
    
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/invalid/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=request.POST["username"], password=request.POST["password1"])
            if user is not None:
                auth.login(request, user)
            return HttpResponseRedirect('/home/')
        
    else:
        form = UserCreationForm()
    args = {}
    args.update(csrf(request))
    
    args['form'] = form
    
    return render_to_response('register.html', args)

def addtocart(request,product_id):
    qty=request.POST["qty"]
    if(qty=='' or qty==None):
        qty=0
    try:
        cart=request.user.cart
        crt=cart.kart
        if crt=='':
            crt=str(product_id)
            qty=int(qty)-1
        for i in range(0,int(qty)):
            crt=crt+','+str(product_id)
        cart.kart=crt
        cart.save()
    except:
        return HttpResponseRedirect('/signup/')

        
    (prod_name,prod_quantity,prod_price,tot,usr_hist,usr)=extract_cart(request)
    count=len(prod_quantity)
    return HttpResponseRedirect('/product/%s/'%(str(product_id)),{"prod_name":prod_name,"prod_quantity":prod_quantity,"prod_price":prod_price,"tot":tot,"usr":usr,"count":count,"usr_hist":usr_hist})

        

def showcart(request):
        prod_name,prod_quantity,prod_price,tot,usr_hist,usir = extract_cart(request)
        prod=product.objects.all()
        cat=[]
        for i in prod:
            cat.append(i.category)
        cat=list(set(cat))
        
        usr=request.user.username
        if len(usr)==0:
            flg=0
        else:
            flg=1
        
        c={}
        c.update(csrf(request))
        c["cat_list"]=cat
        c["flag"]=flg
        c["prod_name"]=prod_name
        c["prod_quantity"]=prod_quantity
        c["prod_price"]=prod_price
        c["tot"]=tot
        c["count"]=len(prod_quantity)
        c["usr_hist"]=usr_hist
        c["usr"]=usir
        return render_to_response('showcart.html',c)

def disptrans(request):
    prod_name,prod_quantity,prod_price,tot,usr_hist,usir = extract_cart(request)
    
    t1=transaction.objects.all().filter(user_id=request.user.id,delivered=False)
    t2=transaction.objects.all().filter(user_id=request.user.id,delivered=True)
    usr=request.user.username
    prod=product.objects.all()
    cat=[]
    if len(usr)==0:
        flg=0
    else:
        flg=1
    for i in prod:
        cat.append(i.category)
    cat=list(set(cat))
    c={}
    c.update(csrf(request))
    c["cat_list"]=cat
    c["flag"]=flg
    c["prod_name"]=prod_name
    c["prod_quantity"]=prod_quantity
    c["prod_price"]=prod_price
    c["tot"]=tot
    c["count"]=len(prod_quantity)
    c["t1"]=t1
    c["t2"]=t2
    c["usr_hist"]=usr_hist
    c["usr"]=usir
    
    return render_to_response('showtrans.html',c)

    
def showtrans(request):
    prod_name,prod_quantity,prod_price,tot,usr_hist,usr = extract_cart(request)
    
    for i in prod_name:
        if(i[0].quantity<i[1]):
            continue  #MAINTAIN A LIST OF ERRORS
        i[0].quantity=i[0].quantity-i[1]
        i[0].save()
        temp=transaction()
        temp.user=request.user
        temp.product=i[0]
        temp.quantity=i[1]
        temp.date=timezone.now()
        temp.date_complete=timezone.now()
        temp.address=str(request.POST["city"])
        temp.address_complete=str(request.POST["add"])
        temp.save()
    cart=request.user.cart
    cart.kart=""
    cart.save()
    t1=transaction.objects.all().filter(user_id=request.user.id,delivered=False)
    t2=transaction.objects.all().filter(user_id=request.user.id,delivered=True)
    t1=list(reversed(list(t1)))
    t2=list(reversed(list(t2)))
    usr=request.user.username
    prod=product.objects.all()
    cat=[]
    if len(usr)==0:
        flg=0
    else:
        flg=1
    for i in prod:
        cat.append(i.category)
    cat=list(set(cat))
    c={}
    c.update(csrf(request))
    c["cat_list"]=cat
    c["flag"]=flg
    c["prod_name"]=prod_name
    c["prod_quantity"]=prod_quantity
    c["prod_price"]=prod_price
    c["tot"]=tot
    c["count"]=len(prod_quantity)
    c["t1"]=t1
    c["t2"]=t2
    c["usr_hist"]=usr_hist
    c["usr"]=usr
    return render_to_response('showtrans.html',c)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/home/')

def category(request,prod_cat):
    prod_name,prod_quantity,prod_price,tot,usr_hist,usir = extract_cart(request)
    
    usr=request.user.username
    prod=product.objects.all()
    cat=[]
    if len(usr)==0:
        flg=0
    else:
        flg=1
    for i in prod:
        cat.append(i.category)
    cat=list(set(cat))
    prod=product.objects.all().filter(category__icontains=str(prod_cat))
    c={}
    c.update(csrf(request))
    c["cat_list"]=cat
    c["flag"]=flg
    c["prod_list"]=prod
    c["prod_name"]=prod_name
    c["prod_quantity"]=prod_quantity
    c["prod_price"]=prod_price
    c["tot"]=tot
    c["count"]=len(prod_quantity)
    c["usr_hist"]=usr_hist
    c["usr"]=usir

    return render_to_response('home.html',c)

def submit_com(request,prod_id):
    try:
        temp=comments()
        temp.user=request.user
        temp.product=product.objects.all().get(id=int(prod_id))
        temp.comment=str(request.POST["comm"])
        temp.save()
        return HttpResponseRedirect('/product/'+str(prod_id)+'/')

    except:
        return HttpResponseRedirect('/signup/')

                

def srch(request):
    srch_strng=str(request.POST["srch_val"])
    prod=product.objects.all().filter(name__icontains=srch_strng)
    prod1=product.objects.all().filter(category__icontains=srch_strng)
    prod=list(prod)+list(prod1)
    cat=[]
    for i in prod:
        cat.append(i.category)
    cat=list(set(cat))
    usr=request.user.username
    if len(usr)==0:
        flg=0
    else:
        flg=1
    (prod_name,prod_quantity,prod_price,tot,usr_hist,usr)=extract_cart(request)
    c={}
    c.update(csrf(request))
    c["cat_list"]=cat
    c["prod_list"]=prod
    c["flag"]=flg
    c["prod_name"]=prod_name
    c["prod_quantity"]=prod_quantity
    c["prod_price"]=prod_price
    c["count"]=len(prod_quantity)
    c["tot"]=tot
    c["usr_hist"]=usr_hist
    c["usr"]=usr
    return render_to_response('home.html',c)

    
def admin_trans_user(request):
    u_list=User.objects.all()
    c={}
    c.update(csrf(request))
    return render_to_response('admin_trans_user.html',{"u_list":u_list})

def admin_trans(request):
    return render_to_response('admin_trans.html',{})

def admin_trans_userinfo(request,u_id):
    u_list_pending=transaction.objects.all().filter(user_id=u_id,delivered=False)
    u_list_delivered=transaction.objects.all().filter(user_id=u_id,delivered=True)
    return render_to_response('admin_trans_userinfo.html',{"u_list_pending":u_list_pending,"u_list_delivered":u_list_delivered})
        

def admin_trans_prod(request):

    p_list=[]


    try:    
        from_dt=request.POST["from_dt"]
        from_dt=from_dt.split('-')
        to_dt=request.POST["to_dt"]
        to_dt=to_dt.split('-')
        p_list_all=transaction.objects.all()
        for i in p_list_all:
            temp=str(i.date)
            temp=temp.split('-')
            if temp>=from_dt and temp<=to_dt:
                p_list.append(i)
    except:
        p_list=[]

    length=0
    for i in p_list:
        length=length+i.quantity
    c={}
    c.update(csrf(request))
    c["p_list"]=p_list
    c["length"]=length
    return render_to_response('admin_trans_prod.html',c)

        
    

