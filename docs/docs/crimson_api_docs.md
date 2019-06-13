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
	- Fields: `analysis`, `startDate`, `endDate`, `timezone`, `sources`, `keywords`, `languages`, `locations`, `gender`, `requestingContractInfo`
	- Restricted = False
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
	- Fields: `analysis`, `startDate`, `endDate`, `timezone`, `sources`, `keywords`, `languages`, `locations`, `gender`, `requestingContractInfo`
	- Restricted = False
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
	- Fields: `volumeResults`, `sentimentResults`, `genderResult`, `ageResult`, `locationResult`, `siteResult`, `affinityResults`, `reach`
	- Restricted = False
* `message` - Result message
	- Type: String
	- Restricted = False
* `request` - Related task request
	- Type: ApiAnalysisTaskRequest
	- Fields: `analysis`, `startDate`, `endDate`, `timezone`, `sources`, `keywords`, `languages`, `locations`, `gender`, `requestingContractInfo`
	- Restricted = False

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
	- Fields: `startDate`, `endDate`, `countsByAuthor`, `numberOfAuthors`, `docsPerAuthor`, `totalImpressions`
	- Restricted = False

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
	- Fields: `id`, `teamName`, `name`, `description`, `documents`
	- Restricted = False

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
	- Fields: `id`, `teamName`, `name`, `description`, `documents`
	- Restricted = False

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

### Content Upload Custom Fields Support
##### Upload content via the API w/ custom fields support - Category: admin
##### `/content/upload` - POST
##### Parameters
* `documentType` - The id of the document type to which the uploading docs will belong
	- Type: Long
	- Required = True
* `batch` - The id of the batch to which the uploading docs will belong
	- Type: String
	- Required = False

##### Response
* `batchId` - The id of the batch to which these docs belong
	- Type: String
	- Restricted = False

-------------------------

### Day and Time
##### Volume information for a monitor aggregated by time of day or day of week) - Category: results
##### `/monitor/dayandtime` - GET
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
* `aggregatebyday` - If true, volume information will be aggregated by day of the week instead of time of day
	- Type: boolean
	- Required = False
* `uselocaltime` - If true, volume aggregation will use the time local to the publishing author of a post when determining counts by day/time, instead of converting that time to the timezone of the selected monitor
	- Type: boolean
	- Required = False

##### Response
* `volumes` - JSON array of zero or more objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `numberOfDocuments`, `volume`
	- Restricted = False

-------------------------

### Demographics - Age
##### Daily volume information for age in a monitor - Category: results
##### `/monitor/demographics/age` - GET
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
* `ageCounts` - JSON array of zero or more objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `numberOfDocuments`, `ageCount`
	- Restricted = False

-------------------------

### Demographics - Gender
##### Daily volume information for gender in a monitor - Category: results
##### `/monitor/demographics/gender` - GET
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
* `genderCounts` - JSON array of zero or more objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `numberOfDocuments`, `genderCounts`
	- Restricted = False

-------------------------

### Facebook Admin Posts
##### Daily likes, comments, and shares for individual admin posts made by a Facebook account in a Facebook social account monitor - Category: social
##### `/monitor/facebook/adminposts` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `adminPostMetrics`
	- Restricted = False

-------------------------

### Facebook Page Likes
##### Total page likes as of the requested dates for a Facebook social monitor - Category: social
##### `/monitor/facebook/pagelikes` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `date`, `likes`
	- Restricted = False

-------------------------

### Facebook Total Activity
##### Daily total likes, comments, and shares on admin and user posts for a Facebook account in a Facebook social monitor - Category: social
##### `/monitor/facebook/totalactivity` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `admin`, `user`
	- Restricted = False

-------------------------

### Geography - All Resources
##### Returns all the available geolocation resources - Category: util
##### `/geography/info/all` - GET
##### Parameters

##### Response
* `resources` - JSON array with the geography resources
	- Type: List
	- Fields: `id`, `name`, `country`, `state`, `city`, `latitude`, `longitude`
	- Restricted = False

