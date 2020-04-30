import requests
import json
import time


tenant_id = "<>"
client_id = "<>"
client_secret = "<>"
resource = "https://management.azure.com"
subscription_id = "<>"
grant_type = "client_credentials"

apiVersion = "2017-04-19"
sleepTimeInSecs = 60
retryCtr = 5



# Function to Fetch AccessToken

def fetchAccessToken(tenant_id, client_id, client_secret, resource, subscription_id, grant_type):
    
    accessToken = ""

    try: 
       accessTokenURL = "https://login.microsoftonline.com/"+tenant_id+"/oauth2/token"
       accessTokenHeaders = {"Content-Type":"application/x-www-form-urlencoded"}
       accessTokenReqBody = {"tenant_id":tenant_id, "client_id":client_id, "client_secret":client_secret, "resource":resource, "subscription_id":subscription_id, "grant_type":grant_type}
       tokenResponse = requests.post(url=accessTokenURL, data=accessTokenReqBody, headers=accessTokenHeaders)
       tokenResponseJson = json.loads(tokenResponse.text) 
       accessToken = tokenResponseJson["access_token"]
    except:
       print("Error while fetching the access token")
       return accessToken

    print("AccessToken Fetched!") 

    return accessToken



# Function to fetch OperationId 

def fetchOpId(subscription_id, accessToken, apiVersion):

    genRecommStatusCode = 0
    genRecommResponse = ""
    operationId = ""

    try: 
       genRecommURL = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Advisor/generateRecommendations?api-version="+apiVersion
       genRecommHeaders = {"Authorization":"Bearer "+accessToken, "Content-Type":"application/json"}
       genRecommResponse = requests.post(url=genRecommURL, headers=genRecommHeaders)

       genRecommStatusCode = genRecommResponse.status_code
      
       print(genRecommResponse)
    except:
       print("Error while generating Azure Advisor recommendations")

    if genRecommStatusCode == 202:
       print("Azure Advisor generate recommendations request successful.")
       locationHeader = genRecommResponse.headers['Location']
       start = "generateRecommendations/"
       end = "?api-version"
       operationId = locationHeader[locationHeader.find(start)+len(start):locationHeader.rfind(end)]
       print("OperationId is: "+operationId)
    else:
       print("Azure Advisor generate recommendations NOT successful")

    return operationId


# Function to fetch OperationId 

def fetchGenStatus(operationId, subscription_id, accessToken, apiVersion, sleepInterval, retryCtr):

    genStatus = False
    genStatusCode = 0

    try: 
       genStatusURL = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Advisor/generateRecommendations/"+operationId+"?api-version="+apiVersion
       genStatusHeaders = {"Authorization":"Bearer "+accessToken, "Content-Type":"application/json"}

       while retryCtr > 0:
           genStatusResponse = requests.get(url=genStatusURL, headers=genStatusHeaders)
           genStatusCode = genStatusResponse.status_code
           print("*****Gen Status Code********")
           print(genStatusCode)
    
           if genStatusCode == 204:
              genStatus = True
              print("Azure Advisor recommendations generation complete")
              break
           else:
              retryCtr -= 1  
              time.sleep(sleepInterval)
    except:
       print("Error while fetching Azure Advisor recommendations generation status")

    return genStatus


# Function to fetch Recommendations List 

def fetchRecommList(subscription_id, accessToken, apiVersion):

    recommListResponseJson = None
   
    try: 
       recommListURL = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Advisor/recommendations?api-version="+apiVersion
       recommListHeaders = {"Authorization":"Bearer "+accessToken, "Content-Type":"application/json"}

       recommListResponse = requests.get(url=recommListURL, headers=recommListHeaders)
       recommListResponseJson = json.loads(recommListResponse.text)
       print("Fetched the Azure Advisor recommendations list")

    except:
       print("Error while fetching Azure Advisor recommendations list")

    return recommListResponseJson


# Function to fetch Recommendation Details

def fetchRecommDetails(resourceId, accessToken, apiVersion):

    recommDetailsResponseJson = None
   
    try: 
       recommDetailsURL = "https://management.azure.com"+resourceId+"?api-version="+apiVersion
       recommDetailsHeaders = {"Authorization":"Bearer "+accessToken, "Content-Type":"application/json"}
       recommDetailsResponse = requests.get(url=recommDetailsURL, headers=recommDetailsHeaders)
       recommDetailsResponseJson = json.loads(recommDetailsResponse.text)
       print("Fetched the Azure Advisor recommendation details")

    except:
       print("Error while fetching Azure Advisor recommendations details")

    return recommDetailsResponseJson


# Fetch AccessToken

accessToken = fetchAccessToken(tenant_id, client_id, client_secret, resource, subscription_id, grant_type)


# Fetch OperationId  

operationId = fetchOpId(subscription_id, accessToken, apiVersion)

if operationId != "":
   #Fetch Generation status 
   generationStatus = fetchGenStatus(operationId, subscription_id, accessToken, apiVersion, sleepTimeInSecs, retryCtr)

   if generationStatus == True:
      # Fetch Recommendations List 
      recommList = fetchRecommList(subscription_id, accessToken, apiVersion)
      for i in recommList['value']:
          if i['properties']['category'] == "Cost":
              #Fetch Recommendation Details
              #For this example, we are just fetching the first recommendation detail which is related to Cost
              recommDetails = fetchRecommDetails(i['id'], accessToken, apiVersion)
              print("****Recommendation Details****")
              print(recommDetails)
              break
else:
   print("OperationId fetch unsuccessful....exiting now")

