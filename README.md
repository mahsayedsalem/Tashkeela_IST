# Tashkeela_IST

## Problem Statement

A web application which enables its’ users to enter an Arabic sentence then get it’s diacritized version of the sentence. 
A dataset was given to aid in the solution of the problem in hand.

## Constraints
The representation was constrained to Spring Java as back-end and Angular as front-end. Time limit was 10 days.


## Planning and Deployment

We have 2 main components. The 1st component was the NLP solution which deals with abstract concepts. An Arabic sentence as input, a diacritized version of the word as an output. 

The 2nd component was the representation. It was constrained by using Spring Framework as back-end framework and Angular as front-end framework. 
The time I could give to the task in total from the 10 days, was 3 and half days. 
I had basic experience in NLP but passion to learn, and no experience at all in both Angular and Spring. So I started with the NLP task. 

Examining the data that was given to me, it was clear that it’s a quite difficult problem for various reasons. The data itself wasn’t clean at all. In the documentation some folders supposed to have hundreds of files but in the Kaggle dataset the folder was empty. After simple preprocessing the number of words of obtained was around 50K word. For an NLP task that wasn't enough.

So I researched the literature of this dataset. I found a Hidden Markov Model based solution https://github.com/Anwarvic/Tashkeela-Model , it was quite good and doesn’t actually need lots of data as it treats every letter as a state by itself. One drawback that kept me from using this approach though, it worked mainly on maximum of 3-characters gram level. Reading about Arabic grammar, I knew this wasn’t enough. We need to work on word level, not characters. This was seen while testing this approach, it didn’t perform like expected.

There were almost no other framework solutions using this dataset. So I started researching for a pre-trained model which was trained to do the same inference as I need.

The best one I found, by far, was Shakkala pre-trained model: https://github.com/Barqawiz/Shakkala

It performed great while testing with a decent speed which makes it quite good candidate for a real time application. It was also published under the MIT License granting me the full access to publish, edit or built upon the model and codebase. 
Testing the model on some random words from the Tashkeela corpus it gave 95% accuracy on character level, and 73% on words level.

Given the time constrained I was in, this was the best approach to proceed in. I started wrapping the Shakkala model to be deployable ready, i.e. be ready to be integrated to a Spring Back-end.

The previous research took around a day and half to be finished (12.5 working hours)

I started the second part of the task which was a complete grey area for me. I’ve never worked with both Angular and Spring. I have a 3-months experience in web development using Flask Framework integrated with Bootstrap thus, and I developed one feature using React. But never used Angular and Spring.

I faced a lot of problems, one of them is that there are too much literature about Spring. This naturally shouldn’t be a problem but it was because when I followed the same steps I found I download or configure different versions of the framework. I searched for Tutorials which integrates Angular to Spring, I found some. I faced some problems in creating an Angular project, something related to permissions. I spent some time following up for solutions. Then faced some problems configuring Spring. For some tutorials I downloaded Tomcat and others I downloaded Glassfish. I faced problems with each of them. I even had problems running it using an IDE in development mode.
In a nutshell, it didn’t work as expected. When I finally built a project integrating them both, and it run, I had problems understanding the syntax of Angular and figuring out how to send and receive the data from the Spring back-end. I knew that even after I find a solution for these problems I will have another problem of integrating my wrapped python code to the spring framework back-end. I’ve already spend 2 days (18 hours) in the above steps. Probably with more time, I might have succeeded, but there was no time and I needed to make a decision to switch to Flask.

I have experience with Flask so building the web application and integrating it to the NLP solution took very little time.


## Run and Install

In order to share it in an easy way, I deployed my application to Heroku servers. The link for the application:  https://isttashkeelatask.herokuapp.com/ where you can freely test the model.
Yet the request time in Heroku is very short, so you can only try it was a word or two. For a complete phrase, try running it locally.

First, clone the project
`git clone https://github.com/mahsayedsalem/Tashkeela_IST.git`

Open the folder you will find a batch file called *setup.bat*. 
Open it and replace the first two lines with your python paths. 
For example the first two lines on my computer looks like this:
"C:\python35\python.exe" -m pip install virtualenv
"C:\python35\Scripts\virtualenv" env
That’s because my Python folder is "C:\python35”.

Wherever your python folder is, replace it with mine. Each python folder will have python.exe and a Script folder which has a virtualenv file. We need these two paths in order to be able to setup our project.

“Why should we do this” is a good question. Because another simple solution is simply go to my application folder and pip install requirements.txt then run the application, yet the packages will be downloaded on your main Python environment. What the setup does is creating a separate environment for this project only to avoid any problems with previous projects.
After you edit the *setup bat*, all you have to do is run it. It will build the environment, download the dependencies and take care of everything for you. Once it finished you can run the *run-server.bat* to run the server locally.