-------------------------

### Geography - Cities
##### Returns all the available cities / urban areas in the given country - Category: util
##### `/geography/info/cities` - GET
##### Parameters
* `country` - Specifies the ISO 3166 3 letter country code
	- Type: String
	- Required = True

##### Response
* `resources` - JSON array with the geography resources
	- Type: List
	- Fields: `id`, `name`, `country`, `state`, `city`, `latitude`, `longitude`
	- Restricted = False

-------------------------

### Geography - Countries
##### Returns all the available countries - Category: util
##### `/geography/info/countries` - GET
##### Parameters

##### Response
* `resources` - JSON array with the geography resources
	- Type: List
	- Fields: `id`, `name`, `country`, `latitude`, `longitude`
	- Restricted = False

-------------------------

### Geography - States
##### Returns all the available states / regions in the given country - Category: util
##### `/geography/info/states` - GET
##### Parameters
* `country` - Specifies the ISO 3166 3 letter country code
	- Type: String
	- Required = True

##### Response
* `resources` - JSON array with the geography resources
	- Type: List
	- Fields: `id`, `name`, `country`, `state`, `latitude`, `longitude`
	- Restricted = False

-------------------------

### Get Monitor Creation Report
##### Returns a list of Teams within an Organization and how many monitors were created during a given time period - Category: reports
##### `/report/monitorCreation` - GET
##### Parameters
* `organizationId` - The id of the organization being requested
	- Type: long
	- Required = True

##### Response
* `data` - List of 0..n monitor creation report rows
	- Type: List
	- Fields: `team_name`, `monitors_used`, `monitor_limit`, `monitors_created_past_month`
	- Restricted = False

-------------------------

### Get Social Site Report
##### Returns a list of social sites and associated usernames for Teams within an Organization. Also indicates which of the social sites have failed and when - Category: reports
##### `/report/socialSites` - GET
##### Parameters
* `organizationId` - The id of the organization being requested
	- Type: long
	- Required = True

##### Response
* `data` - List of 0..n social site report rows
	- Type: List
	- Fields: `username`, `socialsite`, `team_name`, `creation_date`, `last_rate_limit_date`, `failed`, `failure_date`
	- Restricted = False

-------------------------

### Get User Activity Report
##### Returns a list of users within an Organization including information on when they last logged into the platform, the last monitor they created, and the last monitor they viewed - Category: reports
##### `/report/userActivity` - GET
##### Parameters
* `organizationId` - The id of the organization being requested
	- Type: long
	- Required = True

##### Response
* `data` - List of 0..n user activity report rows
	- Type: List
	- Fields: `user_id`, `team_id`, `email`, `first_name`, `last_name`, `last_platform_login`, `team_name`, `monitors_viewed_past_month`, `monitors_created_past_month`, `last_team_visit`
	- Restricted = False

-------------------------

### Get User Invitation Report
##### Returns a list of users within an Organization and which Team(s) they were invited to. Also indicates when the invitation was sent and when it was accepted - Category: reports
##### `/report/userInvitations` - GET
##### Parameters
* `organizationId` - The id of the organization being requested
	- Type: long
	- Required = True

##### Response
* `data` - List of 0..n user invitation report rows
	- Type: List
	- Fields: `email`, `team_name`, `create_edit`, `invite_user`, `heliosight`, `api_access`, `admin`, `date_sent`, `date_accepted`
	- Restricted = False

-------------------------

### Image Analysis Request
##### To return list of class IDs and names with specified class type. - Category: results
##### `/imageanalysis/resources/classes/type` - GET
##### Parameters

##### Response

-------------------------

### Image Analysis Request
##### To return list of all class IDs and names. - Category: results
##### `/imageanalysis/resources/classes` - GET
##### Parameters

##### Response

-------------------------

### Image analysis
##### To return image classification data - Category: util
##### `/imageanalysis` - GET
##### Parameters
* `url` - Image URL
	- Type: String
	- Required = True

