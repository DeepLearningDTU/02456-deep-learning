# Installation Guide
> Installation Guide is maintained by Toke Faurby, [Toke.Faurby@gmail.com](mailto:toke.faurby@gmail.com), and Kristoffer Linder-Steinlein, [linder2411@gmail.com](mailto:linder2411@gmail.com).

For this course we will be usin Amazon Web Services ([AWS](https://aws.amazon.com/products/)). AWS provide on-deman computing facilities. Most notably they provide servers with the powerfull [NVIDIA Tesla K80](http://www.nvidia.com/object/tesla-k80.html) graphics cards, which we will be using for this course. These servers are called [p2.xlarge](https://aws.amazon.com/ec2/instance-types/p2/), and cost about 1 $US per hour of runtime. For large tasks it is possible to save money by using [spot instances](https://aws.amazon.com/ec2/spot/pricing/). A spot instances let you bid on spare Amazon EC2 instances to name your own price for compute capacity. The Spot price fluctuates based on the supply and demand of available EC2 capacity. Spot prices are generally a lot lower, e.g. p2.xlarge costs about 0.2 $US, but you risk being outbid, and having your server shut down, without notice.


Most of the technical aspects have been handled ahead of time, requiring only minimal setup on your part. If you would like to dig deepper or get the software running on your own computer a list of resources have been currated in the end of this guide.


**SECURITY WARNING**

The servers and material for this course havn't been made with security in mind, therefore assume that somebody could access your server, and any the data you put on it.


## Setup

You only need to set up the system once. Once setup is complete simply follow the instrictions in *Daily Use*.

### Windows People
If you are using Windows you must download and install Git Bash from [here](https://git-scm.com/downloads). [AWS CodeCommit](http://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-https-windows.html#setting-up-https-windows-install-git) supports Git versions 1.7.9 and later. We won't use the Git capabilities, we simply need to use it as a Bash terminal. 

Most of installation settings aren't that important. The suggested settings are:
* Check `Use a TrueType font in all consoles`. 
 * This makes things prettier, doesn't make any significant difference however.
* Check `Use Git from Windows Command Prompt`.
 * This if you also want to use Git from Winows Command Prompt. We don't need it for this course.
* 'Checkout Windows-style, commit Unix-style line endings'
 * Windows uses a different line ending character than Unix systems.
* Check `Use Windows' default console window`.
 * This configures the terminal emulator for Git Bash.

Use Git Bash as your terminal for the remainder of this guide.

**##### DO WE NEED PYTHON ON WINDOWS, or can we just get AWS CLI MSI? http://docs.aws.amazon.com/cli/latest/userguide/installing.html#install-msi-on-windows**


### Everybody

We have setup some Amazon Machine Images (AMI), and will be hosting them through our AWS accounts. In order to interface with the machines you will have to use AWS Command Line Interface (CLI).


Install [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) by typing the following in your terminal:

    pip install awscli

**If on a Mac** type this instead:

    pip install awscli --ignore-installed six


Once installed we need to configure it. We have created an user for you with the privleges to start and stop a server (read more [here](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html)). You will recieve your `<Access_ID>` and `<Secret_Key>` separately.

    aws configure
    AWS Access Key ID []: <Access_ID>
    AWS Secret Access Key []: <Secret_Key>
    Default region name []: eu-west-1

Leave the rest as their default (just press enter).

You will also need the E2C Secret Key, a `.pem` file. Download it from [here](https://www.dropbox.com/s/1lht13gtyhqaryb/p2-xlarge.pem?dl=0), and save it somewhere that is easy to access. You will need to use this file everytime you want to launch your server.

Set the permissions using your terminal:

    cd <path to .pem file>
    chmod 400 p2-xlarge.pem


## Daily Use

You will be provided an AMI ID. This is the ID of your server for the entirity of the course. It will look something like this:

    i-0123456789abcdefg

Turn on the server

    aws ec2 start-instances --instance-ids <AWS instance ID>

Get your public DNS (for connecting to the server), and your public IP (for accessing the material in a browser) addresses. **These change value every time the server is shut down**.

    aws ec2 describe-instances --instance-ids <AWS instance ID> | grep Public

This will print the `publicDNS` and `publicIP` (three times). Save them somewhere temporarily.

Now we will connect to the actual server through `ssh`.

    cd <path to .pem file>
    ssh -i "p2-xlarge.pem" icarus@<publicDNS>
    Are you sure you want to continue connecting (yes/no)? yes
    icarus@<...>'s password: changetheworld
    
We are now connected to the server. Start the exercises by:

    cd 02456-deep-learning/
    jupyter notebook

We have now started a jupyter server, and are hosting it via the AWS server. View the exercises by opening your browser, and navigate to

    https://<publicIP>:8888

If you have multiple instances of Jupyter running (or other processes using your ports) the `8888` might be a different number. Check the output in the terminal if the above doens't work.
We have a self-signed certificate, so your browser will most likely come with a security complaint. Click 'advanced' (or something similar) and click 'proceed'.

The password is `42`.

You should now see an overview of the course material. Enjoy!


**When you are done**, or not using your server please shut it down. In your terminal (it doesn't matter if you are connected via `ssh`) type:

    aws ec2 stop-instances --instance-ids <AWS instance ID>



## After the course

The servers that you used will be deleted.


The privleges you were granted have been revoked (the things you setup through `aws config`). If you want to continue working with AWS sign up, and create your own account [here](https://aws.amazon.com/). If you want to keep the exercises, and the work that you did 

    scp -i p2-xlarge.pem -r icarus@<publicDNS>:~/02456-deep-learning/ <descitation folder>

set `<destination folder` to `.` if you want to download it to the current folder

If you would like to continue working with AWS there are many AMI's online where a lot of the set necessary software is pre-installed. The AMI that was used for this course is based on this [one](https://github.com/Miej/GoDeeper).


