# Crimson Hexagon API Documenttion
**ROOT_URL = `https://api.crimsonhexagon.com/api/`**

### Table of Contents
* [Analysis Request](#0)
* [Analysis Results](#1)
* [Authentication](#2)
* [Authors](#3)
* [Content Upload](#4)
* [Day and Time](#5)
* [Demographics - Age](#6)
* [Demographics - Gender](#7)
* [Facebook Admin Posts](#8)
* [Facebook Page Likes](#9)
* [Facebook Total Activity](#10)
* [Geography - All Resources](#11)
* [Geography - Cities](#12)
* [Geography - Countries](#13)
* [Geography - States](#14)
* [Get Monitor Creation Report](#15)
* [Get Social Site Report](#16)
* [Get User Activity Report](#17)
* [Get User Invitation Report](#18)
* [Image analysis](#19)
* [Instagram Followers](#20)
* [Instagram Hashtags](#21)
* [Instagram Sent Media](#22)
* [Instagram Total Activity](#23)
* [Interest Affinities](#24)
* [Monitor Audit](#25)
* [Monitor Detail](#26)
* [Monitor Dump](#27)
* [Monitor Image Results](#28)
* [Monitor List](#29)
* [Monitor Results](#30)
* [Monitor Results by City](#31)
* [Monitor Results by Country](#32)
* [Monitor Results by State](#33)
* [Monitor Training Posts](#34)
* [Posts](#35)
* [Realtime Cashtags](#36)
* [Realtime Configure](#37)
* [Realtime Details](#38)
* [Realtime Disable](#39)
* [Realtime Enable](#40)
* [Realtime Hashtags](#41)
* [Realtime Monitor List](#42)
* [Realtime Retweets](#43)
* [Realtime SocialGuids](#44)
* [Realtime Tweets](#45)
* [Realtime Volume](#46)
* [Realtime Volume by Sentiment](#47)
* [Stream Add Monitor](#48)
* [Stream Create](#49)
* [Stream Delete](#50)
* [Stream List](#51)
* [Stream Posts](#52)
* [Stream Remove Monitor](#53)
* [Stream Update Monitor](#54)
* [Team List](#55)
* [Top Sites and Content Sources](#56)
* [Topic Clustering](#57)
* [Topic Waves](#58)
* [Training Document Upload](#59)
* [Twitter Engagement Metrics](#60)
* [Twitter Followers](#61)
* [Twitter Sent Posts](#62)
* [Twitter Total Engagement](#63)
* [Volume](#64)
* [WhitelistBlacklist](#65)
* [Word Cloud](#66)

<a name="0"></a>
#### Analysis Request
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
* `resultsUri` - Defines the URI that can be queried to retrieve the analysis status/results in the future
	- Type: String
	- Restricted = False
* `contractInfo` - If requested, the contract info after this request has been processed.
	- Type: ApiAnalysisContractInfo
	- Restricted = False
-------------------------

<a name="1"></a>
#### Analysis Results
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
* `message` - Result message
	- Type: String
	- Restricted = False
* `request` - Related task request
	- Type: ApiAnalysisTaskRequest
	- Restricted = False
-------------------------

<a name="2"></a>
#### Authentication
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

<a name="3"></a>
#### Authors
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
-------------------------

<a name="4"></a>
#### Content Upload
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

<a name="5"></a>
#### Day and Time
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
	- Restricted = False
-------------------------

<a name="6"></a>
#### Demographics - Age
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
	- Restricted = False
-------------------------

<a name="7"></a>
#### Demographics - Gender
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
	- Restricted = False
-------------------------

<a name="8"></a>
#### Facebook Admin Posts
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
	- Restricted = False
-------------------------

<a name="9"></a>
#### Facebook Page Likes
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
	- Restricted = False
-------------------------

<a name="10"></a>
#### Facebook Total Activity
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
	- Restricted = False
-------------------------

<a name="11"></a>
#### Geography - All Resources
##### Returns all the available geolocation resources - Category: util
##### `/geography/info/all` - GET
##### Parameters

##### Response
* `resources` - JSON array with the geography resources
	- Type: List
	- Restricted = False
-------------------------

<a name="12"></a>
#### Geography - Cities
##### Returns all the available cities / urban areas in the given country - Category: util
##### `/geography/info/cities` - GET
##### Parameters
* `country` - Specifies the ISO 3166 3 letter country code
	- Type: String
	- Required = True

##### Response
* `resources` - JSON array with the geography resources
	- Type: List
	- Restricted = False
-------------------------

<a name="13"></a>
#### Geography - Countries
##### Returns all the available countries - Category: util
##### `/geography/info/countries` - GET
##### Parameters

##### Response
* `resources` - JSON array with the geography resources
	- Type: List
	- Restricted = False
-------------------------

<a name="14"></a>
#### Geography - States
##### Returns all the available states / regions in the given country - Category: util
##### `/geography/info/states` - GET
##### Parameters
* `country` - Specifies the ISO 3166 3 letter country code
	- Type: String
	- Required = True

##### Response
* `resources` - JSON array with the geography resources
	- Type: List
	- Restricted = False
-------------------------

<a name="15"></a>
#### Get Monitor Creation Report
##### Returns a list of Teams within an Organization and how many monitors were created during a given time period - Category: reports
##### `/report/monitorCreation` - GET
##### Parameters
* `organizationId` - The id of the organization being requested
	- Type: long
	- Required = True

##### Response
* `data` - List of 0..n monitor creation report rows
	- Type: List
	- Restricted = False
-------------------------

<a name="16"></a>
#### Get Social Site Report
##### Returns a list of social sites and associated usernames for Teams within an Organization. Also indicates which of the social sites have failed and when - Category: reports
##### `/report/socialSites` - GET
##### Parameters
* `organizationId` - The id of the organization being requested
	- Type: long
	- Required = True

##### Response
* `data` - List of 0..n social site report rows
	- Type: List
	- Restricted = False
-------------------------

<a name="17"></a>
#### Get User Activity Report
##### Returns a list of users within an Organization including information on when they last logged into the platform, the last monitor they created, and the last monitor they viewed - Category: reports
##### `/report/userActivity` - GET
##### Parameters
* `organizationId` - The id of the organization being requested
	- Type: long
	- Required = True

##### Response
* `data` - List of 0..n user activity report rows
	- Type: List
	- Restricted = False
-------------------------

<a name="18"></a>
#### Get User Invitation Report
##### Returns a list of users within an Organization and which Team(s) they were invited to. Also indicates when the invitation was sent and when it was accepted - Category: reports
##### `/report/userInvitations` - GET
##### Parameters
* `organizationId` - The id of the organization being requested
	- Type: long
	- Required = True

##### Response
* `data` - List of 0..n user invitation report rows
	- Type: List
	- Restricted = False
-------------------------

<a name="19"></a>
#### Image analysis
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

<a name="20"></a>
#### Instagram Followers
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
	- Restricted = False
-------------------------

<a name="21"></a>
#### Instagram Hashtags
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
	- Restricted = False
-------------------------

<a name="22"></a>
#### Instagram Sent Media
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
	- Restricted = False
-------------------------

<a name="23"></a>
#### Instagram Total Activity
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
	- Restricted = False
-------------------------

<a name="24"></a>
#### Interest Affinities
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
	- Restricted = False
-------------------------

<a name="25"></a>
#### Monitor Audit
##### Audit information about the selected monitor - Category: admin
##### `/monitor/audit` - GET
##### Parameters
* `id` - The id of the monitor to be audited
	- Type: long
	- Required = True

##### Response
* `auditInfo` - JSON array of audit events pertaining to the selected monitor
	- Type: List
	- Restricted = False
-------------------------

<a name="26"></a>
#### Monitor Detail
##### Attributes of the specified monitor - Category: admin
##### `/monitor/detail` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
* `monitorDetail` - JSON array of monitor details
	- Type: MonitorDetailModel
	- Restricted = False
-------------------------

<a name="27"></a>
#### Monitor Dump
##### Get detailed information of the monitor - Category: admin
##### `/monitor/dump` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
* `monitorDump` - Monitor dump
	- Type: MonitorDumpModel
	- Restricted = False
-------------------------

<a name="28"></a>
#### Monitor Image Results
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
	- Restricted = False
-------------------------

<a name="29"></a>
#### Monitor List
##### List of monitors available to the passed in username - Category: admin
##### `/monitor/list` - GET
##### Parameters
* `team` - The id of the team to which the listed monitors belong
	- Type: Long
	- Required = False

##### Response
* `monitors` - JSON array of monitors viewable by the user
	- Type: List
	- Restricted = False
-------------------------

<a name="30"></a>
#### Monitor Results
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
	- Restricted = False
-------------------------

<a name="31"></a>
#### Monitor Results by City
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
	- Restricted = False
-------------------------

<a name="32"></a>
#### Monitor Results by Country
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
	- Restricted = False
-------------------------

<a name="33"></a>
#### Monitor Results by State
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
	- Restricted = False
-------------------------

<a name="34"></a>
#### Monitor Training Posts
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
	- Restricted = False
-------------------------

<a name="35"></a>
#### Posts
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
	- Restricted = False
* `totalPostsAvailable` - The number of posts stored for this monitor that match the query. Dates in the date range selected that have more than 10 thousand posts will be sampled. You may perform extrapolation calculations to approximate the total number of unsampled posts using the results counts in the Monitor Results endpoint.
	- Type: int
	- Restricted = False
-------------------------

<a name="36"></a>
#### Realtime Cashtags
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

<a name="37"></a>
#### Realtime Configure
##### Configure the Realtime evaluators for the Monitor - Category: monitors
##### `/realtime/monitor/configure` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False
-------------------------

<a name="38"></a>
#### Realtime Details
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

<a name="39"></a>
#### Realtime Disable
##### Disable Realtime Data - Category: monitors
##### `/realtime/monitor/disable` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
-------------------------

<a name="40"></a>
#### Realtime Enable
##### Enable Realtime Data - Category: monitors
##### `/realtime/monitor/enable` - GET
##### Parameters
* `id` - The id of the monitor being requested
	- Type: long
	- Required = True

##### Response
-------------------------

<a name="41"></a>
#### Realtime Hashtags
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

<a name="42"></a>
#### Realtime Monitor List
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

<a name="43"></a>
#### Realtime Retweets
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

<a name="44"></a>
#### Realtime SocialGuids
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

##### Response
* `realtimeData` - JSON object of monitor realtime data
	- Type: Map
	- Restricted = False
-------------------------

<a name="45"></a>
#### Realtime Tweets
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

<a name="46"></a>
#### Realtime Volume
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

<a name="47"></a>
#### Realtime Volume by Sentiment
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

<a name="48"></a>
#### Stream Add Monitor
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

<a name="49"></a>
#### Stream Create
##### Stream creation - Category: admin
##### `/stream` - POST
##### Parameters

##### Response
* `stream` - Stream information
	- Type: StreamModel
	- Restricted = False
* `path` - Stream path
	- Type: String
	- Restricted = False
-------------------------

<a name="50"></a>
#### Stream Delete
##### Stream deletion - Category: admin
##### `/stream/{streamid}` - DELETE
##### Parameters
* `streamId` - The id of the stream to delete
	- Type: Long
	- Required = True

##### Response
-------------------------

<a name="51"></a>
#### Stream List
##### List of streams available to the passed in username - Category: admin
##### `/stream/list` - GET
##### Parameters
* `teamid` - The id of the team to which the listed streams belong
	- Type: Long
	- Required = False

##### Response
* `streams` - JSON array of streams viewable by the user
	- Type: List
	- Restricted = False
-------------------------

<a name="52"></a>
#### Stream Posts
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
	- Restricted = False
* `totalPostsAvailable` - The number of posts stored for this monitor that match the query. Dates in the date range selected that have more than 10 thousand posts will be sampled. You may perform extrapolation calculations to approximate the total number of unsampled posts using the results counts in the Monitor Results endpoint.
	- Type: int
	- Restricted = False
-------------------------

<a name="53"></a>
#### Stream Remove Monitor
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

<a name="54"></a>
#### Stream Update Monitor
##### Stream Update Monitor Data - Category: admin
##### `/stream/{streamid}` - POST
##### Parameters
* `streamId` - The id of the stream
	- Type: Long
	- Required = True

##### Response
-------------------------

<a name="55"></a>
#### Team List
##### List of teams accessible to the current user - Category: admin
##### `/team/list` - GET
##### Parameters

##### Response
* `teams` - JSON array of teams accessible by the user
	- Type: List
	- Restricted = False
-------------------------

<a name="56"></a>
#### Top Sites and Content Sources
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
	- Restricted = False
-------------------------

<a name="57"></a>
#### Topic Clustering
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

<a name="58"></a>
#### Topic Waves
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
	- Restricted = False
-------------------------

<a name="59"></a>
#### Training Document Upload
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

<a name="60"></a>
#### Twitter Engagement Metrics
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
	- Restricted = False
-------------------------

<a name="61"></a>
#### Twitter Followers
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
	- Restricted = False
-------------------------

<a name="62"></a>
#### Twitter Sent Posts
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
	- Restricted = False
-------------------------

<a name="63"></a>
#### Twitter Total Engagement
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
	- Restricted = False
-------------------------

<a name="64"></a>
#### Volume
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
	- Restricted = False
-------------------------

<a name="65"></a>
#### WhitelistBlacklist
##### Detailed Information about a specific whitelistblacklists associated to the monitor - Category: visualizations
##### `/whitelistblacklist/{whitelistblacklistid}/detail` - GET || POST
##### Parameters
* `whitelistBlacklistId` - The id of the whitelistblacklist being requested
	- Type: Long
	- Required = True

##### Response
* `whitelistblacklistdetail` - JSON object of whitelistblacklist detail
	- Type: WhitelistBlacklistDetailModel
	- Restricted = False
-------------------------

<a name="66"></a>
#### Word Cloud
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