##### Response
* `imgData` - Message object contains request parameters and image classification result
	- Type: ImageAnalysisData
	- Restricted = False

-------------------------

### Instagram Followers
##### Total daily follower counts for Instagram social account monitors - Category: social
##### `/monitor/instagram/followers` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `date`, `followerCount`
	- Restricted = False

-------------------------

### Instagram Hashtags
##### Total daily volume by Instagram hashtags for specific monitor - Category: social
##### `/monitor/instagram/hashtags` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `date`, `hashtags`
	- Restricted = False

-------------------------

### Instagram Sent Media
##### Daily likes, comments, and tags for individual media posted by an Instagram account in an Instagram social account monitor - Category: social
##### `/monitor/instagram/sentmedia` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `adminPostMetrics`
	- Restricted = False

-------------------------

### Instagram Total Activity
##### Daily likes, comments, and shares for individual admin posts made by an Instagram account in an Instagram social account monitor - Category: social
##### `/monitor/instagram/totalactivity` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `admin`
	- Restricted = False

-------------------------

### Interest Affinities
##### Aggregate affinities for the selected monitor over a given date range - Category: visualizations
##### `/monitor/interestaffinities` - GET
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
* `daily` - If true, results returned from this endpoint will be trended daily instead of aggregated across the selected date range.
	- Type: boolean
	- Required = False
* `documentsource` - document source for affinities. valid params [TWITTER, TUMBLR]
	- Type: String
	- Required = False

##### Response
* `startDate` - Inclusive start date in dashboard time for this result - ISO 8601 format yyyy-MM-dd'T'HH:mm:ss
	- Type: Date
	- Restricted = False
* `endDate` - Exclusive end date in dashboard time for this result - ISO 8601 format yyyy-MM-dd'T'HH:mm:ss
	- Type: Date
	- Restricted = False
* `affinityInfo` - JSON array of affinity objects containing information about the top affinities for the date range selected
	- Type: List
	- Fields: `id`, `name`, `relevancyScore`, `percentInMonitor`, `percentOnTwitter`
	- Restricted = False

-------------------------

### Monitor Audit
##### Audit information about the selected monitor - Category: admin
##### `/monitor/audit` - GET
##### Parameters
* `id` - The id of the monitor to be audited
	- Type: long
	- Required = True

##### Response
* `auditInfo` - JSON array of audit events pertaining to the selected monitor
	- Type: List
	- Fields: `event`, `user`, `eventDate`
	- Restricted = False

-------------------------

### Monitor Detail
##### Attributes of the specified monitor - Category: admin
##### `/monitor/detail` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
* `monitorDetail` - JSON array of monitor details
	- Type: MonitorDetailModel
	- Fields: `parentMonitorId`, `categories`, `emotions`, `id`, `name`, `description`, `type`, `enabled`, `resultsStart`, `resultsEnd`, `keywords`, `languages`, `geolocations`, `gender`, `sources`, `timezone`, `teamName`, `tags`, `subfilters`
	- Restricted = False

-------------------------

### Monitor Image Results
##### Daily image results for a monitor - Category: results
##### `/monitor/imageresults` - GET
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
* `type` - Specifies type of image classes, valid values [object, scene, action, logo]
	- Type: String
	- Required = False
* `top` - If defined, only the top number of results will be returned
	- Type: Integer
	- Required = False

##### Response
* `results` - JSON array of zero or more daily image results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `creationDate`, `numberOfDocuments`, `numberOfImageDocuments`, `imageClasses`
	- Restricted = False

-------------------------

### Monitor List
##### List of monitors available to the passed in username - Category: admin
##### `/monitor/list` - GET
##### Parameters
* `team` - The id of the team to which the listed monitors belong
	- Type: Long
	- Required = False

##### Response
* `monitors` - JSON array of monitors viewable by the user
	- Type: List
	- Fields: `id`, `name`, `description`, `type`, `enabled`, `resultsStart`, `resultsEnd`, `keywords`, `languages`, `geolocations`, `gender`, `sources`, `timezone`, `teamName`, `tags`, `subfilters`
	- Restricted = False

