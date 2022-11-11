from nordigen import NordigenClient
from django.conf import settings
from celery import shared_task

# Function using Celery to get transaction data async
@shared_task
def getTranzactionsAsync(pk):
    """
    Function using Celery transactions get data opject from API async. As parameter use requisition id.

    Args:
        pk: Get id from view.

    Returns:
        dict: transactions
    """
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id=settings.SECRET_ID,
        secret_key=settings.SECRET_KEY
    )
    # Use existing access token
    client.token = settings.ACCESS_TOKEN
    # Exchange refresh token for new access token
    client.exchange_token(settings.REFRESH_TOKEN)

    # Get account id after you have completed authorization with a bank
    accounts = client.requisition.get_requisition_by_id(
        requisition_id= pk
    )
    # Get account id from the list.
    try:
        account_id = accounts["accounts"][0]
        # Create account instance and provide your account id from previous step
        account = client.account_api(id=account_id)
        # Fetch account metadata
        transactions = account.get_transactions()

        return transactions
    except IndexError:
        raise ValueError(
            "Account list is empty. Make sure you have completed authorization with a bank."
        )


# Function using Celery to get details data async
@shared_task
def getDetailsAsync(pk):
    """
    Function using Celery get details data opject from API async. As parameter use requisition id.

    Args:
        pk: Get id from view.

    Returns:
        dict: details
    """
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id=settings.SECRET_ID,
        secret_key=settings.SECRET_KEY
    )
    # Use existing access token
    client.token = settings.ACCESS_TOKEN
    # Exchange refresh token for new access token
    client.exchange_token(settings.REFRESH_TOKEN)

    # Get account id after you have completed authorization with a bank
    accounts = client.requisition.get_requisition_by_id(
        requisition_id= pk
    )
    # Get account id from the list.
    try:
        account_id = accounts["accounts"][0]
        # Create account instance and provide your account id from previous step
        account = client.account_api(id=account_id)
        # Fetch account details
        details = account.get_details()

        return details
    except IndexError:
        raise ValueError(
            "Account list is empty. Make sure you have completed authorization with a bank."
        )


# Function using Celery to get balance data async
@shared_task
def getBalanceAsync(pk):
    """
    Function using Celery get balance details data opject from API async. As parameter use requisition id.

    Args:
        pk: Get id from view.

    Returns:
        dict: balances
    """
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id=settings.SECRET_ID,
        secret_key=settings.SECRET_KEY
    )
    # Use existing access token
    client.token = settings.ACCESS_TOKEN
    # Exchange refresh token for new access token
    client.exchange_token(settings.REFRESH_TOKEN)

    # Get account id after you have completed authorization with a bank
    accounts = client.requisition.get_requisition_by_id(
        requisition_id= pk
    )
    # Get account id from the list.
    try:
        account_id = accounts["accounts"][0]
        # Create account instance and provide your account id from previous step
        account = client.account_api(id=account_id)
        # Fetch account details
        balances = account.get_balances()

        return balances
    except IndexError:
        raise ValueError(
            "Account list is empty. Make sure you have completed authorization with a bank."
        )


# Function using Celery to get premium transaction data async
@shared_task
def getPremiumProductsAsync(pk):
    """
    Function using Celery get premium transaction details data opject from API async. As parameter use requisition id.

    Args:
        pk: Get id from view.

    Returns:
        dict: premium_transactions
    """
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id=settings.SECRET_ID,
        secret_key=settings.SECRET_KEY
    )
    # Use existing access token
    client.token = settings.ACCESS_TOKEN
    # Exchange refresh token for new access token
    client.exchange_token(settings.REFRESH_TOKEN)

    # Get account id after you have completed authorization with a bank
    accounts = client.requisition.get_requisition_by_id(
        requisition_id= pk
    )
    # Get account id from the list.
    try:
        account_id = accounts["accounts"][0]
        # Create account instance and provide your account id from previous step
        account = client.account_api(id=account_id)

        #Get premium transactions. Country and date parameters are optional
        premium_transactions = account.get_premium_transactions()
        return premium_transactions
    except IndexError:
        raise ValueError(
            "Account list is empty. Make sure you have completed authorization with a bank."
        )


# Function using Celery to get premium transaction data and calculate balances by categories total async
@shared_task
def getCategoryTotoalAsync(pk):
    """
    Function using Celery to get premium transaction data and calculate balances by categories total async.

    Args:
        pk: Get id from view.

    Returns:
        dict: categoryList
    """
    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY
    client = NordigenClient(
        secret_id=settings.SECRET_ID,
        secret_key=settings.SECRET_KEY
    )
    # Use existing access token
    client.token = settings.ACCESS_TOKEN
    # Exchange refresh token for new access token
    client.exchange_token(settings.REFRESH_TOKEN)

    # Get account id after you have completed authorization with a bank
    accounts = client.requisition.get_requisition_by_id(
        requisition_id= pk
    )
    # Get account id from the list.
    try:
        account_id = accounts["accounts"][0]
        # Create account instance and provide your account id from previous step
        account = client.account_api(id=account_id)

        #Get premium transactions. Country and date parameters are optional
        premium_transactions = account.get_premium_transactions()

        # Empty object to add categories data
        categoryList = {}
        # loop through all transactions and sum all categories separately
        for i in range(len(premium_transactions['transactions']['booked'])):
            premium_transactions['transactions']['booked'][i]['enrichment']['purposeCategory']
            premium_transactions['transactions']['booked'][i]['enrichment']['purposeCategoryId']

            # Check if the category does not exist in our categoryList its adds to it
            if categoryList.get(premium_transactions['transactions']['booked'][i]['enrichment']['purposeCategoryId']) == None:
                getExistingCatBalance = float(premium_transactions['transactions']['booked'][i]['transactionAmount']['amount'])
            # Check if the category exists in our categoryList its pluses the balance to it
            else:
                getExistingCatBalance = float(categoryList[premium_transactions['transactions']['booked'][i]['enrichment']['purposeCategoryId']]['categoryBalance'])
                getExistingCatBalance += float(premium_transactions['transactions']['booked'][i]['transactionAmount']['amount'])

            categoryList[premium_transactions['transactions']['booked'][i]['enrichment']['purposeCategoryId']] = { 'categoryName': premium_transactions['transactions']['booked'][i]['enrichment']['purposeCategory'], 'categoryBalance':getExistingCatBalance}

        return categoryList
    except IndexError:
        raise ValueError(
            "Account list is empty. Make sure you have completed authorization with a bank."
        )