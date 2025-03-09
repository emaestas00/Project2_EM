from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from decimal import Decimal, InvalidOperation

from .models import Listing, Bid, Comment, Watchlist, User


# -------------------------------
# Home Page: Show Active Listings
# -------------------------------
def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {"listings": active_listings})


# -------------------------------
# Authentication Views (Login, Logout, Register)
# -------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "auctions/register.html")

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            messages.error(request, "Username already taken.")

    return render(request, "auctions/register.html")


# -------------------------------
# Create Listing
# -------------------------------
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        starting_bid = request.POST.get("starting_bid", "").strip()
        image = request.FILES.get("image")
        category = request.POST.get("category", "").strip()

        if not title or not description or not starting_bid:
            messages.error(request, "Please fill out all required fields.")
            return render(request, "auctions/create_listing.html")

        listing = Listing.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_bid=starting_bid,
            image=image or None,
            category=category or None,
            owner=request.user,
            is_active=True
        )

        messages.success(request, "Listing created successfully!")
        return redirect("listing", listing_id=listing.id)

    return render(request, "auctions/create_listing.html")


# -------------------------------
# View Listing (Bidding, Watchlist, Closing)
# -------------------------------
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    highest_bid = Bid.objects.filter(listing=listing).order_by("-amount").first()
    is_owner = request.user == listing.owner
    is_on_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists() if request.user.is_authenticated else False

    if highest_bid:
        listing.current_bid = highest_bid.amount
        listing.save()

    # Handle Closing the Auction (Owner Only)
    if request.method == "POST" and "close_auction" in request.POST and is_owner and listing.is_active:
        listing.is_active = False
        listing.save()
        messages.success(request, "The auction has been closed.")
        return redirect("listing", listing_id=listing.id)

    # Handle Bidding
    if request.method == "POST" and "bid_submit" in request.POST:
        bid_amount = request.POST.get("bid", "").strip()

        if not bid_amount:
            messages.error(request, "Please enter a bid amount.")
        else:
            try:
                bid_amount = Decimal(bid_amount)

                if bid_amount < listing.starting_bid:
                    messages.error(request, "Your bid must be at least the starting price.")
                elif bid_amount <= listing.current_bid:
                    messages.error(request, "Your bid must be higher than the current bid.")
                else:
                    new_bid = Bid.objects.create(listing=listing, user=request.user, amount=bid_amount)
                    listing.current_bid = new_bid.amount
                    listing.save()
                    messages.success(request, "Bid placed successfully!")

            except (ValueError, InvalidOperation):
                messages.error(request, "Invalid bid amount. Please enter a valid number.")

        return redirect("listing", listing_id=listing.id)

    # Handle Comments
    if request.method == "POST" and "comment_submit" in request.POST:
        comment_content = request.POST["comment"].strip()

        if comment_content:
            Comment.objects.create(listing=listing, commenter=request.user, content=comment_content)
            messages.success(request, "Comment posted successfully!")

        return redirect("listing", listing_id=listing.id)

    user_won = request.user == highest_bid.user if highest_bid and not listing.is_active else False

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_owner": is_owner,
        "is_on_watchlist": is_on_watchlist,
        "highest_bid": highest_bid,
        "comments": Comment.objects.filter(listing=listing).order_by("-created_at"),
        "user_won": user_won,
    })


# -------------------------------
# Watchlist (Add, Remove, View)
# -------------------------------
def watchlist(request):
    watchlist_items = [entry.listing for entry in Watchlist.objects.filter(user=request.user).select_related("listing")]
    return render(request, "auctions/watchlist.html", {"watchlist_items": watchlist_items})


def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    Watchlist.objects.get_or_create(user=request.user, listing=listing)
    messages.success(request, f"'{listing.title}' was added to your watchlist.")
    return redirect("listing", listing_id=listing.id)


def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    deleted_count, _ = Watchlist.objects.filter(user=request.user, listing=listing).delete()

    if deleted_count:
        messages.success(request, f"'{listing.title}' was removed from your watchlist.")
    else:
        messages.warning(request, "This listing was not in your watchlist.")

    return redirect("listing", listing_id=listing.id)


# -------------------------------
# Categories (View Listings by Category)
# -------------------------------
def categories(request):
    all_categories = Listing.objects.values_list("category", flat=True).distinct().order_by("category")
    active_category_counts = {
        cat["category"]: cat["count"] for cat in Listing.objects.filter(is_active=True).values("category").annotate(count=Count("category"))
    }
    categories = [{"category": cat, "count": active_category_counts.get(cat, 0)} for cat in all_categories]
    
    return render(request, "auctions/categories.html", {"categories": categories})


def category_listings(request, category_name):
    listings = Listing.objects.filter(category=category_name, is_active=True)
    return render(request, "auctions/category_listings.html", {"category_name": category_name, "listings": listings})
