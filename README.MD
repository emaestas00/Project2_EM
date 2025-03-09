# Project 2 Overview
Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

I had a difficult time with this project and had to restart it many times. I hope some of my implementation notes can assist someone working through this project as well. 

# Requirements.txt
This file lists the necessary Python packages for my Django project, ensuring that all dependencies are installed when setting up the project environment. In this file there are comments explaining how each was used. 

# Resources

* Visual Studio - this is the resource I used to build my project. I find visual studio to be a great help as it often provides suggestions based on items you've already created. One example being building models. I built the first model and it recommended how to build the following. This on top of general debugging allowed for me to move through this project. 

* CSSCI AI Model - AI models are helpful when debugging. In this project I was running into issues with powershell and my environments and this AI model helped me verify what was wrong. 

* Pip Documentation - https://pip.pypa.io/en/stable/reference/requirements-file-format/

* Django Documentation - https://docs.djangoproject.com/en/3.0/ref/models/fields/

* Django Forms Documentation - https://docs.djangoproject.com/en/3.0/topics/forms/


# Task Models
Task: Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.

Implementation Notes: 

Listing Model
Represents an auction listing with the following fields:
* Title (CharField) – The name of the auction item.
* Description (TextField) – A detailed description of the item.
* Starting Bid (DecimalField) – The minimum price required to start bidding.
* Current Bid (DecimalField) – The highest bid currently placed.
* Image (URLField, optional) – A URL linking to an image of the item.
* Category (CharField) – A category classification for easier filtering (e.g., Electronics, Clothing, Home, etc.).
* Owner (ForeignKey to User) – The user who created the listing.
* is_active (BooleanField, default=True) – Indicates whether the auction is still open.
* created_at (DateTimeField, auto_now_add=True) – The timestamp of when the listing was created.

Bid Model
Tracks bids placed on listings. Each bid belongs to a specific listing and is associated with a user.
* Listing (ForeignKey to Listing) – The auction listing on which the bid is placed.
* User (ForeignKey to User) – The user who placed the bid.
* Amount (DecimalField) – The bid amount, which must be greater than the previous highest bid.
* created_at (DateTimeField, auto_now_add=True) – The timestamp of when the bid was placed.

Comment Model
Stores comments made by users on auction listings.
* Listing (ForeignKey to Listing) – The listing on which the comment is made.
* Commenter (ForeignKey to User) – The user who made the comment.
* Content (TextField) – The content of the comment.    
* created_at (DateTimeField, auto_now_add=True) – The timestamp of when the comment was posted.

Watchlist Model
Allows users to track listings they are interested in.
* User (ForeignKey to User) – The user who added the listing to their watchlist.
* Listing (ForeignKey to Listing) – The auction listing being watched.
* created_at (DateTimeField, auto_now_add=True) – The timestamp of when the * listing was added to the watchlist.

# Task: Create Listing
Task: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

Implementation Notes: 

Listing.HTML
* Step 1: Created an HTML template called create_listing 
    * A form that allows the use to enter title, description, starting bid and optionally add an image and category. I did give them the option of hand entering in their category value or selecting from a pre-populated list.

* Step 2: Form Behavior and UX Enhancements 
    * Used CSRF protection as recommended during the lecture to ensure secure submissions. 
    * Provided form validation. 

* Step 3: Views.py
    * Created a listing view function to handle form submission
    * When the form is validated, a new listing object is created and saved to db. 
    * The user is redirected to the active listings page after. 
* Step 4: URL Configuation
    * Added a URL pattern for /create and the create_listing view

# Task Active Listings Page
Task: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).

Implementation Notes: 

* Step 1: update index.html
    * Update the index to dynamically display all active auction listings
    * Create cards that have listing details and display images if there are one. 
* Step 2: UX Enhancements
    * Used bootstrap to create 'cards' and a aesthetic layout. 
* Step 3: Views.py update 
    * Created a view function that retrieves and displays only active listings. 
* Step 4: URL Configuration 
    * Set the default route to call the index view

# Task Listing Page
Task: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
    If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
    If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
    If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
    If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
    Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.

Implementation Notes: 
* Step 1: create listing.html 
    * This dynamically displays all details of the specific listing. 