-------------------------

### Monitor Results
##### Daily results for a monitor - Category: results
##### `/monitor/results` - GET
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
* `hideExcluded` - If true, categories set as hidden will not be included in category proportion calculations
	- Type: boolean
	- Required = False

##### Response
* `results` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `creationDate`, `numberOfDocuments`, `numberOfRelevantDocuments`, `categories`
	- Restricted = False

-------------------------

### Monitor Results by City
##### Returns all the monitor results grouped by the cities / urban areas in a given country (if given) - Category: results
##### `/monitor/geography/cities` - GET
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
* `country` - Specifies the ISO 3166 3 letter country code, if not given all cities in the world will be returned
	- Type: String
	- Required = False

##### Response
* `startDate` - Requested start date
	- Type: Date
	- Restricted = False
* `endDate` - Requested end date
	- Type: Date
	- Restricted = False
* `totalVolume` - Volume matching the defined geography filter
	- Type: long
	- Restricted = False
* `data` - JSON array of monitor geography result information
	- Type: List
	- Fields: `info`, `volume`, `perMillion`
	- Restricted = False

-------------------------

### Monitor Results by Country
##### Returns all the monitor results grouped by country - Category: results
##### `/monitor/geography/countries` - GET
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
* `startDate` - Requested start date
	- Type: Date
	- Restricted = False
* `endDate` - Requested end date
	- Type: Date
	- Restricted = False
* `totalVolume` - Volume matching the defined geography filter
	- Type: long
	- Restricted = False
* `data` - JSON array of monitor geography result information
	- Type: List
	- Fields: `info`, `volume`, `perMillion`
	- Restricted = False

-------------------------

### Monitor Results by State
##### Returns all the monitor results grouped by the country states / regions - Category: results
##### `/monitor/geography/states` - GET
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
* `country` - Specifies the ISO 3166 3 letter country code
	- Type: String
	- Required = True

##### Response
* `startDate` - Requested start date
	- Type: Date
	- Restricted = False
* `endDate` - Requested end date
	- Type: Date
	- Restricted = False
* `totalVolume` - Volume matching the defined geography filter
	- Type: long
	- Restricted = False
* `data` - JSON array of monitor geography result information
	- Type: List
	- Fields: `info`, `volume`, `perMillion`
	- Restricted = False

-------------------------

### Monitor Training Posts
##### Download training posts for a monitor - Category: admin
##### `/monitor/trainingposts` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `category` - Category id to target training posts from a specific category
	- Type: Long
	- Required = False

##### Response
* `trainingPosts` - JSON array of training posts for the selected monitor or category in a monitor
	- Type: List
	- Fields: `categoryId`, `categoryName`, `categoryGroup`, `url`, `date`, `author`, `contents`, `title`, `type`
	- Restricted = False

-------------------------

### Posts
##### Information about posts in a monitor - Category: visualizations
##### `/monitor/posts` - GET || POST
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
* `MISSING` - Optional JSON payload to filter response
	- Type: MonitorPostsFilter
	- Required = False
* `filter` - Pipe-separated list of field:value pairs used to filter results by given parameters
	- Type: String
	- Required = False
* `extendLimit` - If true, increases the limit of returned posts from 500 per call to 10,000 per call
	- Type: boolean
	- Required = False
* `fullContents` - If true, the contents field will return the original, complete post contents instead of truncating around search terms
	- Type: boolean
	- Required = False
* `geotagged` - If true, returns only geotagged documents matching and the given filter, if false or undefined any post matching the given filter
	- Type: boolean
	- Required = False

##### Response
* `posts` - JSON array of zero or more post objects that contain post-specific attributes
	- Type: List
	- Fields: `location`, `geolocation`, `language`, `authorPosts`, `authorsFollowing`, `authorsFollowers`, `authorGender`, `trainingPost`, `assignedCategoryId`, `assignedEmotionId`, `categoryScores`, `emotionScores`, `imageInfo`, `customFields`, `batchId`, `url`, `date`, `author`, `contents`, `title`, `type`
	- Restricted = False
