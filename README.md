# azadvisorapisclient
Python based sample client application to demonstrate how to consume the RESTful APIs of Azure Advisor and to fetch the recommendations.

## Background
Azure Advisor is a service in Azure which helps one optimize the deployments on Azure. More information here - https://docs.microsoft.com/en-us/azure/advisor/advisor-overview <br />

Azure Advisor also has a set of RESTful APIs to generate and fetch the recommendations. The same can be found at: https://docs.microsoft.com/en-us/rest/api/advisor/recommendations <br />

## Flow
The flow for using these APIs is as follows: <br />

**Step 1:** First, the Access Token needs to be fetched for using the RESTful APIs. <br />
For fetching the access token an Azure Active Directory service principal needs to be created -- https://docs.microsoft.com/en-us/cli/azure/ad/sp?view=azure-cli-latest#az-ad-sp-create-for-rbac . <br />
The default command for the same is: <br />
az ad sp create-for-rbac -n "<sp_name>"

The above command gives the below output: <br />
{ "appId": "", "displayName": "<sp_name>", "name": "http://<sp_name>", "password": "<sp_password>", "tenant": "<tenant_id>" } <br />

The above values need to be entered in the file - **advrecomm.py**. In advrecomm.py, the function **fetchAccessToken** is used to fetch the access token. <br />

**Step 2:** Use the **Generate Recommendations** API to generate the recommendation process - https://docs.microsoft.com/en-us/rest/api/advisor/recommendations/generate. <br /> It is an asynchronous process. This API returns an **OperationId** which can be used to check the status of the recommendation generation process. The advrecomm.py, the function **fetchOpId** uses this API. <br />

**Step 3:** The recommendation generation status can be checked using the **OperationId** - https://docs.microsoft.com/en-us/rest/api/advisor/recommendations/getgeneratestatus. <br /> If the API returns an HTTP response code as **202**, it means that the recommendation generation is still in progress. If it generates HTTP response code of **204**, it means that the recommendation generation process is complete. In advrecomm.py, **fetchGenStatus** function is used to invoke the **Generate Recommendations** API to check the status. <br />

**Step 4:** After the recommendation generation is complete, the generated recommendations are cached. A list of these generated recommendations can be fetched using the **Recommendations** API - https://docs.microsoft.com/en-us/rest/api/advisor/recommendations/list <br />. In advrecomm.py, the function **fetchRecommList** is used used to fetch the list of recommendations. <br />

**Step 5:** If it is desired to seek details of any of the recommendations, then the API needs to be passed the **Resource Id** of the Azure resource along with the **Recommendation Id** - https://docs.microsoft.com/en-us/rest/api/advisor/recommendations/get. <br /> These details can be found in the **id** field of the JSON response returned by the **fetchRecommList** (in the previous step). This data in the **id** field is used to fetch the detailed recommendation for a particular Azure resource. The function **fetchRecommDetails** does it. <br />
Please note that for this example, we have invoked the function **fetchRecommDetails** only for one recommendation of the **Cost** category. This can be tweaked to fetch the details to the desired recommendations. <br />





