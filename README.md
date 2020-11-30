# Multiverse-ClientServer
 Reworked multiverse client server with master

There is a few things to get to before you start.

READ all the readme files and this document completely before you start.

A MMO consist of a wide range of programming tied together to make use of a number of different systems. It is not an easy task for one person and usually needs a team of engineers, programmers, artists and support staff. Making a MMO is a very difficult undertaking and not for the faint at heart. There is no pushbutton and instant game here. You will be tasked with a lot of work to get a fully functional MMO. I have put together the old Multiverse engine for those that want to make a MMO and get it running. The instructions you get here are aimed at making it easier to install and get your basic system fully functional without having a whole range of issues as with the original version. The documentation is lacking but is being reworked as best I can. I can always use some help with the tasks involved.

I haven’t worked on this engine for a couple years. This version is still DirctX9 and using Axiom engine. I want to go ahead and release this version to see if there is any interest in releasing a newer version later or someone may want to use it as is. I want to state again, I am only working on a new client. In order to make more changes there would have to be others to work on the server. I would need a java programmer to update the server code to the newest version. I would need a database engineer and http needs work to build pages for users. I could do it but it would take a very long time to complete it. This version has been modified to work with the master server so you can connect to a remote server. You can connect to a VPS but that VPS needs to be setup. The master server can run on the same machine or be on a completely different server. The website can be on another. This is highly configurable.

There are SPECIFIC instructions in the configuration files to follow and are documented here. These instructions MUST be followed when compiling this engine to work with your system. If you try to compile it before making these changes the compiler will stop and error out. I built this into the code to alert you of where the changes have to happen. You simply edit the section and comment out the error code.

I decided to pick it back up and see what I could do to make it workable as a full blown system. There were a number of projects started and died I think mostly because of the complex task of getting a working system. Once the Multiverse master was turned off there was no way for developers to connect and build their games and there was so little information that most developers stopped working on their games. I studied this system and worked through the issues in order to make the master work and get the server talking to the client without having to deal with any special input. You just start the master, start the server and connect with the client now. The configuration files take care of everything. Right now it is pretty difficult to install on the client since there is no new installer but I give you detailed instruction on how to get your clients working for development environment. It is NOT ready for customers by a long shot and only meant for development. Once there is a game made there will be an installer.

The engine has been reworked to only run on a Unix platform. I decided to do away windows server and also standalone games so if you do not have some knowledge of Unix or Linux then you need to study the Linux manual. If you want to build a standalone game the rewrite the client. It’s not that hard if you know what you’re doing. It may run under Cygwin but I have not tested it. I’m not here to teach you Linux or programming. I will however give you the necessary tasks and links you need to get your system up and running with the basic game. If you undertake this project know full well it is written in 5 different language platforms (Python, C#, bash, Java, MySQL). You will need programming knowledge of these in order to make a full scale MMO.

For testing I am using VirtualBox 6 and Centos 7 for my server but you can use about any Linux or even Unix to run your server although some of the newer Linux may require a lot more effort as for example CentOS 8 will require a complete rewrite to work since the database driver requires a different type of time stamp with the new java DBC . I use CentOS for the fact this engine is capable of enterprise level with many different sub servers all tied together in a massive system. It is capable of handling millions of concurrent connections using the RPC of the operating systems. This will be covered in a different document later on installing development platforms because the process is extremely complex it will require a lot more detail. There is still some issues I am working on with multiple servers.

The system is capable of very large worlds and has been tested on worlds as large a  34,722,449,288 square meters although there is still a memory leak in this code since the code is the original. With he cluster system it can be unlimited in size but limited only by the cost to run it and the number of machines or clouds. With the use of enterprise MySQL the database can server up millions across the database cluster.

Server OS Installation instructions:

Setup your server if you haven’t yet. Use a version of Linux or Unix OS. I recommend you use CentOS 7 because it is enterprise level but you can choose which ever system you want. You will probably not have the necessary programs on a default install. Follow the OS install instructions of the system you select.

Make sure to install development tools. Python, Java, if you do server code then you need apache ant. Follow instructions in the readme.

Installing the Multiverse server. Extract the file called multiverse-server.zip into your home directory. I recommend that you use this zip to perserve permissions. You should have directory now called multiverse. Copy this to /usr

Open the file called master.sql and edit the values to match your server IP. Replace dave and test with your own user and password. I suggest you use a password other than multiverse. This is simply a example here. ALWAYS use secure passwords and NEVER use these defaults for a public game. They may work fine for a development environment but they can be hacked in the real world. Save this file.

NOTE: The master will not work if activated is not set to 1 or suspended is not set to zero. Do NOT change these values!

Start terminal
You should be in the home directory;
Type the following in terminal -> cd multiverse;

Type the following in terminal -> mysql -u root -p

Enter password

Type the following in terminal -> Source bin/install.sql;

Type the following in terminal -> Source bin/master.sql;

Your database is now setup for the master server and your game server.

For you website. (you need to be logged in a root) Copy the directorys in website to /etc/www/html. Do this as root and set the permissions to excute.

This is fully functional server and has been tested from a blank install.

In /usr/multiverse/bin is a file called master_server.py. I created a key for use but you should create your own key and replace this one. Google is your friend. You can find a number of methods to create keys on the web.

To run the server.

from home ---> cd /usr/multiverse/bin

          ---> ./master.sh start

          ---> ./multiverse.sh start

to stop the server.
          ---> ./master.sh stop

          ---> ./multiverse.sh stop

to check the status.
          ---> ./master.sh status

          ---> ./multiverse.sh status

Logging is set to WARN. Set the logging in master.properties and/or multiverse.properties to suit your taste. Make sure to rename server name to your server name (demonz1)

Client install is dirty and difficult.

Run the installers in the install directory.

Use Visual Studio 17 or 19 (built with both versions to test it)

Open Multiverse.sln in the directory MultiverseClient and compile it. Copy all the exe files that were created over to the program directories. Usually C:\Program Files (x86)\Multiverse Software Foundation For the tools and C:\Program Files (x86)\Multiverse Software Foundation\Multiverse Client\bin For the client. Make sure not to delete the dependencies.

Current settings in VS are debug you may want to change them but the code is such that you will have to comment out the logging since configuration only works in debug and logs everthing in release.

Good luck and enjoy.