* `totalPostsAvailable` - The number of posts stored for this monitor that match the query. Dates in the date range selected that have more than 10 thousand posts will be sampled. You may perform extrapolation calculations to approximate the total number of unsampled posts using the results counts in the Monitor Results endpoint.
	- Type: int
	- Restricted = False

-------------------------

### Realtime Cashtags
##### Get Cashtags associated to a Monitor - Category: monitors
##### `/realtime/monitor/cashtags` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False
* `top` - The top N cashtags to retrieve
	- Type: Integer
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Configure
##### Configure the Realtime evaluators for the Monitor - Category: monitors
##### `/realtime/monitor/configure` - POST
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Details
##### Get the Realtime evaluators details for the Monitor - Category: monitors
##### `/realtime/monitor/detail` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Disable
##### Disable Realtime Data - Category: monitors
##### `/realtime/monitor/disable` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response

-------------------------

### Realtime Enable
##### Enable Realtime Data - Category: monitors
##### `/realtime/monitor/enable` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response

-------------------------

### Realtime FullRetweets
##### Get the Realtime fulretweets for the Monitor - Category: monitors
##### `/realtime/monitor/fullretweets` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime FullTweets
##### Get the Realtime fulltweets for the Monitor - Category: monitors
##### `/realtime/monitor/fulltweets` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Hashtags
##### Get Hashtags associated to a Monitor - Category: monitors
##### `/realtime/monitor/hashtags` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False
* `top` - The top N hashtags to retrieve
	- Type: Integer
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Monitor List
##### Get the Monitors which are in Proteus - Category: monitors
##### `/realtime/monitor/list` - GET
##### Parameters
* `team` - The id of the team to which the listed monitors belong
	- Type: Long
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Retweets
##### Get the Realtime retweets for the Monitor - Category: monitors
##### `/realtime/monitor/retweets` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime SocialGuids
##### Get the Realtime social guids for the Monitor - Category: monitors
##### `/realtime/monitor/socialguids` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `type` - Specifies the document type
	- Type: String
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False
* `receivedafter` - Specifies inclusive receivedafter date in epoch seconds
	- Type: Long
	- Required = False
* `maxresults` - Specifies maximum results to fetch
	- Type: Integer
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Tweets
##### Get the Realtime tweets for the Monitor - Category: monitors
##### `/realtime/monitor/tweets` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Volume
##### Get the Realtime volume for the Monitor - Category: monitors
##### `/realtime/monitor/volume` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False
* `type` - Specifies the document type to filter
	- Type: List
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Volume by Emotion
##### Get the Realtime volume by emotion for the Monitor - Category: monitors
##### `/realtime/monitor/volumebyemotion` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False
* `type` - Specifies the document type to filter
	- Type: List
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Realtime Volume by Sentiment
##### Get the Realtime volume by sentiment for the Monitor - Category: monitors
##### `/realtime/monitor/volumebysentiment` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True
* `start` - Specifies inclusive start date in epoch seconds
	- Type: Long
	- Required = False
* `type` - Specifies the document type to filter
	- Type: List
	- Required = False

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False

-------------------------

### Stream Add Monitor
##### Stream Add Monitor Association - Category: admin
##### `/stream/{streamid}/monitor/{monitorid}` - POST
##### Parameters
* `streamId` - The id of the stream
	- Type: Long
	- Required = True
* `monitorId` - The id of the monitor to which the association will be created
	- Type: Long
	- Required = True

##### Response

-------------------------

### Stream Create
##### Stream creation - Category: admin
##### `/stream` - POST
##### Parameters

##### Response
* `stream` - Stream information
	- Type: StreamModel
	- Fields: `id`, `name`, `teamName`, `monitors`
	- Restricted = False
* `path` - Stream path
	- Type: String
	- Restricted = False

-------------------------

### Stream Delete
##### Stream deletion - Category: admin
##### `/stream/{streamid}` - DELETE
##### Parameters
* `streamId` - The id of the stream to delete
	- Type: Long
	- Required = True