* Step 2: Watchlist
    * If the user is signed in, they can add/remove the item from their watchlist.
    * If the listing is already in the user’s watchlist, clicking “Remove from Watchlist” removes it.
    * If not, clicking “Add to Watchlist” adds it.
* Step 3: Bidding and Validation
    * Users who are signed in can place a bid via a form on the listing page.
    * Ensure the bid meets or exceeds the starting bid.
    * Ensure the bid is higher than any existing bid.
    * Display an error message if the bid is invalid.
    * If valid, update the current highest bid and refresh the page.

* Step 4: Close
    * If the logged-in user is the listing owner, they see a “Close Auction” button.
    * Clicking this button Marks the listing as inactive (is_active=False). 
    Declares the highest bidder as the winner (if there were any bids).

* Step 5: Display Message
    * If the user is signed in and is the winner, the page displays:
        “Congratulations! You won this auction.”
    * If the user is not the winner, they simply see that the auction is closed.

* Step 6: Comments 
    * Signed-in users can add comments to the listing.
    * Comments are displayed chronologically beneath the listing details.

* Step 7: UX Enhancements
    *  Styled with Bootstrap for a clean, intuitive UI.
    *  Error handling & validation messages for bids and comments.
* Step 8: Views.py 
    * Created a view function (listing) to handle displaying a single listing
        Retrieves the Listing object using its unique ID.
        Fetches all related bids to determine the highest bid.
        Fetches comments associated with the listing.
        Checks if the current user has added the listing to their watchlist.
        Checks if the user is the listing owner to enable the auction-closing option.
        Passes all necessary data to listing.html for rendering.
* Step 9: URLs
    * Added a route for listing pages

# Task Watchlist
Task: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

Implementation Notes: 
* Step 1: create watchlist.html
    * Displays all listings a user has added to their watchlist.
    * If the user has no saved listings, the page displays a "No items in watchlist" message.
* Step 2: Add or Remove Listings
    * Implemented POST request handlers for watchlist actions
     If a user clicks “Remove from Watchlist”, the listing is removed from their saved items.
    If a user clicks “Add to Watchlist” from the listing page, it is added to their watchlist.
    * The page dynamically updates to reflect the change.
* Step 3: UX Enhancements
    * Similar style cards to the active listing page. 
* Step 4: Views.py 
    * Created a view function (watchlist) to display the current user’s saved listings.
    Ensures the user is authenticated
    Retrieves all listings where the user has added them to their watchlist.
    Passes the list of saved listings to watchlist.html for rendering.
* Step 5: URLs
    * Added a route for the watchlist page
# Task Categories
Task: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

Implementation Notes: 
* Step 1: create categories.html and categoyr_listings.html
    * Created an HTML template named categories.html that lists all available categories.
    * Each category name is a clickable link that redirects users to a page displaying active listings within that category.
    * Created a separate template named category_listings.html to display all active listings under a selected category.

* Step 2: Views.py 
    * Created a view function (categories) to display a list of unique categories:
    * Created another view function (category_listings) to display listings in a selected category
* Step 3: URLs
    * Added routes for category pages
# Django Admin Interface
Task: Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.

Implementation Notes: 
This was completed by registering the Listing, Bid, and Comment models in Django’s admin.py using admin.site.register(). This allows the site administrator to view, add, edit, and delete these models via the Django admin interface. Additionally, the admin panel was customized to display relevant fields for easier management.

# Style.css
The styles.css file was used to enhance the visual design and usability of the auction site. It was applied to various templates to ensure a clean, modern, and consistent look. 

# Views.py Overview
The views.py file in this project contains the logic for handling user requests and rendering the appropriate responses. It manages:

* Displaying Listings – Shows active auction listings on the homepage and allows users to view individual listings.
* User Actions – Handles bidding, adding/removing items from the watchlist, posting comments, and closing auctions.
* Forms & Validation – Processes user-submitted data for creating listings, placing bids, and commenting, ensuring required conditions are met.
* Category & Watchlist Pages – Retrieves and displays listings filtered by category or a user’s saved watchlist.
* Authentication & Permissions – Ensures only logged-in users can perform certain actions, such as bidding or modifying their watchlist.

# URLS.py Overview
The urls.py file in this project defines the URL routing, mapping specific web addresses to their corresponding view functions in views.py. It ensures users can navigate the site and access different features.



