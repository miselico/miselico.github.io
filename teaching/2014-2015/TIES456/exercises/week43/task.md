Cloud Services
========================

Goal
----
In this exercises we will look at the different products offered by a cloud service provider
In particular different groups will try out different products and present their findings in the final lectures.

Prerequisites
-------------

Find out what [availability zones are in aws](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) .
Try to log in to aws. First you need to get your personal password from [http://ties456aws.appspot.com](http://ties456aws.appspot.com).



Task
----
Your task is depending on what topic your group picks. 
While you are doing the task you have to keep the following things in mind:

* How does it work?
* What do you have to pay? How is the pricing? Are there hidden costs?
* How expensive is this particular thing?

Then you make a cost estimate and add it to the README.txt file in the repository for this week.
Also add all code artifacts to the repository.

During the last review session, each group is supposed to give a short presentation about the what the service is, how much it costs and what you did with it.

Depending on the task you will work in a given availability zone.

* [AWS OpsWorks](https://console.aws.amazon.com/opsworks/home?#firstrun) DevOpsApplication Management Service
    * Make a set-up similar to the one described in the [getting started video](https://www.youtube.com/watch?v=9NnWJsS4Y2c)
    * Host a simple PHP webpage which displays a form in which the user can enter a date. After submitting the form the user sees the number of days since that date.
    * Availability Zone : US East (N. Virginia)
    * group 1
* [Amazon CloudFront](https://console.aws.amazon.com/cloudfront/home) Global content delivery framework
    * Get a video stream from Amazon CloudFront working from S3
    * Availability Zone : US West (Oregon)
    * group 4
* [Elastic MapReduce](https://console.aws.amazon.com/elasticmapreduce/home) Managed Hadoop framework
    * Implement a map reduce job on top of this infrastructure
    * You can base your application on [this article with a word count example](http://aws.amazon.com/articles/2273) but you should use another problem and a custom reducer.
    * Use a dataset with a size big enough to have a realistic running time for instance from [freely available data sets](http://aws.amazon.com/datasets)
    * Availability Zone : US West (N. California)
    * group 8
* [Elastic Transcoder](https://console.aws.amazon.com/elastictranscoder/home) Media transcoding in the cloud
    * Transcode video using pipelines, jobs and presets
    * Availability Zone : EU (Ireland)
    * group 6
* [SQS](https://console.aws.amazon.com/sqs/home) Message queue service
    * Create two applications (a publisher and a consumer)
    * Communicate between the two using the queuing system
    * Availability Zone : Asia Pacific (Singapore)
    * group 3
* [Amazon SWF](https://console.aws.amazon.com/swf/home) Amazon Simple Workflow Service 
    * Implement a workflow with 5 workers and 4 deciders. (amounts are flexible)
    * Availability Zone : Asia Pacific (Tokyo)
    * group 2
* [Amazon CloudSearch](https://console.aws.amazon.com/cloudsearch/home)
    * Configure a search domain
    * Add data from one of the [freely available data sets](http://aws.amazon.com/datasets) (Keep the size within limits)
    * Provide a small web-interface to perform searches
    * Availability Zone : Asia Pacific (Sydney)
    * group 7
* [Elasticache](https://console.aws.amazon.com/elasticache/home) In memory cache in the cloud
    * Try both Memcached and Redis caching
    * Write an application which is using this cache and an S3 or other database solution as a back-end.
    * Availability Zone : South America (São Paulo)
    * group 5

### Returning the task###
* Code in the repo
* Presentation in class


### Questions ###
Ask your own questions [http://ties456.it.jyu.fi/q2a/index.php?qa=questions&qa_1=week42](http://ties456.it.jyu.fi/q2a/index.php?qa=questions&qa_1=week42).






Hints
-----
* Be creative