##### Response

-------------------------

### Stream List
##### List of streams available to the passed in username - Category: admin
##### `/stream/list` - GET
##### Parameters
* `teamid` - The id of the team to which the listed streams belong
	- Type: Long
	- Required = False

##### Response
* `streams` - JSON array of streams viewable by the user
	- Type: List
	- Fields: `id`, `name`, `teamName`, `monitors`
	- Restricted = False

-------------------------

### Stream Posts
##### Information about posts in a stream - Category: results
##### `/stream/{streamid}/posts` - GET
##### Parameters
* `streamId` - The id of the stream to which the realtime information belongs
	- Type: Long
	- Required = True
* `count` - The maximum number of posts to fetch from the stream
	- Type: Integer
	- Required = False

##### Response
* `posts` - JSON array of zero or more post objects that contain post-specific attributes
	- Type: List
	- Fields: `location`, `geolocation`, `language`, `authorPosts`, `authorsFollowing`, `authorsFollowers`, `authorGender`, `trainingPost`, `assignedCategoryId`, `assignedEmotionId`, `categoryScores`, `emotionScores`, `imageInfo`, `customFields`, `batchId`, `url`, `date`, `author`, `contents`, `title`, `type`
	- Restricted = False
* `totalPostsAvailable` - The number of posts stored for this monitor that match the query. Dates in the date range selected that have more than 10 thousand posts will be sampled. You may perform extrapolation calculations to approximate the total number of unsampled posts using the results counts in the Monitor Results endpoint.
	- Type: int
	- Restricted = False

-------------------------

### Stream Remove Monitor
##### Stream Remove Monitor Association - Category: admin
##### `/stream/{streamid}/monitor/{monitorid}` - DELETE
##### Parameters
* `streamId` - The id of the stream
	- Type: Long
	- Required = True
* `monitorId` - The id of the monitor to which the association will be removed
	- Type: Long
	- Required = True

##### Response

-------------------------

### Stream Update Monitor
##### Stream Update Monitor Data - Category: admin
##### `/stream/{streamid}` - POST
##### Parameters
* `streamId` - The id of the stream
	- Type: Long
	- Required = True

##### Response

-------------------------

### Team List
##### List of teams accessible to the current user - Category: admin
##### `/team/list` - GET
##### Parameters

##### Response
* `teams` - JSON array of teams accessible by the user
	- Type: List
	- Fields: `id`, `name`
	- Restricted = False

-------------------------

### Top Sites and Content Sources
##### Content source breakdown and top sites - Category: results
##### `/monitor/sources` - GET
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
* `contentSources` - JSON array of zero or more content sources objects that contain results for each date requested
	- Type: List
	- Fields: `startDate`, `endDate`, `topSites`, `sources`
	- Restricted = False

-------------------------

### Topic Clustering
##### XML data that can be used to generate clustering visualizations using third-party software - Category: visualizations
##### `/monitor/topics` - GET || POST
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
* `MISSING` - Optional JSON payload to filter response
	- Type: MonitorPostsFilter
	- Required = False
* `filter` - Pipe-separated list of field:value pairs used to filter results by given parameters
	- Type: String
	- Required = False

##### Response
* `clustering` - XML string for generating visualizations
	- Type: String
	- Restricted = False

-------------------------

### Topic Waves
##### Topic waves information for a monitor - Category: visualizations
##### `/monitor/topicwaves` - GET || POST
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
* `MISSING` - Optional JSON payload to filter response
	- Type: MonitorPostsFilter
	- Required = False

##### Response
* `startDate` - Inclusive start date in dashboard time for this result - ISO 8601 format yyyy-MM-dd'T'HH:mm:ss
	- Type: Date
	- Restricted = False
* `endDate` - Exclusive end date in dashboard time for this result - ISO 8601 format yyyy-MM-dd'T'HH:mm:ss
	- Type: Date
	- Restricted = False
