# Crimson Hexagon API Documentation

**API URL: `https://api.crimsonhexagon.com/api`**

## Endpoints

### Analysis Request
##### To submit an analysis task for asynchronous processing  - Category: results
##### `/results` - POST
##### Parameters

##### Response
* `status` - Defines the status of the analysis. Refer to Response Statuses table for additional information
	- Type: Status
	- Restricted = False
* `resultId` - Defines the unique identifier by which the analysis status/results can be retrieved
	- Type: long
	- Restricted = False
* `retrieveAt` - Nullable. ISO8601 formatted date indicating a suggested time to re-attempt result retrieval if the status is WAITING
	- Type: Date
	- Restricted = False
* `request` - Defines the original request parameters made to invoke this analysis
	- Type: ApiAnalysisTaskRequest
	- Restricted = False
	- Fields: `analysis`, `startDate`, `endDate`, `timezone`, `sources`, `keywords`, `languages`, `locations`, `gender`, `requestingContractInfo`
* `resultsUri` - Defines the URI that can be queried to retrieve the analysis status/results in the future
	- Type: String
	- Restricted = False
* `contractInfo` - If requested, the contract info after this request has been processed.
	- Type: ApiAnalysisContractInfo
	- Restricted = False

-------------------------

### Analysis Results
##### To retrieve the status of the analysis task and the results - Category: results
##### `/results/{resultId}` - GET
##### Parameters

##### Response
* `status` - Defines the status of the analysis. Refer to Response Statuses table for additional information
	- Type: Status
	- Restricted = False
* `resultId` - Defines the unique identifier by which the analysis status/results can be retrieved
	- Type: long
	- Restricted = False
* `retrieveAt` - Nullable. ISO8601 formatted date indicating a suggested time to re-attempt result retrieval if the status is WAITING
	- Type: Date
	- Restricted = False
* `request` - Defines the original request parameters made to invoke this analysis
	- Type: ApiAnalysisTaskRequest
	- Restricted = False
	- Fields: `analysis`, `startDate`, `endDate`, `timezone`, `sources`, `keywords`, `languages`, `locations`, `gender`, `requestingContractInfo`
* `resultsUri` - Defines the URI that can be queried to retrieve the analysis status/results in the future
	- Type: String
	- Restricted = False
* `contractInfo` - If requested, the contract info after this request has been processed.
	- Type: ApiAnalysisContractInfo
	- Restricted = False
* `resultId` - Identificator of the task response
	- Type: long
	- Restricted = False
* `status` - Current status of analysis task
	- Type: Status
	- Restricted = False
* `analysisResults` - Analysis result
	- Type: AnalysisResults
	- Restricted = False
	- Fields: `volumeResults`, `sentimentResults`, `genderResult`, `ageResult`, `locationResult`, `siteResult`, `affinityResults`, `reach`
* `message` - Result message
	- Type: String
	- Restricted = False
* `request` - Related task request
	- Type: ApiAnalysisTaskRequest
	- Restricted = False
	- Fields: `analysis`, `startDate`, `endDate`, `timezone`, `sources`, `keywords`, `languages`, `locations`, `gender`, `requestingContractInfo`

-------------------------

### Authentication
##### Generate authentication tokens for use in API requests - Category: admin
##### `/authenticate` - GET
##### Parameters
* `username` - Username of the requesting user
	- Type: String
	- Required = True
* `password` - Password of the requesting user
	- Type: String
	- Required = True
* `force` - If true, forces authentication token update for the requesting user
	- Type: boolean
	- Required = False
* `noExpiration` - If true, the authentication token returned will not expire
	- Type: boolean
	- Required = False

##### Response
* `auth` - Authentication token
	- Type: String
	- Restricted = False
* `expires` - Token expiration date (24 hours from token creation). If noExpiration = true, this field will not be returned
	- Type: Date
	- Restricted = False

-------------------------

### Authors
##### Information about Twitter authors in a monitor - Category: results
##### `/monitor/authors` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in YYYY-MM-DD
	- Type: Date
	- Required = True
* `end` - Specifies exclusive end date in YYYY-MM-DD
	- Type: Date
	- Required = True

##### Response
* `authors` - JSON array of zero or more authors objects that contain author-specific attributes
	- Type: List
	- Restricted = False
	- Fields: `startDate`, `endDate`, `countsByAuthor`, `numberOfAuthors`, `docsPerAuthor`, `totalImpressions`

-------------------------

### Content Delete
##### Delete content via the API - Category: admin
##### `/content/delete` - POST
##### Parameters
* `documentType` - The id of the document type to delete documents from
	- Type: long
	- Required = True

##### Response

-------------------------

### Content Delete
##### Delete batch content via the API - Category: admin
##### `/content/delete` - POST
##### Parameters
* `documentType` - The id of the document type to delete documents from
	- Type: long
	- Required = True
* `batch` - The id of the document batch to delete
	- Type: String
	- Required = True

##### Response

-------------------------

### Content Source Create
##### Content Source creation - Category: admin
##### `/content/sources` - POST
##### Parameters

##### Response
* `contentSource` - Content Source
	- Type: ContentSourceModel
	- Restricted = False
	- Fields: `id`, `teamName`, `name`, `description`, `documents`

-------------------------

### Content Source Delete
##### Content Source deletion - Category: admin
##### `/content/sources` - DELETE
##### Parameters
* `documentType` - The id of the document type to delete
	- Type: long
	- Required = True

##### Response

-------------------------

### Content Source List
##### Content Source list - Category: admin
##### `/content/sources/list` - GET
##### Parameters
* `team` - The id of the team to which the listed content sources belong
	- Type: Long
	- Required = True

##### Response
* `contentSources` - Content Sources
	- Type: List
	- Restricted = False
	- Fields: `id`, `teamName`, `name`, `description`, `documents`

-------------------------

### Content Upload
##### Upload content via the API - Category: admin
##### `/content/upload` - POST
##### Parameters

##### Response
* `uploadCount` - The number of posts that were successfully uploaded
	- Type: Integer
	- Restricted = False
* `DocumentsUploadedInLastTwentyFourHours` - If requested, the number of documents this organization has uploaded in the last twenty four hours.
	- Type: Long
	- Restricted = False
* `ContractedDocumentsWithinTwentyFourHours` - If requested, the number of documents this organization can upload in a rolling twenty four hour period.
	- Type: Long
	- Restricted = False

-------------------------