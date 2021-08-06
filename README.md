# My CS50 Final Project: LinkLEARN
#### Video Demo: https://www.youtube.com/watch?v=kmoiaCc1pIg&t=5s
#### Description:

LinkLEARN is a webapp that helps consolidate links for learning a particular topic. Upon finishing the CS50 lectures, I found that I jumped to online sources like StackOverflow when I had problems in programming my final project. To help me and others who use the web to learn, I came up with the idea of LinkLEARN, which provides its user with a way to consolidate links which may be helpful in learning a particular topic. The user can even save a simple description and edit it afterwards as he sees fit to help him remember the salient points from a particular link, be it an online resource, forum or video! 

My concept is somewhat similar to LinkTree, but mine serves an educational purpose rather than a marketing purpose.

I decided not to use CS50 libraries in this project, taking off most of the training wheels. However, I did take the configuration, and helper functions from CS50's finance. I hope to continuously improve it so that one day, many people will use it! 

The latest update is that LinkLEARN's infrastructure is all in place. I'd consider it a MVP(minimum viable product)

## Let's run through the routes of the app 

### Home 
/index \
The home(or index) route displays all of the links (in the form of an anchor tag with their nicknames as the HTML InnerText) as well as their corresponding descriptions.\
Each link's description can be edited and saved again. This refreshes the page.\
Each link can also be deleted. I implemented a trash (see "Trash" ) system so that the link goes to a trash bin where it can be either restored back to the homepage, or permanently deleted.

### Add
The user adds links through this route. 3 fields need to be filled: URL, Nickname and Description.\
The cool thing about the nickname field to me is that I have implemented the app such that it displays the link in [Home](#home) as an anchor tag with the Nickname as its HTML Innertext.\
This anchor tag is displayed on the homepage along with its description and when clicked on, redirects the user to the stored URL in a new tab by default.

### Trash 
As explained previously, all of the user's temporarily deleted links are shown here and the user has the option to either restore the link to be displayed back in the homepage, or to be permanently deleted and only kept in History.

### History 
History displays all of the links added. I did put more thought into history to make it more useful to the user by indicating the current status of the links added. For each link shown in history, it is either in the homepage, trash, or permanently deleted(cannot restore). *I do think that History will be more useful if it tracks all the actions to links as well: editing descriptions, time of adding and time of deletions. However as the app is still in the MVP phase, I have yet to implement this. Will consider doing it in future*

### Register, Log in and Log out 
I did take CS50's implementation details for this but SQL was all done using Flask-SQLAlchemy. CS50 saved alot of hassle on this one!


### Lastly, Below is my "TODO" list for this project! I think at this stage it's ready for submission to CS50 as a final project. That being said, I will continue to work on it as it's my first project with version control on GitHub! 

#### COMPLETED: 
- Add links 
- Display Links on Home page 
- History of links 
- Temporarily Delete links 
- Permanently delete links  
- Restoration of links 
- Aesthetics of Home 
- Edit descriptions and save them.
- Fix timezone for timestamp *but not optimised*
- Register button in the centre of login page
- Add button in the centre of homepage
- Deploy to Web Server

#### TODO: ####
- Categorising links
- Displaying ALL actions in History
- Converting apology function into on-screen message
- Add change password functionality
- email functionality