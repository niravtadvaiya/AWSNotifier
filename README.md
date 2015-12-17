Introduction
============
For system-wide visibility into AWS cloud resources and applications, user can leverage AWS messaging and monitoring services such as AWS Simple Notification Services (SNS) and AWS CloudWatch to get notification for critical events such as CPU usage, Disk usage, application performance etc. To receive such notifications as SMS on mobile, user can use the AWSNotifier app that makes it easy to set up, operate, and send notifications from the AWS cloud. This app collects published messages from AWS service such as AWS SNS and immediately deliver them to subscriber’s mobile as SMS.

AWSNotifier is a web service which sends SMS using the Nexmo Messaging APIs. This service communicates with AWS SNS service and sends SMS notification to the configured phone number whenever the defined condition satisfies.

Use Case
========

For AWS cloud resources and applications, enable AWS Administrator to receive real-time SMS notifications wherever they are.

Prerequisites 
=============
 - Python 2.7
 - AWS user with administrative privileges
 - Nexmo subscription and corresponding Nexmo API keys (Keys and Secret). To access the API keys, see appendix section.

Features
========
 - Enable and disable SMS functionality
 - Send AWS notifications as SMS
 - Easy integration and configuration with SNS
 - User friendly UI
 - Real time notification
 - It supports Ubuntu operating systems (OS)
 - Compatible with any AWS service which is mapped to AWS SNS
 
 
Steps to deploy the AWSNotifier
=================================
To install the AWSNotifier app on Ubuntu, follow the below steps:
1.  Go to AWS Instance terminal ie. Putty or SSH
2.  Clone the AWSNotifier repository use the following commands.**
	** cd ~**
	**git clone [Visit GitHub!](https://www.github.com)**
![](https://github.com/niravtadvaiya/AWSNotifier/blob/master/docs/1.png?raw=true)
3.  Change the directory to the AWSNotifier.
	**cd AWSNotifier**

4.  Run the following command to install and configure the Nexmo services.
	**sudo python install.py**
This will install the following on AWS instance*:*

-   Django 1.8.5

-   Nexmo library

-   Python 2.7

AWS security settings
=====================

1.  Login to the AWS Web Console.

2.  Select EC2 Service.

3.  On EC2 dashboard, select the EC2 instance where you have installed the Nexmo **AWSNotifier**.

4.  Click on the **Security groups** link as shown in the image below:
![](https://github.com/niravtadvaiya/AWSNotifier/blob/master/docs/2.png)
5.  Select **Inbound** and click on **Edit** as shown in the image below.
![](https://github.com/niravtadvaiya/AWSNotifier/blob/master/docs/3.png?raw=true)
1.  In the popup, click on **Add Rule** to define the rule to access on internet.

2.  Select the **Custom TCP Rule,** and set the port number as **9033** and set source as **0.0.0.0/0** or specific IP to access internet as shown in the below image:

![](https://github.com/niravtadvaiya/AWSNotifier/blob/master/docs/4.png?raw=true)


1.  Click on **Save**.

Steps to use the AWSNotifier app
================================

1.  Go to the browser and type **&lt;&lt;AWS Instance IP&gt;&gt;:9033** (replace AWS Instance IP with your instance public IP address).

2.  Login with default credentials - username: **admin** and password: **admin.**
![](https://github.com/niravtadvaiya/AWSNotifier/blob/master/docs/4.png?raw=true)
3.  Click on **Login**.
4.  Solarized flips between light and dark modes. In each mode, four monotones form
the core values (with an optional fifth for emphasized content).


(https://github.com/niravtadvaiya/AWSNotifier/blob/master/docs/5.png)
5.  Click on **Save**.
