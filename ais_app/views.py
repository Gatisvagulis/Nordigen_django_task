from django.shortcuts import render, redirect
from uuid import uuid4
from json import dumps
from nordigen import NordigenClient
from django.conf import settings
from .models import RequisitonId
from celery.result import AsyncResult
from .tasks import ( 
    getTranzactionsAsync,
    getDetailsAsync,
    getBalanceAsync,
    getPremiumProductsAsync,
    getCategoryTotoalAsync)

# 1. Secret_ID and Secret_KEY should be entered in .env file under SECRET_ID and SECRET_KEY
# 2. The starting point, when the access token and refresh token are empty users generates them here
# 3. Both tokens from point #2. should be saved under .env file ACCESS_TOKEN and REFRESH_TOKEN

def getToken(request):

    # This statement check if new tokens should be generated
    if settings.ACCESS_TOKEN == '' or settings.REFRESH_TOKEN == '':
        # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
        client = NordigenClient(
            secret_id=settings.SECRET_ID,
            secret_key=settings.SECRET_KEY
        )
        # Create new access and refresh token
        token_data = client.generate_token()
        
        context = {'token_data':token_data}
        return render(request, 'ais_app/get-token.html', context )
    else:
        return redirect('index')


# 1. This function base view renders available Banks and countries
def runNordigen(request):
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id=settings.SECRET_ID,
        secret_key=settings.SECRET_KEY
    )
    # Use existing access token
    client.token = settings.ACCESS_TOKEN
    # Exchange refresh token for new access token
    client.exchange_token(settings.REFRESH_TOKEN)

    # Get all institution by providing country code in ISO 3166 format
    institutions = dumps(client.institution.get_institutions())
    
    context = {
        'institutions':institutions,
    }
    return render(request, 'ais_app/index.html', context )
    

# 1. Connects with the bank by institution id using generated link
def goToBank(request, id):
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id=settings.SECRET_ID,
        secret_key=settings.SECRET_KEY
    )
    # Use existing access token
    client.token = settings.ACCESS_TOKEN
    # Exchange refresh token for new access token
    client.exchange_token(settings.REFRESH_TOKEN)

    # Initialize bank session
    init = client.initialize_session(
        # institution id
        institution_id=id,
        # redirect url after successful authentication
        redirect_uri="http://127.0.0.1:8000/profile",
        # additional layer of unique ID defined by you
        reference_id=str(uuid4())
    )
    # Get requisition_id and link to initiate authorization process with a bank
    link = init.link # bank authorization link

    # Get chosen bank data as object
    bankObj = client.institution.get_institution_by_id(id)

    # Checks if the requisition id is made then save in DB requisition id and bank name
    if init.requisition_id != '':
        RequisitonId.objects.create(
            requisitionId = init.requisition_id,
            bankName = bankObj['name']
        )
    return redirect(link)


# Render a list of all user-connected banks
def getProfileInfo(request):
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id=settings.SECRET_ID,
        secret_key=settings.SECRET_KEY
    )
   # Use existing access token
    client.token = settings.ACCESS_TOKEN
    # Exchange refresh token for new access token
    client.exchange_token(settings.REFRESH_TOKEN)
    # Get from DB all saved requisition id and bank name
    requisitonObj = RequisitonId.objects.all()
    # adds = add()
    context = {
        # 'add':adds,
        'bankInfo':requisitonObj,
    }
    return render(request, 'ais_app/get-profile-info.html', context)


# Render transactions by requisition id
def getTransactions(request, pk):
    # Using Celery to get data async
    tranzactions = getTranzactionsAsync.delay(pk)
    # Query results by id async
    r = AsyncResult(tranzactions)
    transaction_results = r.get()
    # Checks the state of the query, if success renders data in the template, if failure redirects to starting page
    if r.state == 'SUCCESS':
        context = {'transactions':transaction_results}
        return render(request, 'ais_app/get-transactions.html', context)
    if r.state == 'FAILURE':
        redirect('profile')


# Render details by requisition id
def getDetails(request, pk):
    # Using Celery to get data async
    details = getDetailsAsync.delay(pk)
    # Query results by id async
    r = AsyncResult(details)
    details_results = r.get()  
    # Checks the state of the query, if success renders data in the template, if failure redirects to starting page
    if r.state == 'SUCCESS':
        context = {'details':details_results}
        return render(request, 'ais_app/get-details.html', context)
    if r.state == 'FAILURE':
        redirect('profile')
    

# Render balance by requisition id
def getBalance(request, pk):
    # Using Celery to get data async
    balances = getBalanceAsync.delay(pk)
    # Query results by id async
    r = AsyncResult(balances)
    balance_results = r.get()  
    # Checks the state of the query, if success renders data in the template, if failure redirects to starting page
    if r.state == 'SUCCESS':
        context = {'details':balance_results}
        return render(request, 'ais_app/get-balance.html', context)
    if r.state == 'FAILURE':
        redirect('profile')


# Render premium transactions and aggregate categories by requisition id
def getPremiumProducts(request, pk):
    # Using Celery to get data async
    premium_products = getPremiumProductsAsync.delay(pk)
    # Query results by id async
    r = AsyncResult(premium_products)
    premium_products_result = r.get()
    # Using Celery to get data async
    categories_total = getCategoryTotoalAsync.delay(pk)
    # Query results by id async
    p = AsyncResult(categories_total)
    categoryList_result = p.get()
    if r.state == 'SUCCESS' and p.state == 'SUCCESS':
        context = {'premium_details':premium_products_result, 'categoryList':categoryList_result}
        return render(request, 'ais_app/get-premium-products.html', context)
    if r.state == 'FAILURE' or p.state == 'FAILURE':
        redirect('profile')