* `timezone` - IANA timezone identifier specifying the timezone for all dates in the response
	- Type: String
	- Restricted = False
* `groupBy` - Defines the grouping for the volume information
	- Type: String
	- Restricted = False
* `totalTopicsVolume` - Total Volume for the topics
	- Type: long
	- Restricted = False
* `topics` - JSON array of 1..n topics volume information for grouped periods
	- Type: List
	- Fields: `name`, `totalVolume`, `volume`
	- Restricted = False

-------------------------

### Training Document Upload
##### Train monitors via the API - Category: util
##### `/monitor/train` - POST
##### Parameters
* `id` - The id of the monitor being trained
	- Type: long
	- Required = True

##### Response
* `message` - Success response indicating a training post has been sucessfully uploaded
	- Type: String
	- Restricted = False

-------------------------

### Twitter Engagement Metrics
##### Engagement metrics for Twitter content in a monitor - Category: results
##### `/monitor/twittermetrics` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `topHashtags`, `topMentions`, `topRetweets`
	- Restricted = False

-------------------------

### Twitter Followers
##### Total daily follower counts for Twitter Social Account monitors - Category: social
##### `/monitor/twittersocial/followers` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `date`, `followers`
	- Restricted = False

-------------------------

### Twitter Sent Posts
##### Daily retweets, replies, and impressions for individual posts made by a Twitter account in a Twitter social account monitor - Category: social
##### `/monitor/twittersocial/sentposts` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `sentPostMetrics`, `totalImpressions`
	- Restricted = False

-------------------------

### Twitter Total Engagement
##### Daily retweets, replies, and mentions for a targeted Twitter account in a Twitter social account monitor - Category: social
##### `/monitor/twittersocial/totalengagement` - GET
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
* `dailyResults` - JSON array of zero or more daily results objects that contain endpoint-specific attributes
	- Type: List
	- Fields: `startDate`, `endDate`, `mentions`, `replies`, `retweets`
	- Restricted = False

-------------------------

### Volume
##### Volume of total posts in a monitor - Category: results
##### `/monitor/volume` - GET
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
* `groupBy` - Specifies how the volume data over the date range will be grouped. Valid values: [HOURLY, DAILY, WEEKLY, MONTHLY]. Defaults to DAILY. Grouping requires a date range of at least 1 full unit; e.g., WEEKLY requires a date range of at least 1 week. Grouping only returns full units so the range may be truncated. e.g., 2017-01-15 to 2017-03-15 with MONTHLY grouping will return a date range of 2017-02-01 to 2017-03-01. A monitor must have complete results for the specified date range. If any day in the range is missing results an error will be returned.
	- Type: String
	- Required = False

##### Response
* `startDate` - Inclusive start date in dashboard time for this result - ISO 8601 format yyyy-MM-dd'T'HH:mm:ss
	- Type: Date
	- Restricted = False
* `endDate` - Exclusive end date in dashboard time for this result - ISO 8601 format yyyy-MM-dd'T'HH:mm:ss
	- Type: Date
	- Restricted = False
* `timezone` - IANA timezone identifier specifying the timezone for all dates in the response
	- Type: String
	- Restricted = False
* `groupBy` - Defines the grouping for the volume information
	- Type: String
	- Restricted = False
* `numberOfDocuments` - Total volume for this period
	- Type: long
	- Restricted = False
* `volume` - JSON array of 1..n volume information for grouped periods
	- Type: List
	- Fields: `startDate`, `endDate`, `numberOfDocuments`
	- Restricted = False

-------------------------

### Word Cloud
##### Word frequency information for posts in a monitor - Category: visualizations
##### `/monitor/wordcloud` - GET || POST
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
* `MISSING` - Optional JSON payload to filter response
	- Type: MonitorPostsFilter
	- Required = False
* `filter` - Pipe-separated list of field:value pairs used to filter results by given parameters
	- Type: String
	- Required = False

##### Response
* `data` - Map of the top 300 terms appearing in a monitor to their frequency in that monitor
	- Type: Map
	- Restricted = False

-------------------------